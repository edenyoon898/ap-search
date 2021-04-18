from urllib.parse import urlencode, urlunparse

from ap_search.index_es.client import ElasticSearchClient
from ap_search.query_es.base import BaseQueryClient

__all__ = ("ProductQueryClient",)


class ProductQueryClient(BaseQueryClient):
    _ALIAS_NAME = "products"
    _API_ENDPOINT: str = "/search/v1/product"

    _DEFAULT_QUERY = """
        "query": {{
            "bool": {{
                {match}
            }}
        }},
        "sort": {sort}
    """

    _SEARCH_QUERY = """
        "must": [
            {{ "match": {{
                "contents": {{
                    "query": "{keyword}",
                    "operator" : "and",
                    "boost": 0
                }}
            }} }}
        ]
    """

    _DEFAULT_SORT = """[
        {{
            "_script" : {{
                "type" : "number",
                "script" : {{
                    "lang": "painless",
                    "source": "if (doc['category_no'].value == 3) {{ return 1 }} else {{ return 0 }}"
                }},
                "order" : "desc"
            }}
        }},
        {{ "product_no": "desc" }}
    ]"""

    _PRICE_DESC_SORT = """[
        {{ "price": "desc" }},
        {{ "product_no": "desc" }}
    ]"""

    _PRICE_ASC_SORT = """[
        {{ "price": "asc" }},
        {{ "product_no": "desc" }}
    ]"""

    _SORT_QUERYS = {
        "default": _DEFAULT_SORT,
        "price-asc": _PRICE_ASC_SORT,
        "price-desc": _PRICE_DESC_SORT,
    }

    def __init__(
        self,
        keyword: str = None,
        offset: int = 0,
        limit: int = 20,
        sort: str = "default",
    ):
        super(ProductQueryClient, self).__init__(
            keyword=keyword, from_=offset, size=limit
        )

        self.sort = sort

    def match_clause(self, keyword: str) -> str:
        if not keyword:
            return ""

        return self._SEARCH_QUERY.format(keyword=keyword)

    def search_with_elasticsearch(self, keyword: str) -> dict:
        match_clause = self.match_clause(keyword)
        sort_clause = self._SORT_QUERYS.get(self.sort, self._DEFAULT_SORT).format(
            keyword=keyword
        )

        query = ElasticSearchClient.QUERY_FOR_SEARCH.format(
            query=self._DEFAULT_QUERY.format(
                match=match_clause,
                sort=sort_clause,
            )
        )
        result = self.search_raw_data_with_elasticsearch(query)
        return result

    def search(self):
        result = self.search_with_elasticsearch(self.normalized_keyword)
        if not result["hits"]["hits"]:
            return self._NO_RESULT_RESPONSE

        return self.generate_data(result)

    def generate_data(self, result: dict) -> dict:
        total = result["hits"]["total"]["value"]
        data = {
            "total": total,
            "data": [self.serialize(doc["_source"]) for doc in result["hits"]["hits"]],
            "paging": {
                "next": self.get_next_url(total),
            },
        }

        return data

    @staticmethod
    def serialize(raw: dict) -> dict:
        result = {
            "product_no": raw.get("product_no"),
            "name": raw.get("name"),
            "price": raw.get("price", 0),
            "category_name": raw.get("category_name"),
            "brand_name": raw.get("brand_name"),
        }
        return result

    def get_next_url(self, total: int) -> str:
        if total <= self.from_ + self.size:
            return None

        query = {
            "limit": self.size,
            "offset": self.from_ + self.size,
            "sort": self.sort,
        }

        if self.keyword:
            query["keyword"] = self.keyword

        return urlunparse(("", "", self._API_ENDPOINT, "", urlencode(query), ""))

    def get(self, product_no: int) -> dict:
        result = ElasticSearchClient.get_client().get(self._ALIAS_NAME, product_no)
        return self.serialize(result["_source"])
