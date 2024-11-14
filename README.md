# Automated Stock Trading using Alpaca API and TensorFlow

This project aims to automate stock trading using the **Alpaca API** for real-time market data and trade execution. **TensorFlow** is used for implementing machine learning models, while different trading strategies, including the **Supertrend** indicator, are being tested to optimize trade performance. The code is designed to run automatically and execute trades based on defined strategies.

This project is based on trading strategies provided in this video : https://www.youtube.com/watch?v=21b5QF-b0rE
- Talks about using 3 supertrend indicators

## Project Structure

- `main.py`: This is the main script that runs the trading bot. It fetches real-time stock data using the Alpaca API, applies trading strategies, and automatically executes buy/sell orders based on the strategy's signals.
- `Strategy_Stock.py`: This script handles various trading strategies. Currently, the **Supertrend** strategy is implemented and under testing. Other strategies can be added and tested through this file.

## Features

1. **Alpaca API Integration**: The bot retrieves real-time stock data (e.g., candlestick data) and executes trades via Alpaca's API.
2. **TensorFlow ML Integration**: Machine learning models are applied to predict stock price movements or optimize trade execution.
3. **Supertrend Indicator**: The Supertrend strategy is implemented to generate buy/sell signals based on market trends.
4. **Automated Trading**: Once a strategy generates a signal, the bot automatically executes the trade on the Alpaca platform.


## Usage

1. **Customizing Strategies**:
   - To customize or add new strategies, edit the `Strategy_Stock.py` file. Each strategy can be defined as a separate function and then invoked in `main.py` based on your desired trading approach.

2. **Supertrend Strategy**:
   - The **Supertrend** strategy currently fetches stock data, calculates the Supertrend line, and makes buy/sell decisions based on whether the price is above or below the Supertrend line.
   - You can fine-tune the parameters like **ATR period** and **Multiplier** in `Strategy_Stock.py`.

## Files

- **`main.py`**: This script orchestrates the overall trading process:
  - Fetches stock data.
  - Calls strategy functions to generate trading signals.
  - Executes trades using the Alpaca API.

- **`Strategy_Stock.py`**: Contains various trading strategies that are tested and implemented in this project. Currently, the **Supertrend** strategy is implemented.

## Future Work

- Implement additional strategies like **Moving Average Crossovers**, **RSI**, and **Machine Learning-based Predictions**.
- Improve the Supertrend strategy by optimizing parameters based on backtesting results.
- Integrate more complex TensorFlow models for predictive trading.
- Add more logging and error handling for production readiness.


## Disclaimer

This bot is currently being tested and should not be used for live trading without proper risk management and testing. Use at your own risk.

