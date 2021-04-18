import redis
from flask import Flask, request

from ap_search.query_es.product import ProductQueryClient

app = Flask(__name__)
cache = redis.Redis(host="ap-redis", port=6379)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/search/v1/product")
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
def search_v1_product_get(product_no: int):
    result = ProductQueryClient().get(product_no)
    return result
