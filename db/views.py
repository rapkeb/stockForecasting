from datetime import datetime

import pandas as pd
from models import check_password_hash
from pymongo import MongoClient
# from dotenv import load_dotenv
from flask_login import current_user, login_user, logout_user, login_required
from flask import request, session, jsonify, Flask
from models import User
from confluent_kafka import Producer # Kafka Configuration 
from bson.son import SON


# load_dotenv()

mongo_host = 'mongo-service'
mongo_port = 27017  # Default MongoDB port
database_name = 'StockDB'
collection_name = 'users'

client = MongoClient(mongo_host, mongo_port)
db = client[database_name]
users_collection = db[collection_name]
purchases_collection = db['purchases']

for document in db['login_interactions'].find():
    print(document)

conf = {'bootstrap.servers': 'kafka:9092'}  # Kafka service name and port in Minikube
producer = Producer(conf) 
def delivery_report(err, msg): 
    if err is not None: 
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def send_message(topic, message):
    producer.produce(topic, message, callback=delivery_report) 
    producer.flush()

_df = pd.read_csv('companylist.csv')
df = _df.copy()
df = df.fillna('N/A')

def add_user(user):
    user_data = {
        "username": user.username,
        "password_hash": user.password_hash,
        "is_admin": user.is_admin,
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
        is_admin=user_dict['is_admin'],
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


def preferences():
    if request.method == 'POST':
        data = request.json
        selected_sectors = data.get('sectors')
        risk_tolerance = data.get('risk_tolerance')
        investment_horizon = data.get('investment_horizon')
        username = session.get('username')

        if not username or not selected_sectors or not risk_tolerance or not investment_horizon:
            return jsonify({'error': 'Missing data fields'}), 400

        update_prefernces(username, selected_sectors, risk_tolerance, investment_horizon)
        return jsonify({'status': 'success', 'message': 'Preferences updated successfully'}), 200

    elif request.method == 'GET':
        username = session.get('username')
        if not username:
            return jsonify({'error': 'Username is required'}), 400

        user = find_user_by_username(username)
        preferences = user.get('preferences', {})
        sectors = df['Sector'].unique().tolist()
        return jsonify({'preferences': preferences, 'sectors': sectors}), 200


def buy_share():
    data = request.json
    company = data.get('company')
    share = data.get('share')
    quantity = data.get('quantity')
    price = data.get('price')

    if not all([company, share, quantity, price]):
        return jsonify({'status': 'error', 'message': 'Missing data fields'}), 400

    buy_share1(company, share, quantity, price)
    send_message('buy', str(int(quantity)*float(price)))
    return jsonify({'status': 'success', 'message': 'Purchase saved successfully'}), 200


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
    username = session.get('username')
    if not username:
        return jsonify({"error": "User not logged in"}), 401

    purchases = list(purchases_collection.find({'username': username}))
    for purchase in purchases:
        purchase['_id'] = str(purchase['_id'])  # Convert ObjectId to string
    return jsonify(purchases)


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
            session['admin'] = user.is_admin
            login_user(user)
            send_message('login', str(username))
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
    new_user = User(username=username, password=password, is_admin=False)
    add_user(new_user)
    users_collection.update_one({"_id": new_user._id}, {"$set": {"services": new_user.services}})
    return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201


def is_logged_in():
    if current_user.is_authenticated:
        return jsonify({'is_logged_in': True})
    else:
        return jsonify({'is_logged_in': False})
    
def is_admin():
    if 'admin' in session and session['admin']:
        return jsonify({'is_logged_in': True, 'is_admin': True})
    else:
        return jsonify({'is_logged_in': 'username' in session, 'is_admin': False})
    

def write_user_interaction():
    data = request.json
    if not data or "message" not in data or "topic" not in data or "time" not in data:
        return jsonify({"error": "Invalid input"}), 400
    topic = data["topic"]
    message = data["message"]
    time = data["time"]
    try:
        collection_name = topic + "_interactions"
        # Check if the collection exists, if not, create it
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
        collection = db[collection_name]
        time_as_datetime = datetime.fromtimestamp(time)
        collection.insert_one({"message": message, "time": time_as_datetime})
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    #

def get_login_interactions():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    pipeline = [
        {"$match": {"time": {"$gte": datetime.fromisoformat(start_date), "$lte": datetime.fromisoformat(end_date)}}},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$time"}},
            "count": {"$sum": 1}
        }},
        {"$sort": SON([("_id", 1)])}  # Sort by date ascending
    ]
    #
    data = list(db.login_interactions.aggregate(pipeline))
    
    return jsonify({
        'labels': [d['_id'] for d in data],
        'values': [d['count'] for d in data]
    })

def get_shares_interactions():
    start_date_str = request.args.get('startDate')
    end_date_str = request.args.get('endDate')
    if start_date_str and end_date_str:
        try:
            start_date = datetime.fromisoformat(start_date_str)
            end_date = datetime.fromisoformat(end_date_str)
        except ValueError:
            return jsonify({"error": "Invalid date format. Please use ISO 8601 format."}), 400
    else:
        start_date = None
        end_date = None
    pipeline = [
        {"$match": {"time": {"$gte": start_date, "$lte": end_date}} if start_date and end_date else {}},
        {"$group": {
            "_id": "$message",  # Group by the share name (or 'message' in this case)
            "count": {"$sum": 1}  # Count occurrences
        }},
        {"$sort": {"count": -1}}  # Sort by count descending
    ]
    data = list(db.shares_interactions.aggregate(pipeline))
    # Prepare data for pie chart
    labels = [d['_id'] for d in data]
    values = [d['count'] for d in data]
    return jsonify({
        'labels': labels,
        'values': values
    })

def get_buy_interactions():
    start_date_str = request.args.get('startDate')
    end_date_str = request.args.get('endDate')
    if start_date_str and end_date_str:
        try:
            start_date = datetime.fromisoformat(start_date_str)
            end_date = datetime.fromisoformat(end_date_str)
        except ValueError:
            return jsonify({"error": "Invalid date format. Please use ISO 8601 format."}), 400
    else:
        start_date = None
        end_date = None
    pipeline = [
        {"$match": {"time": {"$gte": start_date, "$lte": end_date}} if start_date and end_date else {}},
        {"$addFields": {
            "amount": {"$toDouble": "$message"}  # Convert the 'message' field to a double
        }},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$time"}},
            "total_amount": {"$sum": "$amount"}  # Sum the converted amount
        }},
        {"$sort": {"_id": 1}}  # Sort by date ascending
    ]

    data = list(db.buy_interactions.aggregate(pipeline))
    
    # Prepare data for line chart
    labels = [d['_id'] for d in data]
    values = [d['total_amount'] for d in data]

    return jsonify({
        'labels': labels,
        'values': values
    })


