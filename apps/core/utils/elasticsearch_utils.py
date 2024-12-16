from django.conf import settings
from elasticsearch import Elasticsearch


def get_es_client():
    return Elasticsearch(hosts=[settings.ELASTICSEARCH_URL], http_auth=("elastic", settings.ELASTICSEARCH_PASSWORD))
