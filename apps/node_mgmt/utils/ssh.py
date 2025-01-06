import re
import time
import logging
from uuid import uuid4
from io import StringIO

from paramiko import RSAKey
from paramiko.client import SSHClient, AutoAddPolicy

logger = logging.getLogger(__name__)


class CommandResult:
    def __init__(self, exit_code: int, output: str):
        self.exit_code = exit_code
        self.output = output


class SSH:
    def __init__(self, hostname, port=22, username='root', pkey=None, password=None, default_env=None,
                 connect_timeout=10, term=None):
        """
        初始化 SSH 连接参数
        """
        self.stdout = None
        self.client = None
        self.channel = None
        self.sftp = None
        self.exec_file = None
        self.term = term or {}
        self.eof_msg = 'WEOPS LITE NODE MGMT'
        self.default_env = default_env
        self.command_pattern = re.compile(r'WEOPS LITE NODE MGMT (-?\d+)[\r\n]?')
        self.connection_params = {
            'hostname': hostname,
            'port': port,
            'username': username,
            'password': password,
            'pkey': self._load_private_key(pkey),
            'timeout': connect_timeout,
            'allow_agent': False,
            'look_for_keys': False,
            'banner_timeout': 30
        }

    @staticmethod
    def _load_private_key(pkey):
        if isinstance(pkey, str):
            return RSAKey.from_private_key(StringIO(pkey))
        return pkey

    @staticmethod
    def generate_key():
        """
        生成新的 SSH 密钥对
        """
        key_buffer = StringIO()
        key = RSAKey.generate(2048)
        key.write_private_key(key_buffer)
        return key_buffer.getvalue(), f'ssh-rsa {key.get_base64()}'

    def get_client(self):
        """
        初始化并返回 SSH 客户端
        """
        if self.client:
            return self.client
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy)
        self.client.connect(**self.connection_params)
        return self.client

    def ping(self):
        """
        检查 SSH 连接是否可用
        """
        return True

    def add_public_key(self, public_key):
        """
        向远程服务器添加公钥
        """
        command = f'mkdir -p -m 700 ~/.ssh && echo {public_key!r} >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys'
        result = self.exec_command_raw(command)
        if result.exit_code != 0:
            raise Exception(f'Error adding public key: {result.output}')

    def exec_command_raw(self, command, environment=None):
        """
        在远程服务器上执行命令，并返回原始结果
        """
        transport = self.get_client().get_transport()
        channel = transport.open_session()
        if environment:
            channel.update_environment(environment)
        channel.set_combine_stderr(True)  # 合并标准错误输出到标准输出
        channel.exec_command(command)
        exit_code = channel.recv_exit_status()
        output = self._decode(channel.recv(-1))
        return CommandResult(exit_code, output)

    def exec_command(self, command, environment=None):
        """
        在远程服务器上执行命令，并处理自定义控制台输出
        """
        channel = self._get_channel()
        command = self._prepare_command(command, environment)
        channel.sendall(command)
        output, exit_code = '', -1

        for line in self.stdout:
            match = self.command_pattern.search(line)
            if match:
                exit_code = int(match.group(1))
                line = line[:match.start()]
                output += line
                break
            output += line
        return CommandResult(exit_code, output)

    def _win_exec_command_with_stream(self, command, environment=None):
        """
        在 Windows 远程服务器上以流的形式执行命令，并迭代输出结果
        """
        transport = self.client.get_transport()
        channel = transport.open_session()
        if environment:
            channel.update_environment(environment)
        channel.set_combine_stderr(True)
        channel.get_pty(width=102)
        channel.exec_command(command)
        stdout = channel.makefile("rb", -1)

        # Iterator
        for line in stdout:
            if line:
                yield channel.recv_exit_status(), self._decode(line)
        yield channel.recv_exit_status(), self._decode(line)

    def exec_command_with_stream(self, command, environment=None):
        """
        以流的方式执行命令，并迭代输出结果
        """
        channel = self._get_channel()
        command = self._prepare_command(command, environment)
        channel.sendall(command)

        exit_code, output_line = -1, ''
        while True:
            output_line = self._decode(channel.recv(8196))
            if not output_line:
                break
            match = self.command_pattern.search(output_line)
            if match:
                exit_code = int(match.group(1))
                output_line = output_line[:match.start()]
                break
            yield exit_code, output_line
        yield exit_code, output_line

    def put_file(self, local_path, remote_path, callback=None):
        """
        上传本地文件到远程服务器
        """
        sftp = self._get_sftp()
        sftp.put(local_path, remote_path, callback=callback)

    def put_file_by_fl(self, fl, remote_path, callback=None):
        """
        通过文件流上传文件
        """
        sftp = self._get_sftp()
        sftp.putfo(fl, remote_path, callback=callback, confirm=False)

    def list_dir_attr(self, path):
        """
        列出目录下所有文件的属性
        """
        sftp = self._get_sftp()
        return sftp.listdir_attr(path)

    def sftp_stat(self, path):
        """
        获取远程服务器上文件的状态信息
        """
        sftp = self._get_sftp()
        return sftp.stat(path)

    def remove_file(self, path):
        """
        删除远程服务器上的文件
        """
        sftp = self._get_sftp()
        sftp.remove(path)

    def _get_channel(self):
        """
        获取或初始化 Shell channel
        """
        if self.channel:
            return self.channel

        self.channel = self.client.invoke_shell(**self.term)
        self._initialize_shell()
        return self.channel

    def _initialize_shell(self):
        """
        初始化 Shell 环境
        """
        command = '[ -n "$BASH_VERSION" ] && set +o history\n'
        command += '[ -n "$ZSH_VERSION" ] && set +o zle && set -o no_nomatch\n'
        command += 'export PS1= && stty -echo\n'
        command = self._prepare_command(command, self.default_env)
        self.channel.sendall(command)

        response = ''
        attempts = 0
        while True:
            if self.channel.recv_ready():
                response += self._decode(self.channel.recv(8196))
                if self.command_pattern.search(response):
                    self.stdout = self.channel.makefile('r')
                    break
            elif attempts >= 100:
                self.client.close()
                raise Exception('Timeout while waiting for shell initialization')
            else:
                attempts += 1
                time.sleep(0.1)

    def _get_sftp(self):
        """
        获取或初始化 SFTP 客户端
        """
        if self.sftp:
            return self.sftp
        self.sftp = self.client.open_sftp()
        return self.sftp

    def _prepare_command(self, command, environment):
        """
        准备命令，将环境变量嵌入命令
        """
        new_command = ""
        if not self.exec_file:
            self.exec_file = f'/tmp/spug.{uuid4().hex}'
            new_command += f'trap \'rm -f {self.exec_file}\' EXIT\n'

        if environment:
            env_commands = ' '.join(
                f'export {k.replace("-", "_")}="{self._escape_quotes(v)}"' for k, v in environment.items())
            new_command += f'{env_commands}\n'

        new_command += command
        new_command += f'\necho {self.eof_msg} $?\n'
        self.put_file_by_fl(StringIO(new_command), self.exec_file)
        return f'. {self.exec_file}\n'

    @staticmethod
    def _escape_quotes(value):
        """
        Escapes single quotes in the given value for use in shell commands.
        """
        return value.replace("'", "'\"'\"'")

    @staticmethod
    def _decode(content):
        """
        解码字节流内容，尝试多种编码格式
        """
        try:
            return content.decode()
        except UnicodeDecodeError:
            return content.decode(encoding='GBK', errors='ignore')

    def __enter__(self):
        """
        进入上下文管理，建立 SSH 连接
        """
        self.get_client()
        transport = self.client.get_transport()
        if 'windows' in transport.remote_version.lower():
            logger.info("Remote system is Windows. Adjusting command methods accordingly.")
            self.exec_command = self.exec_command_raw
            self.exec_command_with_stream = self._win_exec_command_with_stream
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        离开上下文管理，关闭 SSH 连接
        """
        if self.client:
            self.client.close()
        self.client = None
