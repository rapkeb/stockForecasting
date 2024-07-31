from flask import render_template, request, redirect, session, url_for, jsonify, flash
from flask_login import login_required
import requests


def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        backend_api_url = 'db/login'  # Adjust URL to your backend service
        response = requests.post(backend_api_url, json={'username': username, 'password': password})
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                session['username'] = username
                session['user_id'] = data['user_id']
                session['is_logged_in'] = True
                return redirect(url_for('index', user_id=data['user_id']))
            else:
                flash(data['message'])
        else:
            flash('An error occurred during login. Please try again.')
        return render_template('login.html', username=username)
    return render_template('login.html')


def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        backend_api_url = 'db/register'  # Adjust URL to your backend service
        response = requests.post(backend_api_url, json={
            'username': username,
            'password': password,
            'confirm_password': confirm_password
        })
        if response.status_code == 201:
            return redirect(url_for('login'))
        else:
            data = response.json()
            flash(data['message'])
            return render_template('register.html', username=username)


def logout():
    backend_api_url = 'db/logout'  # Adjust URL to your backend service
    response = requests.post(backend_api_url)
    if response.status_code == 200:
        session.clear()
        return redirect(url_for('login'))
    else:
        return "Error logging out", response.status_code


@login_required
def company_chart():
    company_name = request.args.get('company')
    share = request.args.get('share')
    backend_api_url = 'back/company_chart'
    response = requests.get(backend_api_url, params={'share': share})
    if response.status_code == 200:
        data = response.json()
    else:
        data = {}
    return render_template('chart.html', company=company_name, share=share, data1=data)


@login_required
def index():
    # Backend API URL
    backend_api_url = 'back/homepage'
    # Fetch data from backend API
    response = requests.get(backend_api_url)
    if response.status_code == 200:
        companies = response.json()
    else:
        companies = []
    return render_template('index.html', companies=companies)


@login_required
def compare_shares():
    company1_name = request.args.get('company1')
    company2_name = request.args.get('company2')
    if not company1_name or not company2_name:
        return redirect(url_for('index'))
    # Backend API URL
    backend_api_url = f'back/compare_shares?company1={company1_name}&company2={company2_name}'
    # Fetch data from backend API
    response = requests.get(backend_api_url)
    if response.status_code == 200:
        data = response.json()
    else:
        data = {}
    return render_template('compare_shares.html', company1=data.get('company1'), data1=data.get('data1'), company2=data.get('company2'), data2=data.get('data2'))


@login_required
def buy_share():
    if request.method == 'POST':
        company = request.form.get('company')
        share = request.form.get('share')
        quantity = request.form.get('quantity')
        price = request.form.get('price')

        if not all([company, share, quantity, price]):
            return jsonify({'status': 'error', 'message': 'Missing data fields'}), 400

        backend_api_url = 'back/buy_share'
        data = {
            'company': company,
            'share': share,
            'quantity': quantity,
            'price': price
        }

        response = requests.post(backend_api_url, json=data)
        if response.status_code == 200:
            return jsonify({'status': 'success', 'message': 'Purchase saved successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Failed to save purchase'}), response.status_code


@login_required
def recommendation():
    company = request.args.get('company')
    backend_api_url = 'back/recommendation'  # Adjust URL to your backend service
    response = requests.get(backend_api_url, params={'company': company})
    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        error_message = response.json().get('error', 'An error occurred')
        return jsonify(error_message)
    

@login_required
def current_price():
    company = request.args.get('company')
    backend_api_url = 'back/current_price'  # Adjust URL to your backend service
    response = requests.get(backend_api_url, params={'company': company})

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        error_message = response.json().get('error', 'An error occurred')
        return jsonify(error_message)


@login_required
def preferences():
    backend_api_url = 'back/preferences'
    if request.method == 'POST':
        selected_sectors = request.form.getlist('sectors')
        risk_tolerance = request.form.get('risk_tolerance')
        investment_horizon = request.form.get('investment_horizon')
        username = session.get('username')
        if not username:
            return "User not logged in", 401
        payload = {
            'username': username,
            'sectors': selected_sectors,
            'risk_tolerance': risk_tolerance,
            'investment_horizon': investment_horizon
        }
        response = requests.post(backend_api_url, json=payload)
        if response.status_code == 200:
            return redirect(url_for('preferences'))
        else:
            return "Error updating preferences", response.status_code

    elif request.method == 'GET':
        username = session.get('username')
        if not username:
            return "User not logged in", 401

        response = requests.get(backend_api_url, params={'username': username})
        if response.status_code == 200:
            data = response.json()
            preferences = data['preferences']
            sectors = data['sectors']
            return render_template('preferences.html', preferences=preferences, sectors=sectors)
        else:
            return "Error fetching preferences", response.status_code


@login_required
def predict():
    if request.method == 'GET':
        date = request.form.get('date')
        share = request.form.get('share')
        if not date or not share:
            return jsonify({"error": "Missing date or share parameter"}), 400
        backend_api_url = 'back/predict'
        params = {'date': date, 'share': share}
        response = requests.get(backend_api_url, params=params)
        if response.status_code == 200:
            prediction_data = response.json()
            return jsonify(prediction_data)
        else:
            return jsonify({"error": "Failed to fetch prediction"}), response.status_code


@login_required
def purchases():
    backend_api_url = 'back/purchases'
    username = session.get('username')
    if not username:
        return "User not logged in", 401
    response = requests.get(backend_api_url, params={'username': username})
    if response.status_code == 200:
        purchase_list = response.json()
        return render_template('purchases.html', purchases=purchase_list)
    else:
        return "Error fetching purchases", response.status_code
