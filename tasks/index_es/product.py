from tasks.index_es.base import BaseIndexClient

__all__ = "ProductElasticsearchClient"


class ProductIndexClient(BaseIndexClient):
    _ALIAS_NAME = "products"

    _MAPPINGS = """"properties": {
        "product_no": {
            "type": "long",
            "index": "false"
        },
        "name": {
            "type": "text",
            "analyzer": "korean",
            "search_analyzer": "korean_search",
            "copy_to": ["contents"]
        },
        "brand_name": {
            "type": "keyword",
            "copy_to": ["contents"]
        },
        "category_name": {
            "type": "keyword",
            "copy_to": ["contents"]
        },
        "category_no": {
            "type": "long"
        },
        "price": {
            "type": "double"
        },
        "contents": {
            "type": "text",
            "analyzer": "korean",
            "search_analyzer": "korean_search"
        }
    }"""
