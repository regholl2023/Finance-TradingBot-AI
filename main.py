import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import MinMaxScaler

load_dotenv()

api_key = os.getenv('APCA_API_KEY_ID')
api_secret = os.getenv('APCA_API_SECRET_KEY')
base_url = os.getenv('APCA_API_BASE_URL')

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

aapl_bars = api.get_bars("AAPL", TimeFrame.Minute, limit=100).df
goog_bars = api.get_bars("GOOG", TimeFrame.Minute, limit=100).df

X_train = np.array(aapl_bars['close']).reshape(-1, 1)
y_train = np.array(goog_bars['close']).reshape(-1, 1)

min_length = min(len(X_train), len(y_train))
X_train = X_train[:min_length]
y_train = y_train[:min_length]

X_train = X_train[~np.isnan(X_train)]
y_train = y_train[~np.isnan(y_train)]

X_train = X_train.reshape(-1, 1)
y_train = y_train.reshape(-1, 1)

scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
y_train_scaled = scaler.fit_transform(y_train)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[1])
])

model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.001),
              loss='mean_squared_error')

model.fit(X_train_scaled, y_train_scaled, epochs=500)

prediction = model.predict(scaler.transform([[aapl_bars['close'][-1]]]))
predicted_value = scaler.inverse_transform(prediction)
print(f"Prediction for next stock value: {predicted_value[0][0]}")
