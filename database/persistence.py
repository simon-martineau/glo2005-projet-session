from flask import current_app
from .mysql import MysqlClient
from pymysql.err import MySQLError
import uuid
from datetime import date
from exceptions import InvalidQuantity, InvalidAge


class ApplicationDatabase:
    def __init__(self):
        self.client = MysqlClient(current_app.config['MYSQL_HOST'],
                                  current_app.config['MYSQL_USER'],
                                  current_app.config['MYSQL_PASSWORD'],
                                  current_app.config['MYSQL_DATABASE'])

    def __create_user(self, user_id: str, email_address: str, password: str) -> None:
        """
        Creates a new user in the database
        :param email_address: The user's e-mail address
        :param password: The user's password
        :return: None
        """
        sql_query = f"INSERT INTO Users (user_id, email, password) VALUES ('{user_id}', '{email_address}', '{password}');"
        self.client.query_none(sql_query)

    def is_buyer_username_taken(self, username: str) -> bool:
        query = f"""SELECT COUNT(*) as count FROM buyers b WHERE b.username = '{username}'"""
        result = self.client.query_one(query)
        return int(result['count']) != 0

    def is_email_taken(self, email: str) -> bool:
        query = f"""SELECT COUNT(*) as count FROM users u WHERE u.email = '{email}'"""
        result = self.client.query_one(query)
        return int(result['count']) != 0

    def is_seller_name_taken(self, name: str) -> bool:
        query = f"""SELECT COUNT(*) as count FROM sellers s WHERE s.name = '{name}'"""
        result = self.client.query_one(query)
        return int(result['count']) != 0

    def __delete_user_by_user_id(self, user_id: str) -> None:
        """
        Delets a user in the database by its user_id
        :param user_id: The user_id of the user to delete
        :return: None
        """
        user_query = f"DELETE FROM Users U WHERE U.user_id='{user_id}';"
        self.client.query_none(user_query)

    def create_buyer(self, email_address: str, password: str, first_name: str, last_name: str,
                     username: str, birth_date: date) -> None:
        """
        Creates a new buyer in the database
        :param email_address: The buyer's e-mail address
        :param password: The buyer's password
        :param first_name: The buyer's first name
        :param last_name: The buyer's last name
        :param username: The buyer's chosen username
        :param birth_date: The buyer's birth date
        :return: None
        """
        user_id = str(uuid.uuid4())
        formatted_date = birth_date.strftime("%Y-%m-%d")
        with self.client.connection.cursor() as cursor:
            self.client.connection.begin()
            user_query = f"INSERT INTO Users (user_id, email, password) VALUES ('{user_id}', '{email_address}', '{password}');"
            cursor.execute(user_query)
            buyer_query = f"INSERT INTO Buyers (user_id, first_name, last_name, username, birth_date) VALUES ('{user_id}', '{first_name}', '{last_name}', '{username}', '{formatted_date}');"
            try:
                cursor.execute(buyer_query)
            except MySQLError:
                self.client.connection.rollback()
                raise InvalidAge
        self.client.connection.commit()

    def create_seller(self, email_address: str, password: str, name: str,
                      description: str) -> None:
        """
        Creates a new seller in the database
        :param email_address: The seller's e-mail address
        :param password: The seller's password
        :param name: The seller's name
        :param description: The seller's description
        :return: None
        """
        user_id = str(uuid.uuid4())
        self.__create_user(user_id, email_address, password)
        seller_query = f"INSERT INTO Sellers (user_id, name, description) VALUES ('{user_id}', '{name}', '{description}');"
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
        buyer_query = f"SELECT U.*, B.first_name, B.last_name, B.birth_date, B.username FROM Users U, Buyers B WHERE U.user_id=B.user_id AND B.user_id='{user_id}';"
        return self.client.query_one(buyer_query)

    def get_seller_by_seller_name(self, seller_name: str) -> dict:
        """
        Fetches a seller in the database by its seller_name
        :param seller_name: The seller name to fetch
        :return: dict: The seller's information in the database
        """
        seller_query = f"SELECT U.*, S.name, S.description FROM Users U, Sellers S WHERE U.user_id=S.user_id AND S.name='{seller_name}';"
        return self.client.query_one(seller_query)

    def get_seller_by_user_id(self, user_id: str) -> dict:
        """
        Fetches a seller in the database by its user_id
        :param user_id: The user_id of the seller
        :return: dict: The seller's information in the database
        """
        seller_query = f"SELECT U.*, S.name, S.description FROM Users U, Sellers S WHERE U.user_id=S.user_id AND S.user_id='{user_id}';"
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

    def create_item(self, item_name: str, item_description: str, price: float, quantity: int, category_id: int,
                    seller_id: str) -> None:
        item_id = str(uuid.uuid4())
        item_query = f"""
        INSERT INTO items (item_id, name, description, price, quantity, category_id, seller_id)
            VALUES ('{item_id}', '{item_name}', '{item_description}', {price}, {quantity}, {category_id}, '{seller_id}');
        """
        self.client.query_none(item_query)

    def get_item_by_id(self, item_id: str) -> dict:
        """
        Fetches an item by its item_id
        :param item_id: The item_i dof the item to fetch
        :return: dict: The information about the item
        """
        item_query = f"""
        SELECT I.*, S.name AS seller_name, C.name as category FROM Sellers S
            INNER JOIN Items I on I.seller_id = s.user_id
            INNER JOIN categories C on I.category_id = C.category_id WHERE I.item_id='{item_id}';
            
        """
        return self.client.query_one(item_query)

    def get_items(self, name: str = None) -> tuple:
        """
        Fetches all items whose name contains attribute name
        :param name: The name to search for in the item's name
        :return: tuple: Tuple of dict objects for each matching item
        """
        if not name:
            name = ""
        items_query = f"SELECT I.*, c.name as category FROM Items I Left JOIN categories c on I.category_id = c.category_id WHERE I.name LIKE '%{name}%'"
        items_result = self.client.query_all(items_query)
        return items_result

    def get_items_by_seller_id(self, seller_id):
        query = f"SELECT i.*, c.name as category FROM items i LEFT JOIN categories c on i.category_id = c.category_id WHERE seller_id = '{seller_id}'"
        return self.client.query_all(query)

    def get_item_by_id_and_seller_id(self, item_id, seller_id):
        query = f"SELECT i.*, c.name as category FROM items i LEFT JOIN categories c on i.category_id = c.category_id WHERE item_id = '{item_id}' AND seller_id = '{seller_id}'"
        return self.client.query_one(query)

    def update_item(self, item_id, name, description, price, quantity, category_id):
        query = f"""
        UPDATE items SET 
            name = '{name}',
            description = '{description}',
            price = '{price}',
            quantity = '{quantity}',
            category_id = {category_id}
        WHERE item_id = '{item_id}';
        """
        self.client.query_none(query)

    def get_categories(self):
        query = "SELECT * FROM categories"
        return self.client.query_all(query)

    def get_user_by_id(self, user_id) -> dict:
        """
        Fetched a user by its user_id
        :param user_id: The user_id of the user to fetch
        :return: dict: The information about the user
        """
        user_type = 'buyer'
        user = self.get_buyer_by_user_id(user_id)
        if not user:
            user_type = 'seller'
            user = self.get_seller_by_user_id(user_id)
        if user:
            user['type'] = user_type
        return user

    def get_user_by_email(self, email: str) -> dict:
        """
        Fetches a user by its e-mail address
        :param email: The e-mail address of the user to fetch
        :return: dict: The information about the user
        """
        user_query = f"SELECT Users.user_id FROM Users WHERE Users.email='{email}';"
        user_id = self.client.query_one(user_query)['user_id']
        return self.get_user_by_id(user_id)

    def get_comments_by_item_id(self, item_id: str) -> tuple:
        """
        Fetches comments for an item by its item_id
        :param item_id: The item_id of the item
        :return: tuple: Tuple of dict objects for each comment
        """
        comments_query = f"SELECT B.username, C.* FROM Buyers B INNER JOIN Comments C ON B.user_id = C.buyer_id WHERE C.item_id='{item_id}' ORDER BY c.created DESC;"
        return self.client.query_all(comments_query)

    def get_comments_by_buyer_id(self, buyer_id: str) -> tuple:
        """
        Fetches comments made by a particular buyer by its buyer_id
        :param buyer_id: The buyer_id of the buyer
        :return: tuple: TUple of dict objects for each comment
        """
        comments_query = f"SELECT * FROM Comments C WHERE C.buyer_id='{buyer_id}';"
        return self.client.query_all(comments_query)

    def create_comment(self, buyer_id: str, item_id: str, comment_content: str, rating: int) -> None:
        """
        Creates a comment in the database
        :param buyer_id: The ID of the buyer who is commenting
        :param item_id: The ID of the item to comment on
        :param comment_content: THe content of the comment
        :param rating: The rating given to the item
        :return: None
        """
        comment_id = str(uuid.uuid4())
        comment_query = f"INSERT INTO Comments (comment_id, buyer_id, item_id, content) VALUES ('{comment_id}', '{buyer_id}', '{item_id}', '{comment_content}');"
        self.client.query_none(comment_query)

    def get_transactions_by_buyer_id(self, buyer_id):
        query = f"""SELECT t.*, s.name as seller_name, i.name as item_name
        FROM transactions t 
            INNER JOIN sellers s on t.seller_id = s.user_id
            INNER JOIN items i on t.item_id = i.item_id
        WHERE t.buyer_id = '{buyer_id}'
        ORDER BY t.timestamp DESC
        """
        return self.client.query_all(query)

    def get_transactions_by_seller_id(self, seller_id):
        query = f"""SELECT t.*, b.username as buyer_username, i.name as item_name
        FROM transactions t 
            INNER JOIN buyers b on t.buyer_id = b.user_id
            INNER JOIN items i on t.item_id = i.item_id
        WHERE t.seller_id = '{seller_id}'
        ORDER BY t.timestamp DESC
        """
        return self.client.query_all(query)

    def create_transaction(self, buyer_id, seller_id, item_id, price, quantity):
        transaction_id = uuid.uuid4()
        query = f"""
        INSERT INTO transactions (transaction_id, buyer_id, seller_id, item_id, price, quantity)
        VALUES ('{transaction_id}', '{buyer_id}', '{seller_id}', '{item_id}', {price}, {quantity})
        """
        try:
            self.client.query_none(query)
        except MySQLError:
            raise InvalidQuantity
