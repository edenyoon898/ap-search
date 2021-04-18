import os
import re

from elasticsearch import Elasticsearch, NotFoundError

__all__ = ("ElasticSearchClient",)


class ElasticSearchClient(object):
    _ES_HOST = os.environ.get("ELASTICSEARCH_ENDPOINT")
    _MAX_KEYWORD_LENGTH = 30
    _DEFAULT_SIZE = 20
    _ES_CLIENT = None

    DEFAULT_INDEX_BODY = """{{
        "settings": {{
            {settings}
        }},
        "mappings": {{
            {mappings}
        }}
    }}"""

    UPDATE_META_DATA = (
        '{{ "update" : {{ "_index" : "{index}", '
        '"_id" : "{id}", "retry_on_conflict" : 3 }} }}'
    )
    UPDATE_DOC = '{{ "doc" : {doc}, "doc_as_upsert" : true }}'

    QUERY_FOR_SEARCH = """{{
        "track_total_hits": true,
        {query}
    }}"""

    @classmethod
    def get_client(cls, timeout: int = 60) -> Elasticsearch:
        if not cls._ES_CLIENT:
            cls._ES_CLIENT = Elasticsearch(cls._ES_HOST, timeout=timeout)
        return cls._ES_CLIENT

    @classmethod
    def normalize_keyword(cls, keyword: str) -> str:
        if not keyword:
            return ""

        keyword_removed_symbol = re.sub(
            r"[\x00-\x1F\x7F\s']+", " ", keyword, flags=re.UNICODE
        )
        keyword_escaped_double_quote = re.sub(
            r"([\\\"])", r"\\\1", keyword_removed_symbol, flags=re.UNICODE
        )
        keyword_truncated = keyword_escaped_double_quote.strip()[
            : cls._MAX_KEYWORD_LENGTH
        ]
        keyword_trimed_backshlash = keyword_truncated.rstrip("\\")
        return keyword_trimed_backshlash.lower()

    @classmethod
    def bulk(cls, **kwargs) -> dict:
        return cls.get_client().bulk(**kwargs)

    @classmethod
    def search(cls, stored_fields=None, size=_DEFAULT_SIZE, **kwargs) -> dict:
        if isinstance(stored_fields, list):
            kwargs.update(stored_fields=stored_fields)
        kwargs.update(size=size)
        try:
            res = cls.get_client().search(**kwargs)
        except NotFoundError:
            return None
        else:
            return res

    @classmethod
    def get(cls, index, object_id) -> dict:
        try:
            return cls.get_client().get(index=index, id=object_id)
        except NotFoundError:
            return None
