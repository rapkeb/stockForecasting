import os
from flask import render_template, request, jsonify
import requests
import yfinance as yf
import datetime as dt
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL
from sklearn.metrics import mean_squared_error, accuracy_score
# from mongo.db import find_user_by_username, update_prefernces, buy_share1, get_user_purchases
from flask_login import login_required
from confluent_kafka import Producer # Kafka Configuration 

_df = pd.read_csv('companylist.csv')
df = _df.copy()
df = df.fillna('N/A')

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


def company_chart():
    share = request.args.get('share')
    actual_date = dt.date.today()
    past_date = actual_date - dt.timedelta(days=365 * 5)
    actual_date = actual_date.strftime("%Y-%m-%d")
    past_date = past_date.strftime("%Y-%m-%d")
    data = yf.download(share, start=past_date, end=actual_date)
    df = pd.DataFrame(data).reset_index()

    def format_data(company_data):
        return {
            'dates': company_data['Date'].tolist(),
            'closes': company_data['Close'].tolist(),
            'opens': company_data['Open'].tolist(),
            'highs': company_data['High'].tolist(),
            'lows': company_data['Low'].tolist()
        }

    formatted_data = format_data(df)
    send_message('shares', str(share))
    return jsonify(formatted_data)


def index():
    unique_companies = df[['Company', 'Sector', 'Share', 'Industry']].drop_duplicates().sort_values(by='Company')
    unique_companies_list = unique_companies.to_dict(orient='records')
    return jsonify(unique_companies_list), 200


def compare_shares():
    company1_name = request.args.get('company1')
    company2_name = request.args.get('company2')

    actual_date = dt.date.today()
    past_date = actual_date - dt.timedelta(days=365 * 5)
    actual_date = actual_date.strftime("%Y-%m-%d")
    past_date = past_date.strftime("%Y-%m-%d")

    share1 = df.loc[df['Company'] == company1_name, 'Share'].values[0]
    share2 = df.loc[df['Company'] == company2_name, 'Share'].values[0]

    data1 = yf.download(share1, start=past_date, end=actual_date)
    data2 = yf.download(share2, start=past_date, end=actual_date)

    company1_data = pd.DataFrame(data1).reset_index()
    company2_data = pd.DataFrame(data2).reset_index()

    def format_data(company_data):
        return {
            'dates': company_data['Date'].tolist(),
            'closes': company_data['Close'].tolist(),
            'opens': company_data['Open'].tolist(),
            'highs': company_data['High'].tolist(),
            'lows': company_data['Low'].tolist()
        }

    data1 = format_data(company1_data)
    data2 = format_data(company2_data)

    send_message('shares', str(share1))
    send_message('shares', str(share2))

    return jsonify({
        'company1': company1_name,
        'data1': data1,
        'company2': company2_name,
        'data2': data2
    })
    

def current_price():
    company = request.args.get('company')
    price = get_current_price(company)
    if price is not None:
        return jsonify({'price': price}), 200
    else:
        return jsonify({'error': 'Unable to fetch price'}), 500


def get_current_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period="1d")

        # Check if history DataFrame is empty
        if history.empty:
            raise ValueError(f"No data available for symbol: {symbol}")

        return history['Close'].iloc[-1]
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


def recommendation():
    company = request.args.get('company')
    api_key = os.getenv('FINNHUB_API_KEY')
    url = f'https://finnhub.io/api/v1/stock/recommendation?symbol={company}&token={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch recommendations'}), response.status_code

