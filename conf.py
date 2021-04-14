import os


class BasicConfig:
    SQL_BASEDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sql')
    MYSQL_HOST = ""
    MYSQL_USER = ""
    MYSQL_PASSWORD = ""
    MYSQL_DATABASE = ""
