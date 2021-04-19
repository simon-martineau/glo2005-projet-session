import os


class BasicConfig:
    SQL_BASEDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sql')
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = "projetsession"
