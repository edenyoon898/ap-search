import os

import pymysql

__all__ = ("ConnectionRDB",)


class ConnectionRDB:
    CONNECTION = None

    def __init__(self):
        self.MYSQL_ENDPOINT = os.environ.get("MYSQL_ENDPOINT")
        self.MYSQL_PORT = 3306
        self.MYSQL_USER = os.environ.get("MYSQL_USER")
        self.MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
        self.MYSQL_SCHEMA = "ap"

    def get_connection(self):
        if not self.CONNECTION or self.CONNECTION._closed:
            self.connect()

        return self.CONNECTION

    def connect(self):
        self.CONNECTION = pymysql.connect(
            host=self.MYSQL_ENDPOINT,
            port=self.MYSQL_PORT,
            user=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            db=self.MYSQL_SCHEMA,
            charset="utf8",
            autocommit=True,
        )

    def close(self):
        if self.CONNECTION:
            if not self.CONNECTION._closed:
                self.CONNECTION.close()
            self.CONNECTION = None
