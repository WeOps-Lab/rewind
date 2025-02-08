from datetime import datetime, timezone

from apps.cmdb.constants import CREDENTIAL, CREDENTIAL_ASSOCIATION, ENCRYPTED_KEY, INSTANCE
from apps.cmdb.graph.neo4j import Neo4jClient
from apps.cmdb.models import CREATE_INST_ASST, DELETE_INST_ASST
from apps.cmdb.services.instance import InstanceManage
from apps.cmdb.utils.change_record import create_change_record_by_asso
from apps.cmdb.utils.credential import Credential


class CredentialManage(object):
    @staticmethod
    def credential_list(credential_type: str, operator: str, page: int, page_size: int, order: str = None):
        """获取凭据列表"""
        params = [
            {"field": "_creator", "type": "str=", "value": operator},
            {"field": "credential_type", "type": "str=", "value": credential_type},
        ]
        _page = dict(skip=(page - 1) * page_size, limit=page_size)
        if order and order.startswith("-"):
            order = f"{order.replace('-', '')} DESC"

        with Neo4jClient() as ag:
            inst_list, count = ag.query_entity(
                CREDENTIAL,
                params,
                page=_page,
                order=order,
            )

        return dict(items=inst_list, count=count)

    @staticmethod
    def get_encryption_field(_id, field: str):
        """获取加密字段"""
        with Neo4jClient() as ag:
            data = ag.query_entity_by_id(_id)
        if field not in ENCRYPTED_KEY:
            return data.get(field, "")
        secret = Credential().decrypt_data(data.get(field, ""))
        return secret

    @staticmethod
    def create_credential(credential_type: str, data: dict, operator: str):
        """创建凭据"""

        for key, value in data.items():
            # 密钥类属性加密
            if key in ENCRYPTED_KEY:
                data[key] = Credential().encrypt_data(value)

        now_time = datetime.now(timezone.utc).isoformat()
        info = dict(credential_type=credential_type, update_time=now_time, **data)
        with Neo4jClient() as ag:
            result = ag.create_entity(CREDENTIAL, info, {}, [], operator)
        return result

    @staticmethod
    def update_credential(_id, data: dict):
        """更新凭据"""
        for key, value in data.items():
            # 密钥类属性加密
            if key in ENCRYPTED_KEY:
                data[key] = Credential().encrypt_data(value)

        now_time = datetime.now(timezone.utc).isoformat()
        data.update(update_time=now_time)
        with Neo4jClient() as ag:
            _ = ag.set_entity_properties(CREDENTIAL, [_id], data, {}, [], False)

    @staticmethod
    def batch_delete_credential(ids: list):
        """批量删除凭据"""
        with Neo4jClient() as ag:
            ag.batch_delete_entity(CREDENTIAL, ids)

    @staticmethod
    def credential_asso_inst(data, operator: str):
        """凭据关联实例"""

        asso_instances = data.get("instance_ids", [])
        with Neo4jClient() as ag:
            assos = ag.query_edge(
                CREDENTIAL_ASSOCIATION,
                [
                    {"field": "id", "type": "id=", "value": data["credential_id"]},
                    {"field": "asst_model_id", "type": "str=", "value": data["model_id"]},
                ],
            )

        exist_instance_assos = {i["instance_id"]: i["_id"] for i in assos}

        del_asso_ids = [exist_instance_assos[i] for i in exist_instance_assos.keys() if i not in asso_instances]
        for asso_id in del_asso_ids:
            CredentialManage.credential_association_delete(asso_id, operator)

        add_asso_instance_ids = [i for i in asso_instances if i not in exist_instance_assos]
        for instance_id in add_asso_instance_ids:
            CredentialManage.credential_association_create(
                dict(
                    credential_id=data["credential_id"],
                    instance_id=instance_id,
                    asst_model_id=data["model_id"],
                    _creator=operator,
                ),
                operator,
            )

    @staticmethod
    def credential_asso_inst_list(query_dict, operator: str):
        """获取凭据关联实例列表"""
        credential_id = query_dict.get("credential_id")
        if credential_id:
            with Neo4jClient() as ag:
                query_data = [
                    {"field": "credential_id", "type": "int=", "value": credential_id},
                    {"field": "_creator", "type": "str=", "value": operator},
                ]
                edges = ag.query_edge(CREDENTIAL_ASSOCIATION, query_data, return_entity=True)
            return [i["dst"] for i in edges]

        instance_id = query_dict.get("instance_id")
        if instance_id:
            with Neo4jClient() as ag:
                query_data = [
                    {"field": "instance_id", "type": "int=", "value": instance_id},
                    {"field": "_creator", "type": "str=", "value": operator},
                ]
                edges = ag.query_edge(CREDENTIAL_ASSOCIATION, query_data, return_entity=True)
            return [i["src"] for i in edges]

        return []

    @staticmethod
    def credential_association_create(data: dict, operator: str):
        """创建凭据关联"""

        with Neo4jClient() as ag:
            edge = ag.create_edge(
                CREDENTIAL_ASSOCIATION,
                data["credential_id"],
                CREDENTIAL,
                data["instance_id"],
                INSTANCE,
                data,
                "asst_model_id",
            )
        asso_info = InstanceManage.instance_association_by_asso_id(edge["_id"])
        create_change_record_by_asso(CREDENTIAL_ASSOCIATION, CREATE_INST_ASST, asso_info, operator=operator)

    @staticmethod
    def credential_association_delete(asso_id: int, operator: str):
        """删除凭据关联"""

        asso_info = InstanceManage.instance_association_by_asso_id(asso_id)

        with Neo4jClient() as ag:
            ag.delete_edge(asso_id)

        create_change_record_by_asso(CREDENTIAL_ASSOCIATION, DELETE_INST_ASST, asso_info, operator=operator)
