from flask import current_app
from .mysql import MysqlClient
import uuid
from datetime import date


class ApplicationDatabase:
    def __init__(self):
        self.client = MysqlClient(current_app.config['MYSQL_HOST'],
                                  current_app.config['MYSQL_USER'],
                                  current_app.config['MYSQL_PASSWORD'],
                                  current_app.config['MYSQL_DATABASE'])

    def __create_user(self, user_id: str, email_address: str, password: str, picture_url: str) -> None:
        """
        Creates a new user in the database
        :param email_address: The user's e-mail address
        :param password: The user's password
        :param picture_url: The user's picture's URL
        :return: None
        """
        sql_query = f"INSERT INTO Users (user_id, email_address, pswd, picture_url) VALUES ('{user_id}', '{email_address}', '{password}', '{picture_url}');"
        self.client.query_none(sql_query)

    def __delete_user_by_user_id(self, user_id: str) -> None:
        """
        Delets a user in the database by its user_id
        :param user_id: The user_id of the user to delete
        :return: None
        """
        user_query = f"DELETE FROM Users U WHERE U.user_id='{user_id}';"
        self.client.query_none(user_query)

    def create_buyer(self, email_address: str, password: str, picture_url: str, first_name: str, last_name: str,
                     username: str, birth_date: date) -> None:
        """
        Creates a new buyer in the database
        :param email_address: The buyer's e-mail address
        :param password: The buyer's password
        :param picture_url: The buyer's picture's URL
        :param first_name: The buyer's first name
        :param last_name: The buyer's last name
        :param username: The buyer's chosen username
        :param birth_date: The buyer's birth date
        :return: None
        """
        user_id = str(uuid.uuid4())
        formatted_date = birth_date.strftime("%Y-%m-%d")
        self.__create_user(user_id, email_address, password, picture_url)
        buyer_query = f"INSERT INTO Buyers (user_id, first_name, last_name, username, birth_date) VALUES ('{user_id}', '{first_name}', '{last_name}', '{username}', '{formatted_date}');"
        self.client.query_none(buyer_query)

    def create_seller(self, email_address: str, password: str, picture_url: str, seller_name: str,
                      seller_description: str) -> None:
        """
        Creates a new seller in the database
        :param email_address: The seller's e-mail address
        :param password: The seller's password
        :param picture_url: The seller's picture's URL
        :param seller_name: The seller's name
        :param seller_description: The seller's description
        :return: None
        """
        user_id = str(uuid.uuid4())
        self.__create_user(user_id, email_address, password, picture_url)
        seller_query = f"INSERT INTO Sellers (user_id, seller_name, seller_description) VALUES ('{user_id}', '{seller_name}', '{seller_description}');"
        self.client.query_none(seller_query)

    def get_buyer_by_username(self, username: str) -> dict:
        """
        Fetches a buyer in the database by its username
        :param username: The username to fetch
        :return: dict: The buyer's information in the database
        """
        buyer_query = f"SELECT U.*, B.first_name, B.last_name, B.birth_date FROM Users U, Buyers B WHERE U.user_id=B.user_id AND B.username='{username}';"
        return self.client.query_one(buyer_query)

    def get_buyer_by_user_id(self, user_id: str) -> dict:
        """
        Fetches a buyer in the database by its user_id
        :param user_id: The user_id of the buyer
        :return: dict: The buyer's information in the database
        """
        buyer_query = f"SELECT U.*, B.first_name, B.last_name, B.birth_date FROM Users U, Buyers B WHERE U.user_id=B.user_id AND B.user_id='{user_id}';"
        return self.client.query_one(buyer_query)

    def get_seller_by_seller_name(self, seller_name: str) -> dict:
        """
        Fetches a seller in the database by its seller_name
        :param seller_name: The seller name to fetch
        :return: dict: The seller's information in the database
        """
        seller_query = f"SELECT U.*, S.seller_name, S.seller_description FROM Users U, Sellers S WHERE U.user_id=S.user_id AND S.seller_name='{seller_name}';"
        return self.client.query_one(seller_query)

    def get_seller_by_user_id(self, user_id: str) -> dict:
        """
        Fetches a seller in the database by its user_id
        :param user_id: The user_id of the seller
        :return: dict: The seller's information in the database
        """
        seller_query = f"SELECT U.*, S.seller_name, S.seller_description FROM Users U, Sellers S WHERE U.user_id=S.user_id AND S.user_id='{user_id}';"
        return self.client.query_one(seller_query)

    def delete_buyer_by_user_id(self, user_id: str) -> None:
        """
        Deletes a buyer from the database by its user_id
        :param user_id: The user_id of the buyer to delete
        :return: None
        """
        buyer_query = f"DELETE FROM Buyers B WHERE B.user_id='{user_id}';"
        self.client.query_none(buyer_query)
        self.__delete_user_by_user_id(user_id)

    def delete_seller_by_user_id(self, user_id: str) -> None:
        """
        Deletes a seller by its user_id
        :param user_id: The user_id of the seller to delete
        :return: None
        """
        seller_query = f"DELETE FROM Sellers S WHERE S.user_id='{user_id}';"
        self.client.query_none(seller_query)
        self.__delete_user_by_user_id(user_id)

    def create_item(self, item_name: str, item_description: str, price: float, quantity: int, category: str,
                    seller_id: str) -> None:
        """
        Creates an item for sale in the database
        :param item_name: The name of the item
        :param item_description: The description of the item
        :param price: The price of the item
        :param quantity: The quantity of the item available
        :param category: The category of the item
        :param seller_id: The user_id of the seller
        :return: None
        """
        item_id = str(uuid.uuid4())
        item_query = f"INSERT INTO Items VALUES ('{item_id}', '{item_name}', '{item_description}', {price}, {quantity}, '{category}', '{seller_id}');"
        self.client.query_none(item_query)

    def get_item_by_id(self, item_id: str) -> dict:
        """
        Fetches an item by its item_id
        :param item_id: The item_i dof the item to fetch
        :return: dict: The information about the item
        """
        item_query = f"SELECT * FROM Items I WHERE I.item_id='{item_id}';"
        return self.client.query_one(item_query)

    def get_items(self, name: str = None) -> tuple:
        """
        Fetches all items whose name contains attribute name
        :param name: The name to search for in the item's name
        :return: tuple: Tuple of dict objects for each matching item
        """
        items_query = f"SELECT * FROM Items I WHERE I.item_name LIKE '%{name}%';"
        return self.client.query_all(items_query)

    def get_user_by_id(self, user_id) -> dict:
        """
        Fetched a user by its user_id
        :param user_id: The user_id of the user to fetch
        :return: dict: The information about the user
        """
        user = self.get_buyer_by_user_id(user_id)
        if not user:
            user = self.get_seller_by_user_id(user_id)
        return user

    def get_user_by_email(self, email: str) -> dict:
        """
        Fetches a user by its e-mail address
        :param email: The e-mail address of the user to fetch
        :return: dict: The information about the user
        """
        user_query = f"SELECT Users.user_id FROM Users WHERE Users.email_address='{email}';"
        user_id = self.client.query_one(user_query)['user_id']
        return self.get_user_by_id(user_id)
