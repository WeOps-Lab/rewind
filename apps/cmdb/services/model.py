import json

from apps.cmdb.constants import (
    CLASSIFICATION,
    CREATE_MODEL_CHECK_ATTR,
    INST_NAME_INFOS,
    INSTANCE,
    MODEL,
    MODEL_ASSOCIATION,
    ORGANIZATION,
    SUBORDINATE_MODEL,
    UPDATE_MODEL_CHECK_ATTR_MAP,
    USER,
)
from apps.cmdb.graph.neo4j import Neo4jClient
from apps.cmdb.language.service import SettingLanguage
from apps.cmdb.services.classification import ClassificationManage
from apps.core.exceptions.base_app_exception import BaseAppException
from apps.core.utils.keycloak_client import KeyCloakClient


class ModelManage(object):
    @staticmethod
    def create_model(data: dict):
        """
        创建模型
        """
        # 对模型初始化默认属性实例名称
        data.update(attrs=json.dumps(INST_NAME_INFOS))

        with Neo4jClient() as ag:
            exist_items, _ = ag.query_entity(MODEL, [])
            result = ag.create_entity(MODEL, data, CREATE_MODEL_CHECK_ATTR, exist_items)
            classification_info = ClassificationManage.search_model_classification_info(data["classification_id"])
            _ = ag.create_edge(
                SUBORDINATE_MODEL,
                classification_info["_id"],
                CLASSIFICATION,
                result["_id"],
                MODEL,
                dict(
                    classification_model_asst_id=f"{result['classification_id']}_{SUBORDINATE_MODEL}_{result['model_id']}"  # noqa
                ),
                "classification_model_asst_id",
            )
        return result

    @staticmethod
    def delete_model(id: int):
        """
        删除模型
        """
        with Neo4jClient() as ag:
            ag.batch_delete_entity(MODEL, [id])

    @staticmethod
    def update_model(id: int, data: dict):
        """
        更新模型
        """
        model_id = data.pop("model_id", "")  # 不能更新model_id
        with Neo4jClient() as ag:
            exist_items, _ = ag.query_entity(MODEL, [{"field": "model_id", "type": "str<>", "value": model_id}])
            model = ag.set_entity_properties(MODEL, [id], data, UPDATE_MODEL_CHECK_ATTR_MAP, exist_items)
        return model[0]

    @staticmethod
    def search_model(language: str = "en"):
        """
        查询模型
        """
        with Neo4jClient() as ag:
            models, _ = ag.query_entity(MODEL, [])
        lan = SettingLanguage(language)

        for model in models:
            model["model_name"] = lan.get_val("MODEL", model["model_id"]) or model["model_name"]

        return models

    @staticmethod
    def parse_attrs(attrs: str):
        return json.loads(attrs.replace('\\"', '"'))

    @staticmethod
    def create_model_attr(model_id, attr_info):
        """
        创建模型属性
        """
        with Neo4jClient() as ag:
            model_query = {"field": "model_id", "type": "str=", "value": model_id}
            models, model_count = ag.query_entity(MODEL, [model_query])
            if model_count == 0:
                raise BaseAppException("model not present")
            model_info = models[0]
            attrs = ModelManage.parse_attrs(model_info.get("attrs", "[]"))
            if attr_info["attr_id"] in {i["attr_id"] for i in attrs}:
                raise BaseAppException("model attr repetition")
            attrs.append(attr_info)
            result = ag.set_entity_properties(MODEL, [model_info["_id"]], dict(attrs=json.dumps(attrs)), {}, [], False)

        attrs = ModelManage.parse_attrs(result[0].get("attrs", "[]"))

        attr = None
        for attr in attrs:
            if attr["attr_id"] != attr_info["attr_id"]:
                continue
            attr = attr

        return attr

    @staticmethod
    def update_model_attr(model_id, attr_info):
        """
        更新模型属性
        """
        with Neo4jClient() as ag:
            model_query = {"field": "model_id", "type": "str=", "value": model_id}
            models, model_count = ag.query_entity(MODEL, [model_query])
            if model_count == 0:
                raise BaseAppException("model not present")
            model_info = models[0]
            attrs = ModelManage.parse_attrs(model_info.get("attrs", "[]"))
            if attr_info["attr_id"] not in {i["attr_id"] for i in attrs}:
                raise BaseAppException("model attr not present")
            for attr in attrs:
                if attr_info["attr_id"] != attr["attr_id"]:
                    continue
                attr.update(
                    attr_group=attr_info["attr_group"],
                    attr_name=attr_info["attr_name"],
                    is_required=attr_info["is_required"],
                    editable=attr_info["editable"],
                    option=attr_info["option"],
                )

            result = ag.set_entity_properties(MODEL, [model_info["_id"]], dict(attrs=json.dumps(attrs)), {}, [], False)

        attrs = ModelManage.parse_attrs(result[0].get("attrs", "[]"))

        attr = None
        for attr in attrs:
            if attr["attr_id"] != attr_info["attr_id"]:
                continue
            attr = attr

        return attr

    @staticmethod
    def delete_model_attr(model_id: str, attr_id: str):
        """
        删除模型属性
        """
        with Neo4jClient() as ag:
            model_query = {"field": "model_id", "type": "str=", "value": model_id}
            models, model_count = ag.query_entity(MODEL, [model_query])
            if model_count == 0:
                raise BaseAppException("model not present")
            model_info = models[0]
            attrs = ModelManage.parse_attrs(model_info.get("attrs", "[]"))
            new_attrs = [attr for attr in attrs if attr["attr_id"] != attr_id]
            result = ag.set_entity_properties(
                MODEL,
                [model_info["_id"]],
                dict(attrs=json.dumps(new_attrs)),
                {},
                [],
                False,
            )

            # 模型属性删除后，要删除对应模型实例的属性
            model_params = [{"field": "model_id", "type": "str=", "value": model_id}]
            ag.remove_entitys_properties(INSTANCE, model_params, [attr_id])

        return ModelManage.parse_attrs(result[0].get("attrs", "[]"))

    @staticmethod
    def search_model_info(model_id: str):
        """
        查询模型详情
        """
        query_data = {"field": "model_id", "type": "str=", "value": model_id}
        with Neo4jClient() as ag:
            models, _ = ag.query_entity(MODEL, [query_data])
        if len(models) == 0:
            return {}
        return models[0]

    @staticmethod
    def get_organization_option(items: list, result: list):
        for item in items:
            result.append(
                dict(
                    id=item["id"],
                    name=item["path"],
                    is_default=False,
                    type="str",
                )
            )
            if item["subGroups"]:
                ModelManage.get_organization_option(item["subGroups"], result)

    @staticmethod
    def search_model_attr(model_id: str, language: str = "en"):
        """
        查询模型属性
        """
        model_info = ModelManage.search_model_info(model_id)
        attrs = ModelManage.parse_attrs(model_info.get("attrs", "[]"))
        lan = SettingLanguage(language)
        model_attr = lan.get_val("ATTR", model_id)
        for attr in attrs:
            if model_attr:
                attr["attr_name"] = model_attr.get(attr["attr_id"]) or attr["attr_name"]
        return attrs

    @staticmethod
    def search_model_attr_v2(model_id: str):
        """
        查询模型属性
        """
        model_info = ModelManage.search_model_info(model_id)
        attrs = ModelManage.parse_attrs(model_info.get("attrs", "[]"))
        attr_types = {attr["attr_type"] for attr in attrs}

        if ORGANIZATION in attr_types:
            groups = KeyCloakClient().realm_client.get_groups({"search": ""})
            # 获取默认的第一个根组织
            groups = groups if groups else []
            option = []
            ModelManage.get_organization_option(groups, option)
            for attr in attrs:
                if attr["attr_type"] == ORGANIZATION:
                    attr.update(option=option)

        if USER in attr_types:
            users = KeyCloakClient().realm_client.get_users()
            option = [
                dict(
                    id=user["username"],
                    name=user["username"],
                    is_default=False,
                    type="str",
                )
                for user in users
            ]
            for attr in attrs:
                if attr["attr_type"] == USER:
                    attr.update(option=option)

        return attrs

    @staticmethod
    def model_association_create(**data):
        """
        创建模型关联
        """
        with Neo4jClient() as ag:
            try:
                edge = ag.create_edge(
                    MODEL_ASSOCIATION,
                    data["src_id"],
                    MODEL,
                    data["dst_id"],
                    MODEL,
                    data,
                    "model_asst_id",
                )
            except BaseAppException as e:
                if e.message == "edge already exists":
                    raise BaseAppException("model association repetition")
                else:
                    raise BaseAppException(e.message)
        return edge

    @staticmethod
    def model_association_delete(id: int):
        """
        删除模型关联
        """
        with Neo4jClient() as ag:
            ag.delete_edge(id)

    @staticmethod
    def model_association_info_search(model_asst_id: str):
        """
        查询模型关联详情
        """
        with Neo4jClient() as ag:
            query_data = {
                "field": "model_asst_id",
                "type": "str=",
                "value": model_asst_id,
            }
            edges = ag.query_edge(MODEL_ASSOCIATION, [query_data])
        if len(edges) == 0:
            return {}
        return edges[0]

    @staticmethod
    def model_association_search(model_id: str):
        """
        查询模型所有的关联
        """
        query_list = [
            {"field": "src_model_id", "type": "str=", "value": model_id},
            {"field": "dst_model_id", "type": "str=", "value": model_id},
        ]
        with Neo4jClient() as ag:
            edges = ag.query_edge(MODEL_ASSOCIATION, query_list, param_type="OR")

        return edges

    @staticmethod
    def check_model_exist_association(model_id):
        """模型存在关联关系"""
        edges = ModelManage.model_association_search(model_id)
        if edges:
            raise BaseAppException("model association exist")

    @staticmethod
    def check_model_exist_inst(model_id):
        """模型存在实例"""
        params = [{"field": "model_id", "type": "str=", "value": model_id}]
        with Neo4jClient() as ag:
            _, count = ag.query_entity(INSTANCE, params, page=dict(skip=0, limit=1))
        if count > 0:
            raise BaseAppException("model exist instance")
