import pymysql


class MysqlClient:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(host=host, user=user, password=password, database=database,
                                          cursorclass=pymysql.cursors.DictCursor)

    def query(self, sql, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params=None)
