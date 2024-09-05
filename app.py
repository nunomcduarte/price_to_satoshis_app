from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Function to get current Bitcoin price in EUR
def get_btc_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur'
    response = requests.get(url)
    data = response.json()
    return data['bitcoin']['eur']

# Function to get historical Bitcoin price from a year ago
def get_btc_price_one_year_ago():
    one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%d-%m-%Y')
    url = f'https://api.coingecko.com/api/v3/coins/bitcoin/history?date={one_year_ago}&localization=false'
    response = requests.get(url)
    data = response.json()
    return data['market_data']['current_price']['eur']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_to_satoshis():
    # Get the price from the form (in EUR)
    price_in_eur = float(request.form['price'])

    # Get current Bitcoin price
    current_btc_price = get_btc_price()

    # Get historical Bitcoin price (one year ago)
    btc_price_one_year_ago = get_btc_price_one_year_ago()

    # Convert current price to satoshis
    current_satoshis = (price_in_eur / current_btc_price) * 100000000

    # Convert historical price to satoshis
    historical_satoshis = (price_in_eur / btc_price_one_year_ago) * 100000000

    # Calculate the percentage change
    percentage_change = ((current_satoshis - historical_satoshis) / historical_satoshis) * 100

    return f'''
        The price of {price_in_eur} EUR is {current_satoshis:.0f} satoshis today.<br>
        One year ago, the same price would have been {historical_satoshis:.0f} satoshis.<br>
        The price in satoshis has changed by {percentage_change:.2f}% over the last year.
    '''

if __name__ == '__main__':
    app.run(debug=True)
