import tensorflow as tf
import numpy as np

# Dummy data for training (replace with real stock data)
X_train = np.array([1, 2, 3, 4, 5], dtype=float)
y_train = np.array([5, 7, 9, 11, 13], dtype=float)

# Build a simple model
model = tf.keras.Sequential([tf.keras.layers.Dense(units=1, input_shape=[1])])
model.compile(optimizer='sgd', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=500)

# Make a prediction (replace with real stock input)
prediction = model.predict([6])
print(f"Prediction for stock value: {prediction[0][0]}")
