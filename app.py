from conf import BasicConfig
from flask import Flask, render_template, request, make_response, redirect
from database.persistence import ApplicationDatabase
from sessions import SessionManager
from auth import UserManager
from middleware import AuthenticationMiddleware

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
            res = make_response(redirect('/'))
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
    if request.method == 'GET':
        return render_template('buyer_signup.html')
    else:
        pass


@app.route('/signup/seller', methods=['GET', 'POST'])
def seller_signup():
    if request.method == 'GET':
        return render_template('seller_signup.html')
    else:
        pass


@app.route('/items')
def items():
    # items = db.get_items(name=request.args.get('name'))

    return render_template('items.html', items=fake_items)


@app.route('/items/<item_id>')
def item(item_id):
    requested_item = next(x for x in fake_items if x['id'] == item_id)
    comments = requested_item["comments"]
    return render_template('item.html', item=requested_item, comments=comments)


@app.route('/items/<item_id>/buy', methods=['GET', 'POST'])
def buy_item(item_id):
    requested_item = next(x for x in fake_items if x['id'] == item_id)
    return render_template('buy_item.html', item=requested_item)


@app.route('/account')
def account():
    if not request.environ['user']:
        return 401
    else:
        user = request.environ['user']
        if user['type'] == 'seller':
            return render_template('seller_account.html', seller=user)
        else:
            return render_template('buyer_account.html', buyer=user)


if __name__ == '__main__':
    app.run()
