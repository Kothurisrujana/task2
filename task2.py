#import requests
import json
import datetime

# Constants
API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'
BASE_URL = 'https://www.alphavantage.co/query'
PORTFOLIO = {}

def get_stock_price(symbol):
    """Fetch the current price of a stock using Alpha Vantage API."""
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    try:
        last_refreshed = data['Meta Data']['3. Last Refreshed']
        latest_close = data['Time Series (1min)'][last_refreshed]['4. close']
        return float(latest_close)
    except KeyError:
        print(f"Error fetching data for {symbol}.")
        return None

def add_stock(symbol, shares, price_per_share):
    """Add a stock to the portfolio."""
    if symbol in PORTFOLIO:
        PORTFOLIO[symbol]['shares'] += shares
        PORTFOLIO[symbol]['price_per_share'] = price_per_share
    else:
        PORTFOLIO[symbol] = {'shares': shares, 'price_per_share': price_per_share}
    print(f"Added {shares} shares of {symbol} at ${price_per_share:.2f} per share.")

def remove_stock(symbol):
    """Remove a stock from the portfolio."""
    if symbol in PORTFOLIO:
        del PORTFOLIO[symbol]
        print(f"Removed {symbol} from portfolio.")
    else:
        print(f"{symbol} is not in the portfolio.")

def track_performance():
    """Display the performance of the entire portfolio."""
    total_investment = 0
    current_value = 0
    
    for symbol, details in PORTFOLIO.items():
        current_price = get_stock_price(symbol)
        if current_price:
            investment = details['shares'] * details['price_per_share']
            value = details['shares'] * current_price
            total_investment += investment
            current_value += value
            print(f"{symbol}: Investment: ${investment:.2f}, Current Value: ${value:.2f}, Gain/Loss: ${value - investment:.2f}")
    
    print(f"Total Investment: ${total_investment:.2f}")
    print(f"Total Current Value: ${current_value:.2f}")
    print(f"Total Gain/Loss: ${current_value - total_investment:.2f}")

def main():
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Track Performance")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            price_per_share = float(input("Enter price per share: "))
            add_stock(symbol, shares, price_per_share)
        elif choice == '2':
            symbol = input("Enter stock symbol to remove: ").upper()
            remove_stock(symbol)
        elif choice == '3':
            track_performance()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
