import pymysql


class MysqlClient:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(host=host, user=user, password=password, database=database,
                                          cursorclass=pymysql.cursors.DictCursor)

    def query_one(self, sql, params=None) -> dict:
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    def query_many(self, sql, size, params=None) -> dict:
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchmany(size)

    def query_all(self, sql, params=None) -> dict:
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def query_none(self, sql, params=None) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
        self.connection.commit()

    def __del__(self):
        self.connection.close()
