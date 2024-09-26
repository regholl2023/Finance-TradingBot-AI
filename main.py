import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame


load_dotenv()

# Access the variables
api_key = os.getenv('APCA_API_KEY_ID')
api_secret = os.getenv('APCA_API_SECRET_KEY')
base_url = os.getenv('APCA_API_BASE_URL')


api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# Fetch the latest bars for BLNK stock
aapl_bars = api.get_bars("BLNK", TimeFrame.Minute, limit=5).df


for index, bar in aapl_bars.iterrows():
    print(f"Time: {index}, Close: {bar['close']}")

account = api.get_account()
print(account.buying_power)

clock = api.get_clock()
print('The market is {}'.format('open.' if clock.is_open else 'closed.'))


orders = api.list_orders(status='open')
print(orders)
