from datetime import datetime
from models import check_password_hash
from pymongo import MongoClient
# from dotenv import load_dotenv
from flask_login import login_user, logout_user, login_required
from flask import request, session, jsonify, Flask
from models import User

app = Flask(__name__)

# load_dotenv()

mongo_host = 'mongo-service'
mongo_port = 27017  # Default MongoDB port
database_name = 'StockDB'
collection_name = 'users'

client = MongoClient(mongo_host, mongo_port)
db = client[database_name]
users_collection = db[collection_name]
purchases_collection = db['purchases']


def add_user(user):
    user_data = {
        "username": user.username,
        "password_hash": user.password_hash,
        "services": user.services
    }
    result = users_collection.insert_one(user_data)
    user.set_id(result.inserted_id)


def find_user_by_username(username):
    return users_collection.find_one({"username": username})


def check_user_password(username, password):
    user = find_user_by_username(username)
    if user and check_password_hash(user['password_hash'], password):
        return True
    return False


def user_from_dict(user_dict):
    user = User(
        username=user_dict['username'],
        password=user_dict['password_hash'],
    )
    user.set_id(user_dict['_id'])
    user.services = user_dict['services']
    return user


def update_prefernces(username, selected_sectors, risk_tolerance, investment_horizon):
    # Update user preferences in MongoDB
    users_collection.update_one(
        {'username': username},
        {'$set': {
            'preferences.sectors': selected_sectors,
            'preferences.risk_tolerance': risk_tolerance,
            'preferences.investment_horizon': investment_horizon
        }}
    )


def buy_share1(company, share, quantity, price):
    # Create a purchase document
    quantity = int(quantity)  # Convert quantity to an integer
    price = float(price)  # Convert price to a float
    purchase = {
        'username': session['username'],
        'company': company,
        'share': share,
        'quantity': quantity,
        'price': price,
        'total_cost': quantity * price,
        'timestamp': datetime.now()
    }
    # Insert the purchase document into the purchases collection
    purchases_collection.insert_one(purchase)
    return jsonify({'status': 'success', 'message': 'Purchase saved successfully'}), 200


def get_user_purchases():
    lst = purchases_collection.find({'username': session['username']})
    return lst


@login_required
def logout():
    session.clear()
    logout_user()
    return jsonify({'status': 'success', 'message': 'Logged out successfully'}), 200


def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        user_dict = find_user_by_username(username)
        if user_dict and check_user_password(username, password):
            user = user_from_dict(user_dict)
            session['username'] = user.username
            session['user_id'] = str(user._id)
            session['is_logged_in'] = True
            login_user(user)
            return jsonify({'status': 'success', 'user_id': str(user._id)})
        else:
            return jsonify({'status': 'error', 'message': 'שם משתמש או סיסמה שגויים'}), 401


def is_password_legal(password):
    if len(password) < 8:
        return False
    special_characters = "!@#&%()"
    if not any(char in special_characters for char in password):
        return False

    return True


def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    if password != confirm_password:
        return jsonify({'status': 'error', 'message': 'הסיסמאות לא תואמות!'}), 400
    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        return jsonify({'status': 'error', 'message': 'שם המשתמש כבר תפוס, אנא בחר שם משתמש אחר.'}), 409
    new_user = User(username=username, password=password)
    add_user(new_user)
    users_collection.update_one({"_id": new_user._id}, {"$set": {"services": new_user.services}})
    return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True, port=5005)


