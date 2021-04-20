from database.mysql import MysqlClient
from conf import BasicConfig
import names
import itertools
import uuid
import random
import datetime

ENCRYPTED_PASSWORD = "$5$rounds=535000$7/J2PCRN7CEXcC5/$prCsIeitr4L6jkEs/xNswqg8oVEHmJn9tYVYlVXT.DA"


def populate() -> None:
    """
    Populates the database with random data
    :return:
    """
    client = MysqlClient(
        BasicConfig.MYSQL_HOST,
        BasicConfig.MYSQL_USER,
        BasicConfig.MYSQL_PASSWORD,
        BasicConfig.MYSQL_DATABASE
    )
    # Categories
    nb_of_categories = 6
    categorie_ids = [1, 2, 3, 4, 5, 6]
    categories_names = ["Food", "Electronics", "Furniture", "Health", "Automotive", "Other"]

    # Users
    nb_of_users = 200
    users_ids = [str(uuid.uuid4()) for _ in range(nb_of_users)]
    users_emails = [str(x) + "@email.com" for x in range(nb_of_users)]
    users_passwords = [ENCRYPTED_PASSWORD for _ in range(nb_of_users)]

    # Buyers
    nb_of_buyers = 100
    buyers_user_ids = users_ids[0:100]
    buyers_first_names = [names.get_first_name() for _ in range(nb_of_buyers)]
    buyers_last_names = [names.get_last_name() for _ in range(nb_of_buyers)]
    buyers_usernames = [buyers_first_names[x][:4] + buyers_last_names[x][:4] for x in range(nb_of_buyers)]
    start_date = datetime.date(1971, 1, 1)
    buyers_birth_dates = [(start_date + datetime.timedelta(days=random.randint(1, 9000))).strftime("%Y-%m-%d") for _ in
                          range(nb_of_buyers)]

    # Sellers
    nb_of_sellers = 100
    sellers_user_ids = users_ids[101:]
    sellers_first_names = [names.get_first_name() for _ in range(10)]
    sellers_last_names = ["store", "boutique", "market", "company", "items", "variety", "selection", "shop",
                          "treasures", "picks"]
    sellers_names = ["'s ".join(x) for x in list(itertools.product(sellers_first_names, sellers_last_names))]
    sellers_descriptions = [f"Find everything at {x}!" for x in sellers_names]

    # Items
    colors = ["Red", "Orange", "Yellow", "Lime green", "Green", "Teal", "Blue", "Purple", "Pink", "White", "Black"]
    products = ["chair", "dining table", "couch", "pillow", "coffee table", "bookshelf", "ottoman", "desk", "rug",
                "bedsheet set"]
    nb_of_items = len(colors) * len(products)
    item_ids = [str(uuid.uuid4()) for _ in range(nb_of_items)]
    items_names = [" ".join(x) for x in list(itertools.product(colors, products))]
    items_descriptions = [" ".join(["A beautiful", x, "that fits all your needs!"]) for x in items_names]
    items_prices = [round(random.uniform(15.0, 65.0), 2) for _ in range(nb_of_items)]
    items_quantity = [random.randint(5, 20) for _ in range(nb_of_items)]
    items_categories = ["Furniture" for _ in range(nb_of_items)]
    items_seller_ids = sellers_user_ids

    # Comments
    nb_of_comments = 100
    adverbs = ["Really", "Not really", "Very", "Not very", "Immensely", "Not immensely", "Intensely", "Not intensely",
               "Humongously", "Not humongously"]
    adjectives = ["good", "bad", "convenient", "useful", "futile", "useless", "lovely", "cool", "nice", "awesome"]
    comment_ids = [str(uuid.uuid4()) for _ in range(nb_of_comments)]
    comments_content = [" ".join(x) for x in list(itertools.product(adverbs, adjectives))]
    comments_ratings = [random.randint(1, 5) for _ in range(nb_of_comments)]

    # Transactions
    nb_of_transaction = 100
    transaction_ids = [str(uuid.uuid4()) for _ in range(nb_of_transaction)]
    transactions_quantities = [random.randint(1, 2) for _ in range(nb_of_transaction)]

    # Populating Categories
    for i in range(nb_of_categories):
        categories_query = f"INSERT INTO Categories (category_id, name) VALUES ('{categorie_ids[i]}', '{categories_names[i]}');"
        client.query_none(categories_query)

    # Populating Users
    for i in range(nb_of_users):
        items_query = f"INSERT INTO Users (user_id, email, password) VALUES ('{users_ids[i]}', '{users_emails[i]}', '{users_passwords[i]}');"
        client.query_none(items_query)

    # Populating Buyers
    for i in range(nb_of_buyers):
        buyers_query = f"INSERT INTO Buyers (user_id, first_name, last_name, username, birth_date) VALUES ('{users_ids[i]}', '{buyers_first_names[i]}', '{buyers_last_names[i]}', '{buyers_usernames[i]}', '{buyers_birth_dates[i]}');"
        client.query_none(buyers_query)

    # Populating Sellers
    for i in range(nb_of_sellers):
        sellers_query = f"INSERT INTO Sellers (user_id, name, description) VALUES ('{users_ids[i + 100]}', '{sellers_names[i]}', '{sellers_descriptions[i]}');"
        client.query_none(sellers_query)

    # Populating Items
    for i in range(nb_of_items):
        items_query = f"INSERT INTO Items (item_id, name, description, price, quantity, category_id, seller_id) VALUES ('{item_ids[i]}', '{items_names[i]}', '{items_descriptions[i]}', {items_prices[i]}, {items_quantity[i]}, '{sellers_user_ids[i]}');"
        client.query_none(items_query)

    # Populating Comments
    for i in range(nb_of_comments):
        comments_query = f"INSERT INTO Comments (comment_id, buyer_id, item_id, content, rating) VALUES ('{comment_ids[i]}', '{buyers_user_ids[i]}', '{item_ids[i]}', '{comments_content[i]}', {comments_ratings[i]});"
        client.query_none(comments_query)

    # Populating Transactions
    for i in range(nb_of_transaction):
        transactions_query = f"INSERT INTO Transactions (transaction_id, buyer_id, seller_id, item_id, price, quantity) VALUES ('{transaction_ids[i]}', '{buyers_user_ids[i]}', '{sellers_user_ids[i]}', '{item_ids[i]}', {items_prices[i]}, {transactions_quantities[i]});"


if __name__ == '__main__':
    populate()
