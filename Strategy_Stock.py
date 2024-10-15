import pandas as pd
import numpy as np

# Average True Range (ATR) Calculation


def atr(data, period=14):
    data['high-low'] = data['high'] - data['low']
    data['high-close'] = np.abs(data['high'] - data['close'].shift())
    data['low-close'] = np.abs(data['low'] - data['close'].shift())
    true_range = data[['high-low', 'high-close', 'low-close']].max(axis=1)
    atr = true_range.rolling(period).mean()
    return atr

# Supertrend Calculation


def supertrend(data, period=14, multiplier=3):
    # Calculate ATR
    atr_value = atr(data, period)

    # Calculate basic upper and lower bands
    data['basic_upperband'] = (
        (data['high'] + data['low']) / 2) + (multiplier * atr_value)
    data['basic_lowerband'] = (
        (data['high'] + data['low']) / 2) - (multiplier * atr_value)

    # Initialize Supertrend and direction columns
    data['supertrend'] = np.nan
    data['in_uptrend'] = True

    # Populate Supertrend values
    for current in range(1, len(data.index)):
        previous = current - 1

        if data['close'][current] > data['basic_upperband'][previous]:
            data['supertrend'][current] = data['basic_upperband'][current]
        elif data['close'][current] < data['basic_lowerband'][previous]:
            data['supertrend'][current] = data['basic_lowerband'][current]
        else:
            # Carry forward previous Supertrend value
            if data['in_uptrend'][previous]:
                data['supertrend'][current] = (
                    data['basic_lowerband'][current]
                    if data['basic_lowerband'][current] > data['supertrend'][
                        previous]
                    else data['supertrend'][previous]
                )
            else:
                data['supertrend'][current] = (
                    data['basic_upperband'][current]
                    if data['basic_upperband'][current] < data['supertrend'][
                        previous]
                    else data['supertrend'][previous]
                )

        data['in_uptrend'][current] = (
            data['close'][current] > data['supertrend'][current]
        )

    return data


data = {'open': [100, 102, 104, 106, 108, 110],
        'high': [102, 104, 106, 108, 110, 112],
        'low': [99, 101, 103, 105, 107, 109],
        'close': [101, 103, 105, 107, 109, 111]}
df = pd.DataFrame(data)

# Calculate the Supertrend for the given data
supertrend_df = supertrend(df)

# Check the results
print(supertrend_df[['close', 'supertrend', 'in_uptrend']])
