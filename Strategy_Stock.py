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


def supertrend(data, period=3, multiplier=3):
    hl2 = (data['high'] + data['low']) / 2
    data['atr'] = atr(data, period)
    data['upperband'] = hl2 + (multiplier * data['atr'])
    data['lowerband'] = hl2 - (multiplier * data['atr'])
    data['in_uptrend'] = True

    for i in range(1, len(data)):
        current, previous = i, i-1

        if data['close'][current] > data['upperband'][previous]:
            data.loc[current, 'in_uptrend'] = True
        elif data['close'][current] < data['lowerband'][previous]:
            data.loc[current, 'in_uptrend'] = False
        else:
            data.loc[current, 'in_uptrend'] = data['in_uptrend'][previous]

        if (data['in_uptrend'][current] and
                data['lowerband'][current] < data['lowerband'][previous]):
            data.loc[current, 'lowerband'] = data['lowerband'][previous]

        if (not data['in_uptrend'][current] and
                data['upperband'][current] > data['upperband'][previous]):
            data.loc[current, 'upperband'] = data['upperband'][previous]

    data['supertrend'] = np.where(data['in_uptrend'],
                                  data['lowerband'],
                                  data['upperband'])

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
