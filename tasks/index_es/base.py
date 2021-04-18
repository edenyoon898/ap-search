from abc import ABCMeta
from datetime import datetime
from typing import List

from elasticsearch import NotFoundError

from common.es.client import ElasticSearchClient
from common.util import KST, DocInfo

__all__ = ("BaseIndexClient",)


class BaseIndexClient(metaclass=ABCMeta):
    _ALIAS_NAME = None
    _MAPPINGS = None

    _SETTINGS = """"index": {
        "number_of_shards" : 1,
        "number_of_replicas" : 1,
        "max_result_window" : "100000",
        "analysis": {
            "analyzer": {
                "korean": {
                    "type": "custom",
                    "tokenizer": "nori_user_dict",
                    "filter": ["lowercase", "synonym"]
                },
                "korean_search": {
                    "type": "custom",
                    "tokenizer": "nori_user_dict",
                    "filter": ["lowercase"]
                }
            },
            "tokenizer": {
                "nori_user_dict": {
                    "type": "nori_tokenizer",
                    "decompound_mode": "discard",
                    "user_dictionary": "user_dict.txt"
                }
            },
            "filter": {
                "synonym": {
                    "type": "synonym_graph",
                    "synonyms_path": "synonyms.txt"
                }
            }
        }
    }"""

    @classmethod
    def bulk_upsert(
        cls, doc_infos: List[DocInfo], index_name: str = _ALIAS_NAME
    ) -> dict:
        meta_data = ElasticSearchClient.UPDATE_META_DATA
        update_doc = ElasticSearchClient.UPDATE_DOC

        limit = 1000
        for offset in range(0, len(doc_infos), limit):
            body = ""
            for doc_info in doc_infos[offset : offset + limit]:
                body += meta_data.format(index=index_name, id=doc_info.id) + "\n"
                body += update_doc.format(doc=doc_info.json) + "\n"

            if body:
                return ElasticSearchClient.bulk(body=body)

    @classmethod
    def allow_index_refresh(cls, index_name: str = _ALIAS_NAME) -> None:
        try:
            ElasticSearchClient.get_client().indices.put_settings(
                index=index_name, body='{ "refresh_interval": "1s" }'
            )
        except NotFoundError:
            pass

    @classmethod
    def prevent_index_refresh(cls, index_name: str = _ALIAS_NAME) -> None:
        try:
            ElasticSearchClient.get_client().indices.put_settings(
                index=index_name, body='{ "refresh_interval": "-1" }'
            )
        except NotFoundError:
            pass

    @classmethod
    def create_index(cls, index_name: str, settings: dict, mappings: dict) -> None:
        ElasticSearchClient.get_client().indices.create(
            index=index_name,
            body=ElasticSearchClient.DEFAULT_INDEX_BODY.format(
                settings=settings, mappings=mappings
            ),
        )

    @classmethod
    def get_new_index_name(cls, alias_name: str) -> str:
        index_name = "{0}_{1}_{2}".format(
            alias_name,
            datetime.now(KST).strftime("%Y-%m-%d_%H%M%S"),
            KST.zone.replace("/", "_").lower(),
        )
        return index_name

    @classmethod
    def create_new_index(cls) -> str:
        index_name = cls.get_new_index_name(cls._ALIAS_NAME)
        cls.create_index(index_name, cls._SETTINGS, cls._MAPPINGS)
        return index_name

    @classmethod
    def finalize_bulk_upload(
        cls, index_name: str, alias_name: str, delete_old_index: bool = False
    ) -> None:
        ElasticSearchClient.allow_index_refresh(index_name)
        cls.update_alias(alias_name, index_name, delete_old_index)

    @classmethod
    def update_alias(cls, index_name: str, delete_old_index: bool = False) -> None:
        es_client = ElasticSearchClient.get_client()
        try:
            indices = es_client.indices.get_alias(name=cls._ALIAS_NAME).keys()
        except NotFoundError:
            indices = []

        es_client.indices.put_alias(index=index_name, name=cls._ALIAS_NAME)

        for index in indices:
            es_client.indices.delete_alias(index=index, name=cls._ALIAS_NAME)

            if delete_old_index:
                es_client.indices.delete(index=index)
