import os

from conf import BasicConfig


class SqlLoader:
    def __init__(self):
        self.sql_dir = BasicConfig.SQL_BASEDIR

    def load(self, name: str):
        with open(os.path.join(self.sql_dir, name + '.sql')) as f:
            content = f.read()
        return content
