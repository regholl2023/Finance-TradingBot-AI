import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Assuming the function is in the same directory
from Strategy_Stock import supertrend

load_dotenv()

# Initialize Alpaca API
api_key = os.getenv('APCA_API_KEY_ID')
api_secret = os.getenv('APCA_API_SECRET_KEY')
base_url = os.getenv('APCA_API_BASE_URL')

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# Fetch data for AAPL and GOOG
aapl_bars = api.get_bars("AAPL", TimeFrame.Minute, limit=100).df
goog_bars = api.get_bars("GOOG", TimeFrame.Minute, limit=100).df

# Prepare the data for Supertrend calculation (for AAPL)
data_aapl = {
    'close': aapl_bars['close'],
    'high': aapl_bars['high'],
    'low': aapl_bars['low']
}
df_aapl = pd.DataFrame(data_aapl)

# Calculate Supertrend for AAPL
supertrend_aapl = supertrend(df_aapl)

# Ensure that `supertrend` is not NaN for all entries
if supertrend_aapl['supertrend'].isnull().all():
    raise ValueError(
        "All values in Supertrend are NaN. Check the supertrend calculation.")

# Use Supertrend values as feature for training
X_train = np.array(supertrend_aapl['supertrend']).reshape(-1, 1)
y_train = np.array(goog_bars['close']).reshape(-1, 1)

# Handle mismatched data lengths
min_length = min(len(X_train), len(y_train))
X_train = X_train[:min_length]
y_train = y_train[:min_length]

# Remove rows with NaN values in X_train and y_train
mask = ~np.isnan(X_train) & ~np.isnan(y_train)
X_train = X_train[mask].reshape(-1, 1)
y_train = y_train[mask].reshape(-1, 1)

# Separate scalers for X_train and y_train
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_train_scaled = scaler_X.fit_transform(X_train)
y_train_scaled = scaler_y.fit_transform(y_train)

# Build the model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[1])
])

# Compile the model
model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.001),
              loss='mean_squared_error')

# Train the model
model.fit(X_train_scaled, y_train_scaled, epochs=500)

# Predict using the most recent close price from AAPL
most_recent_close = aapl_bars['close'].iloc[-1]
scaled_prediction_input = scaler_X.transform([[most_recent_close]])
prediction_scaled = model.predict(scaled_prediction_input)
predicted_value = scaler_y.inverse_transform(prediction_scaled)

print(f"Prediction for next stock value: {predicted_value[0][0]}")
