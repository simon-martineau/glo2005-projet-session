import os
import unittest
import conf
from .sqlloader import SqlLoader


class SqlloaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sql_dir = conf.BasicConfig.SQL_BASEDIR
        self.loader = SqlLoader()

        with open(os.path.join(self.sql_dir, 'test_query.sql'), 'w+') as f:
            f.write('test data')

    def test_sql_loader_known_query(self):
        content = self.loader.load('test_query')
        self.assertEqual(content, 'test data')

    def tearDown(self):
        os.remove(os.path.join(self.sql_dir, 'test_query.sql'))
