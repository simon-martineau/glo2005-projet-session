from flask import current_app
from .mysql import MysqlClient
from .sqlloader import SqlLoader


class ApplicationDatabase:
    def __init__(self):

        self.client = MysqlClient(current_app.config['MYSQL_HOST'],
                                  current_app.config['MYSQL_USER'],
                                  current_app.config['MYSQL_PASSWORD'],
                                  current_app.config['MYSQL_DATABASE'])

        self.loader = SqlLoader()

    def _get_user_by_id(self, identifier: str):  # TODO: Mettre les return types, parce que c'est pas toujours évident (je sais pas encore ça retourne quoi exactement)
        query = f"""SELECT * FROM users u WHERE u.user_id = '{identifier}'"""
        result = self.client.query(query)
        return result

    def get_buyer_by_id(self, identifier):
        pass

    def get_seller_by_id(self, identifier):
        pass

