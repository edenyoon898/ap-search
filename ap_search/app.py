from flask import Flask, request
from flask_caching import Cache

from ap_search.query_es.product import ProductQueryClient

app = Flask(__name__)
cache = Cache(app, config={
    'CACHE_TYPE': 'RedisCache', 'CACHE_REDIS_URL': 'redis://ap-redis:6379/0'
})


@app.route("/")
@cache.cached(timeout=300)
def hello():
    return "Hello World!"


@app.route("/search/v1/product")
@cache.cached(timeout=30, query_string=True)
def search_v1_product():
    keyword = request.args.get("keyword", type=str)
    offset = request.args.get("offset", 0, type=int)
    limit = request.args.get("limit", 20, type=int)
    sort = request.args.get("sort", "default", type=str)

    result = ProductQueryClient(
        keyword=keyword, offset=offset, limit=limit, sort=sort
    ).search()

    return result


@app.route("/search/v1/product/<int:product_no>")
@cache.cached(timeout=30, query_string=True)
def search_v1_product_get(product_no: int):
    result = ProductQueryClient().get(product_no)
    return result
