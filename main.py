import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import pandas as pd
from typing import List, Dict, Tuple
from Strategy_Stock import supertrend


def initialize_api() -> tradeapi.REST:
    """Initialize and return Alpaca API client."""
    load_dotenv()

    api_key = os.getenv('APCA_API_KEY_ID')
    api_secret = os.getenv('APCA_API_SECRET_KEY')
    base_url = os.getenv('APCA_API_BASE_URL')

    return tradeapi.REST(api_key, api_secret, base_url, api_version='v2')


def read_symbols(filename: str) -> List[str]:
    """Read stock symbols from a text file."""
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]


def get_stock_data(api: tradeapi.REST, symbol: str) -> pd.DataFrame:
    """Fetch stock data from Alpaca API."""
    bars = api.get_bars(symbol, TimeFrame.Minute, limit=100).df
    return pd.DataFrame({
        'open': bars['open'],
        'high': bars['high'],
        'low': bars['low'],
        'close': bars['close']
    })


def calculate_supertrends(
    df: pd.DataFrame
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Calculate three supertrend signals with different parameters."""
    # Supertrend 1: ATR 12, Multiplier 3
    st1 = supertrend(df.copy(), period=12, multiplier=3)['in_uptrend']

    # Supertrend 2: ATR 10, Multiplier 1
    st2 = supertrend(df.copy(), period=10, multiplier=1)['in_uptrend']

    # Supertrend 3: ATR 11, Multiplier 2
    st3 = supertrend(df.copy(), period=11, multiplier=2)['in_uptrend']

    return st1, st2, st3


def check_signals(
    st1: pd.Series,
    st2: pd.Series,
    st3: pd.Series,
    current_positions: Dict[str, str]
) -> str:
    """
    Check supertrend signals and return trading decision.
    Returns: 'buy', 'sell', 'exit', or 'hold'
    """
    # Get most recent signals
    latest_st1 = st1.iloc[-1]
    latest_st2 = st2.iloc[-1]
    latest_st3 = st3.iloc[-1]

    # Check if all signals agree
    all_bullish = all([latest_st1, latest_st2, latest_st3])
    all_bearish = all([not latest_st1, not latest_st2, not latest_st3])

    if all_bullish:
        return 'buy'
    elif all_bearish:
        return 'sell'
    else:
        return 'exit'


def execute_trade(
    api: tradeapi.REST,
    symbol: str,
    action: str,
    current_positions: Dict[str, str]
) -> Dict[str, str]:
    """Execute trading action and update positions."""
    try:
        current_position = current_positions.get(symbol, None)

        if action == 'buy' and current_position != 'long':
            # Exit any existing short position
            if current_position == 'short':
                api.close_position(symbol)

            # Enter long position
            api.submit_order(
                symbol=symbol,
                qty=1,  # Adjust position size as needed
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            current_positions[symbol] = 'long'
            print(f"Entered long position in {symbol}")

        elif action == 'sell' and current_position != 'short':
            # Exit any existing long position
            if current_position == 'long':
                api.close_position(symbol)

            # Enter short position
            api.submit_order(
                symbol=symbol,
                qty=1,  # Adjust position size as needed
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            current_positions[symbol] = 'short'
            print(f"Entered short position in {symbol}")

        elif action == 'exit' and current_position is not None:
            # Exit any existing position
            api.close_position(symbol)
            del current_positions[symbol]
            print(f"Exited position in {symbol}")

    except Exception as e:
        print(f"Error executing trade for {symbol}: {str(e)}")

    return current_positions


def main():
    # Initialize API and read symbols
    api = initialize_api()
    symbols = read_symbols('symbols.txt')

    # Track current positions
    current_positions = {}

    # Process each symbol
    for symbol in symbols:
        try:
            print(f"\nProcessing {symbol}...")

            # Get stock data
            df = get_stock_data(api, symbol)

            # Calculate supertrends
            st1, st2, st3 = calculate_supertrends(df)

            # Check signals
            action = check_signals(st1, st2, st3, current_positions)

            # Execute trades
            current_positions = execute_trade(
                api,
                symbol,
                action,
                current_positions
            )

        except Exception as e:
            print(f"Error processing {symbol}: {str(e)}")
            continue

    # Print final positions
    print("\nCurrent positions:")
    for symbol, position in current_positions.items():
        print(f"{symbol}: {position}")


if __name__ == "__main__":
    main()
