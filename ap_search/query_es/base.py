from abc import ABCMeta, abstractmethod

from ap_search.index_es.client import ElasticSearchClient

__all__ = "BaseQueryClient"


class BaseQueryClient(metaclass=ABCMeta):
    _DEFAULT_FROM: int = 0
    _DEFAULT_SIZE: int = 20

    _NO_RESULT_RESPONSE = {
        "total": 0,
        "data": [],
        "paging": {
            "next": None,
        },
    }

    def __init__(
        self,
        keyword: str = "",
        from_: int = _DEFAULT_FROM,
        size: int = _DEFAULT_SIZE,
    ):
        self.keyword = keyword if keyword else ""
        self.from_ = from_
        self.size = size

    @property
    def normalized_keyword(self) -> str:
        return ElasticSearchClient.normalize_keyword(self.keyword)

    def search_raw_data_with_elasticsearch(self, query: str, **kwargs) -> dict:
        if "size" not in kwargs:
            kwargs["size"] = self.size
        if "from_" not in kwargs:
            kwargs["from_"] = self.from_

        result = ElasticSearchClient.search(
            index=self._ALIAS_NAME,
            body=query,
            **kwargs,
        )
        return result

    @abstractmethod
    def search(self) -> dict:
        pass
