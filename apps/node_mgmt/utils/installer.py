from apps.rpc.executor import Executor


def exec_command(ip, port, username, password, command):
    pass


# 文件下发
def send_file(ip, port, username, password, local_file, remote_file):
    pass


# 执行本地命令
def exec_command_to_local(instance_id, command):
    exe_obj = Executor(instance_id)
    result = exe_obj.execute_local(command, timeout=60)
    return result


# 执行远程命令
def exec_command_to_remote(instance_id, ip, username, password, command):
    exe_obj = Executor(instance_id)
    result = exe_obj.execute_ssh(command, ip, username, password=password, timeout=60)
    return result


# 文件下发到本地
def download_to_local(instance_id, bucket_name, file_key, file_name, target_path):
    exe_obj = Executor(instance_id)
    result = exe_obj.download_to_local(bucket_name, file_key, file_name, target_path, timeout=60)
    return result


# 文件下发到远程
def download_to_remote(instance_id, bucket_name, file_key, file_name, target_path, host, username, password):
    exe_obj = Executor(instance_id)
    result = exe_obj.download_to_remote(bucket_name, file_key, file_name, target_path, host, username, password, timeout=60)
    return result
