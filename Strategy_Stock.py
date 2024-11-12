import pandas as pd
import numpy as np


def atr(data, period=3):
    data['high-low'] = data['high'] - data['low']
    data['high-close'] = np.abs(data['high'] - data['close'].shift())
    data['low-close'] = np.abs(data['low'] - data['close'].shift())
    tr = data[['high-low', 'high-close', 'low-close']
              ].max(axis=1, skipna=False)
    atr = tr.rolling(period).mean()
    return atr


def supertrend(data):
    # Calculate ATR and initialize columns for supertrend values
    data['supertrend'] = np.nan
    data['in_uptrend'] = True

    for current in range(1, len(data)):
        previous = current - 1

        if 'upperband' in data.columns and 'lowerband' in data.columns:
            # Access values using iloc to avoid KeyError
            if data['close'].iloc[current] > data['upperband'].iloc[previous]:
                data.loc[current, 'in_uptrend'] = True
            elif data['close'].iloc[current] < \
                    data['lowerband'].iloc[previous]:
                data.loc[current, 'in_uptrend'] = False
            else:
                data.loc[current, 'in_uptrend'] = \
                    data['in_uptrend'].iloc[previous]

            # Set supertrend value based on the trend direction
            if data['in_uptrend'].iloc[current]:
                data.loc[current, 'supertrend'] = \
                    data['lowerband'].iloc[current]
            else:
                data.loc[current, 'supertrend'] = \
                    data['upperband'].iloc[current]

    return data


# Sample data
data = {
    'open': [100, 102, 104, 106, 108, 110],
    'high': [102, 104, 106, 108, 110, 112],
    'low': [99, 101, 103, 105, 107, 109],
    'close': [101, 103, 105, 107, 109, 111]
}
df = pd.DataFrame(data)

# Calculate the Supertrend
supertrend_df = supertrend(df)

# Display results
print(supertrend_df[['close', 'supertrend', 'in_uptrend']])
