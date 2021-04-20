from conf import BasicConfig
from flask import Flask, render_template, request, make_response, redirect, abort
from database.persistence import ApplicationDatabase
from sessions import SessionManager
from auth import UserManager
from middleware import AuthenticationMiddleware
from exceptions import UsernameTakenException, EmailTakenException, SellerNameTaken

app = Flask(__name__)
app.config.from_object(BasicConfig)

with app.app_context():
    db = ApplicationDatabase()
user_manager = UserManager(db)
session_manager = SessionManager()
app.wsgi_app = AuthenticationMiddleware(app.wsgi_app, db, session_manager)

fake_items = [
    {
        "id": '1092384750928734',
        "name": "item1",
        "description": "item1 description asdf asdf asdf asdf asdf ",
        "price": 3.99,
        "tags": ["Very noice", "Hekkin chonker"],
        "quantity": 4,
        "seller_name": "bob marley",
        "comments": [
            {
                "username": "simon",
                "content": "very noice item that is",
                "timestamp": "2020-04-05"
            },
            {
                "username": "alex",
                "content": "dis is a very nice nice",
                "timestamp": "2020-04-06"
            }
        ]
    },
    {
        "id": '10923843453456456',
        "name": "item2",
        "description": "item2 description qwer qwer qwer qwer qwer ",
        "price": 113.99,
        "tags": ["Quite noice", "Mega chonker"],
        "quantity": 6,
        "seller_name": "bober",
        "comments": []
    }
]


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = []
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_id = user_manager.verify_user_credentials(email, password)

        if user_id:
            session_id = session_manager.create_session(user_id)
            redirect_url = request.args.get('next')
            if not redirect_url:
                redirect_url = '/'
            res = make_response(redirect(redirect_url))
            res.set_cookie('sessionID', session_id)
            return res
        else:
            errors.append('Invalid username and password combination')

    return render_template('login.html', errors=errors)


@app.route('/logout')
def logout():
    session_id = request.cookies.get('sessionID')
    if session_id:
        session_manager.delete_session(session_id)
        res = make_response(redirect('/'))
        res.delete_cookie('sessionID')
        return res
    else:
        return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')


@app.route('/signup/buyer', methods=['GET', 'POST'])
def buyer_signup():
    errors = []
    if request.method == 'POST':
        form = request.form
        email = form['email']
        username = form['username']
        first_name = form['first_name']
        last_name = form['last_name']
        birth_date = form['birth_date']
        password = form['password']

        try:
            user_manager.create_buyer(email, password, first_name, last_name, username, birth_date)
            return redirect('/login')
        except UsernameTakenException as e:
            errors.append("Username is already taken")
        except EmailTakenException as e:
            errors.append("Email is already taken")

    return render_template('buyer_signup.html', errors=errors)


@app.route('/signup/seller', methods=['GET', 'POST'])
def seller_signup():
    errors = []
    if request.method == 'POST':
        form = request.form
        email = form['email']
        name = form['name']
        description = form['description']
        password = form['password']

        try:
            user_manager.create_seller(email, password, name, description)
            return redirect('/login')
        except SellerNameTaken as e:
            errors.append("This seller already exists")
        except EmailTakenException as e:
            errors.append("Email is already taken")

    return render_template('seller_signup.html', errors=errors)


@app.route('/items')
def items():
    req_items = db.get_items(name=request.args.get('search'))

    return render_template('items.html', items=req_items)


@app.route('/items/<item_id>', methods=['GET', 'POST'])
def item(item_id):
    if request.method == 'POST':
        comment = request.form['comment']
        if comment:
            user = request.environ['user']
            if user['type'] == 'buyer':
                db.create_comment(user['user_id'], item_id, comment, 0)

    requested_item = db.get_item_by_id(item_id)
    comments = db.get_comments_by_item_id(item_id)
    return render_template('item.html', item=requested_item, comments=comments)


@app.route('/items/<item_id>/buy', methods=['GET', 'POST'])
def buy_item(item_id):
    requested_item = next(x for x in fake_items if x['id'] == item_id)
    return render_template('buy_item.html', item=requested_item)


@app.route('/account')
def account():
    if not request.environ['user']:
        return redirect('/login?next=/account')
    else:
        user = request.environ['user']
        if user['type'] == 'seller':
            transactions = db.get_transactions_by_seller_id(user['user_id'])
            return render_template('seller_account.html', seller=user, transactions=transactions)
        else:
            transactions = db.get_transactions_by_buyer_id(user['user_id'])
            return render_template('buyer_account.html', buyer=user, transactions=transactions)


@app.route('/workshop')
def workshop():
    if not request.environ['user']:
        return redirect('/login?next=/workshop')
    user = request.environ['user']
    if user['type'] != 'seller':
        abort(403)
    seller_items = db.get_items_by_seller_id(user['user_id'])
    return render_template('seller_workshop.html', items=seller_items)


@app.route('/workshop/create', methods=['GET', 'POST'])
def item_create():
    errors = []
    if not request.environ['user']:
        return redirect('/login?next=/workshop')
    user = request.environ['user']
    if user['type'] != 'seller':
        abort(403)
    seller_id = user['user_id']
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        category_id = request.form['category']
        try:
            db.create_item(name, description, price, quantity, category_id, seller_id)
            return redirect('/workshop')
        except Exception as e:
            errors.append(str(e))
            raise e
    return render_template('seller_item_create.html', item=request.form, errors=errors, categories=db.get_categories())


@app.route('/workshop/<item_id>', methods=['GET', 'POST'])
def item_edit(item_id):
    if not request.environ['user']:
        return redirect('/login?next=/workshop')
    user = request.environ['user']
    if user['type'] != 'seller':
        abort(403)
    seller_id = user['user_id']
    req_item = db.get_item_by_id_and_seller_id(item_id, seller_id)
    if not item:
        abort(404)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        category_id = request.form['category']
        db.update_item(item_id, name, description, price, quantity, category_id)
        return redirect('/workshop')
    categories = db.get_categories()
    return render_template('seller_item_edit.html', item=req_item, categories=categories)



if __name__ == '__main__':
    app.run()
