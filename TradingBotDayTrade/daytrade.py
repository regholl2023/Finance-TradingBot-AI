import alpaca_trade_api as tradeapi
import time
import os

# Alpaca API credentials from env
API_KEY = os.getenv('APCA_API_KEY_ID')
API_SECRET = os.getenv('APCA_API_SECRET_KEY')
BASE_URL = os.getenv('APCA_API_BASE_URL')


# Initialize the Alpaca API
auth = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')
account = auth.get_account()

# Check if the account is active
if account.status != "ACTIVE":
    raise Exception("Account is not active. Please check your Alpaca account.")

# Settings
symbol = "AAPL"  # Stock to trade
cash_to_invest = 100000  # Simulated cash
sma_short_window = 5  # Short SMA window
sma_long_window = 20  # Long SMA window


def get_historical_data(symbol, timeframe="1Min", limit=100):
    """Fetch historical market data for the given symbol."""
    bars = auth.get_bars(symbol, timeframe, limit=limit).df
    return bars.reset_index()


def calculate_sma(data, window):
    """Calculate the Simple Moving Average."""
    return data['close'].rolling(window=window).mean()


def place_order(symbol, qty, side):
    """Place a market order."""
    try:
        auth.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type="market",
            time_in_force="gtc"
        )
        print(f"Order placed: {side} {qty} shares of {symbol}")
    except Exception as e:
        print(f"Order failed: {e}")


def trading_strategy():
    """Implement the trading strategy."""
    global cash_to_invest

    # Get historical data
    data = get_historical_data(symbol, timeframe="1Min", limit=100)
    data['sma_short'] = calculate_sma(data, sma_short_window)
    data['sma_long'] = calculate_sma(data, sma_long_window)

    # Check the latest data
    latest_data = data.iloc[-1]
    prev_data = data.iloc[-2]

    # Check for crossover
    if (prev_data['sma_short'] <= prev_data['sma_long'] and
            latest_data['sma_short'] > latest_data['sma_long']):
        # Buy signal
        qty = int(cash_to_invest / latest_data['close'])
        place_order(symbol, qty, "buy")
        cash_to_invest -= qty * latest_data['close']

    elif (prev_data['sma_short'] >= prev_data['sma_long'] and
          latest_data['sma_short'] < latest_data['sma_long']):
        # Sell signal
        position = auth.get_position(symbol)
        if position:
            qty = position.qty
            place_order(symbol, qty, "sell")
            cash_to_invest += qty * latest_data['close']


if __name__ == "__main__":
    print("Starting trading bot...")
    try:
        while True:
            trading_strategy()
            time.sleep(60)  # Run every minute
    except KeyboardInterrupt:
        print("Trading bot stopped.")