def predict():
    date_str = request.args.get('date')
    share = request.args.get('share')

    if not date_str or not share:
        return jsonify({"error": "Missing date or share parameter"}), 400

    try:
        target_date = dt.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    actual_date = dt.date.today()
    past_date = actual_date - dt.timedelta(days=365 * 3)

    stock_dataframe = get_stock_data(share, past_date, actual_date)
    gold_dataframe = get_gold_data(past_date, actual_date)
    forex_dataframe = get_forex_data(past_date, actual_date)

    merged_dataframe = pd.merge(stock_dataframe, gold_dataframe, left_index=True, right_index=True)
    merged_dataframe = pd.merge(merged_dataframe, forex_dataframe, left_index=True, right_index=True)

    # Determine the number of days to forecast
    forecast_days = (target_date - actual_date).days
    
    if forecast_days <= 0:
        return jsonify({"error": "Target date must be in the future"}), 400

    forecast, trend, seasonal, resid = stl_forecast(merged_dataframe, steps=forecast_days)
    
    if len(forecast) < forecast_days:
        return jsonify({"error": "Unable to generate forecast for the specified date"}), 500
    
    # Retrieve the forecast for the target date
    target_forecast_index = forecast_days - 1
    todays_forecast = forecast[target_forecast_index]

    trend_accuracy = calculate_trend_accuracy(merged_dataframe, forecast)
    prediction = f"Predicted value for {share} on {date_str} is {todays_forecast:.2f}"
    
    return jsonify({"prediction": prediction, "trend_accuracy": f" in {trend_accuracy} accuracy percent"})


def get_stock_data(symbol, from_date, to_date):
    data = yf.download(symbol, start=from_date, end=to_date)
    df = pd.DataFrame(data)
    print(df.head())
    df['HighLoad'] = (df['High'] - df['Close']) / df['Close'] * 100.0
    df['Change'] = (df['Close'] - df['Open']) / df['Open'] * 100.0

    df['Price_Up'] = df['Close'].diff().fillna(0) > 0  # True if price went up, else False

    df['MA_5'] = df['Close'].rolling(window=5).mean()  # 5-day Moving Average
    df['MA_20'] = df['Close'].rolling(window=20).mean()  # 20-day Moving Average
    df['RSI'] = calculate_rsi(df['Close'])  # Relative Strength Index
    df['MACD'] = calculate_macd(df['Close'])  # MACD
    df['Bollinger_Upper'], df['Bollinger_Lower'] = calculate_bollinger_bands(df['Close'])  # Bollinger Bands

    df = df[['Close', 'HighLoad', 'Change', 'Volume', 'MA_5', 'MA_20', 'RSI', 'MACD', 'Bollinger_Upper', 'Bollinger_Lower', 'Price_Up']]
    df = df.dropna()  # Drop rows with NaN values due to moving averages
    return df

def get_gold_data(from_date, to_date):
    gold_data = yf.download('GC=F', start=from_date, end=to_date)
    gold_df = pd.DataFrame(gold_data)
    gold_df['Gold_HighLoad'] = (gold_df['High'] - gold_df['Close']) / gold_df['Close'] * 100.0
    gold_df['Gold_Change'] = (gold_df['Close'] - gold_df['Open']) / gold_df['Open'] * 100.0

    gold_df['Gold_Price_Up'] = gold_df['Close'].diff().fillna(0) > 0  # True if gold price went up, else False

    gold_df = gold_df[['Close', 'Gold_HighLoad', 'Gold_Change', 'Volume', 'Gold_Price_Up']]
    gold_df = gold_df.dropna()
    gold_df = gold_df.rename(columns={'Close': 'Gold_Close', 'Volume': 'Gold_Volume'})
    return gold_df

def get_forex_data(from_date, to_date):
    forex_data = yf.download('EURUSD=X', start=from_date, end=to_date)
    forex_df = pd.DataFrame(forex_data)
    forex_df['EURUSD_HighLoad'] = (forex_df['High'] - forex_df['Close']) / forex_df['Close'] * 100.0
    forex_df['EURUSD_Change'] = (forex_df['Close'] - forex_df['Open']) / forex_df['Open'] * 100.0

    forex_df['EURUSD_Price_Up'] = forex_df['Close'].diff().fillna(0) > 0  # True if EUR/USD rate went up, else False

    forex_df = forex_df[['Close', 'EURUSD_HighLoad', 'EURUSD_Change', 'Volume', 'EURUSD_Price_Up']]
    forex_df = forex_df.dropna()
    forex_df = forex_df.rename(columns={'Close': 'EURUSD_Close', 'Volume': 'EURUSD_Volume'})
    return forex_df

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(series, short_window=12, long_window=26, signal_window=9):
    short_ema = series.ewm(span=short_window, adjust=False).mean()
    long_ema = series.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd - signal

