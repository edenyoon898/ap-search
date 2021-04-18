from datetime import datetime

from ap_search.index_es import ProductIndexClient
from ap_search.rdb.connection import ConnectionRDB
from ap_search.rdb.product import ProductRDB


def update_products():
    chunk_size = 100
    max_no = ProductRDB.get_max_no()

    index_name = ProductIndexClient.create_new_index()
    ProductIndexClient.prevent_index_refresh(index_name)

    for offset in range(0, max_no + 1, chunk_size):
        products = ProductRDB.get_data_with_range(
            offset,
            offset + chunk_size,
        )
        ProductIndexClient.bulk_upsert(products, index_name)

    ProductIndexClient.allow_index_refresh(index_name)
    ProductIndexClient.update_alias(index_name)

    ConnectionRDB().close()


if __name__ == "__main__":
    start_time = datetime.now()
    print(
        "Bulk Upsert started at {0}.".format(start_time.strftime("%Y-%m-%d %H:%M:%S"))
    )

    update_products()

    finish_time = datetime.now()
    print(
        "Bulk Upsert finished at {0}.".format(finish_time.strftime("%Y-%m-%d %H:%M:%S"))
    )
    print("Excution time: {0}s".format(finish_time - start_time))
