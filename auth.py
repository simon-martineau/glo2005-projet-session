from typing import Union
from passlib.hash import sha256_crypt
from datetime import date

from database.persistence import ApplicationDatabase
from exceptions import EmailTakenException, UsernameTakenException


class UserManager:
    def __init__(self, db: ApplicationDatabase):
        self.db = db

    def _hash_password(self, password: str):
        return sha256_crypt.hash(password)

    def _verify_password(self, password: str, hashed: str):
        return sha256_crypt.verify(password, hashed)

    def create_seller(self, email, password, name, description):
        hashed = self._hash_password(password)
        return self.db.create_seller(email, hashed, name, description)

    def create_buyer(self, email, password, first_name, last_name, username, birth_date):
        if self.db.is_email_taken(email):
            raise EmailTakenException()

        if self.db.is_buyer_username_taken(username):
            raise UsernameTakenException()

        hashed = self._hash_password(password)
        birth_date = date.fromisoformat(birth_date)
        return self.db.create_buyer(email, hashed, None, first_name, last_name, username, birth_date)

    def verify_user_credentials(self, email, password) -> Union[str, None]:
        user = self.db.get_user_by_email(email)
        if not user:
            return None
        user_id = user['user_id']
        expected = user['password']
        if not self._verify_password(password, expected):
            return None
        return user_id