def calculate_bollinger_bands(series, window=20, num_std_dev=2):
    rolling_mean = series.rolling(window).mean()
    rolling_std = series.rolling(window).std()
    upper_band = rolling_mean + (rolling_std * num_std_dev)
    lower_band = rolling_mean - (rolling_std * num_std_dev)
    return upper_band, lower_band

def stl_forecast(df, steps=30, period=7, seasonal=13):
    # Fit STL decomposition
    stl = STL(df['Close'], period=period, seasonal=seasonal)
    result = stl.fit()

    trend = result.trend
    seasonal = result.seasonal
    resid = result.resid

    trend_forecast = [trend[-1]] * steps
    seasonal_forecast = list(seasonal[-period:]) * (steps // period + 1)
    seasonal_forecast = seasonal_forecast[:steps]
    forecast = np.array(trend_forecast) + np.array(seasonal_forecast)

    actual = df['Close'][-steps:].values
    mse = mean_squared_error(actual, forecast[-steps:])
    print(f'STL Forecast MSE: {mse}')

    return forecast, trend, seasonal, resid

    # plt.figure(figsize=(12, 8))
    # plt.subplot(411)
    # plt.plot(df.index, df['Close'], label='Original')
    # plt.legend(loc='best')
    # plt.subplot(412)
    # plt.plot(df.index, trend, label='Trend')
    # plt.legend(loc='best')
    # plt.subplot(413)
    # plt.plot(df.index, seasonal, label='Seasonality')
    # plt.legend(loc='best')
    # plt.subplot(414)
    # plt.plot(df.index, resid, label='Residuals')
    # plt.legend(loc='best')
    # plt.tight_layout()
    # plt.show()


def calculate_trend_accuracy(df, forecast):
    forecast_trend = np.sign(np.diff(forecast))
    actual_trend = np.sign(np.diff(df['Close'].values[-len(forecast):]))
    accuracy = accuracy_score(actual_trend > 0, forecast_trend > 0)
    return accuracy


def get_historical_data(share):
    actual_date = dt.date.today()
    past_date = actual_date - dt.timedelta(days=365 * 5)
    actual_date = actual_date.strftime("%Y-%m-%d")
    past_date = past_date.strftime("%Y-%m-%d")
    data = yf.download(share, start=past_date, end=actual_date)
    return pd.DataFrame(data).reset_index()

def calculate_percentage_change(df):
    if not df.empty:
        start_price = df.iloc[0]['Close']
        end_price = df.iloc[-1]['Close']
        return ((end_price - start_price) / start_price) * 100
    else:
        return None

def find_best_share(share_list):
    best_share = None
    best_change = -float('inf')  # Initialize with negative infinity to find the maximum

    for share in share_list:
        df = get_historical_data(share)
        percentage_change = calculate_percentage_change(df)
        
        if percentage_change is not None and percentage_change > best_change:
            best_change = percentage_change
            best_share = share

    return best_share, best_change

def best_share_long():
    sectors = fetch_user_preferences()
    filtered_shares_df = filter_shares_by_sector(df, sectors)
    share_list = get_share_names(filtered_shares_df)
    best_share, best_change = find_best_share(share_list)
    if best_share:
        response = {
            'best_share': best_share,
            'percentage_change': best_change
        }
    else:
        response = {'message': 'No valid data found for the provided shares.'}
    
    return jsonify(response)


def fetch_user_preferences():
    url = 'http://localhost:80/db/preferences'  # Replace with your Flask app's URL
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'})
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        data = response.json()

        # Extract the preferences and sectors from the JSON response
        print(data)
        preferences = data.get('preferences', {})
        sectors = preferences.get('sectors', [])
        print(sectors)
        return sectors
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    

def filter_shares_by_sector(df, sectors):
    if sectors:
        # Filter the DataFrame based on the sectors
        filtered_df = df[df['Sector'].isin(sectors)]
        return filtered_df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no sectors are provided

def get_share_names(df):
    # Extract the 'Share' column as a list
    return ['AMZN', 'AAPL']
    return df['Share'].tolist()

