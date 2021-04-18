import json
from typing import List

from ap_search.rdb.connection import ConnectionRDB
from ap_search.util import DocInfo

__all__ = ("ProductRDB",)


class ProductRDB:
    BATCH_SIZE = 100

    TABLE_NAME = "product"

    QUERY_MAX_NO = "SELECT max(product_no) FROM product"

    QUERY_FOR_ES = """
        SELECT product_no, product_name, product_price, brand_name, category_name, category.category_no
        FROM product
        JOIN category on product.category_no = category.category_no
        WHERE product_no >= {start_no} AND product_no < {end_no}
    """

    @classmethod
    def get_max_no(cls) -> int:
        connection = ConnectionRDB().get_connection()
        with connection.cursor() as cursor:
            cursor.execute(cls.QUERY_MAX_NO)
            return cursor.fetchone()[0]

    @classmethod
    def get_data_with_range(cls, start_no: int, end_no: int) -> List[DocInfo]:
        data = list()
        connection = ConnectionRDB().get_connection()
        with connection.cursor() as cursor:
            cursor.execute(cls.get_query_with_range(start_no, end_no))
            for record in cursor:
                data.append(cls.get_datum(record))

        return data

    @classmethod
    def get_query_with_range(cls, start_no: int, end_no: int) -> str:
        return cls.QUERY_FOR_ES.format(start_no=start_no, end_no=end_no)

    @classmethod
    def get_datum(cls, record: tuple) -> DocInfo:
        data = {
            "product_no": record[0],
            "name": record[1],
            "price": float(record[2] or 0),
            "brand_name": record[3],
            "category_name": record[4],
            "category_no": record[5],
        }

        return DocInfo(record[0], json.dumps(data))
