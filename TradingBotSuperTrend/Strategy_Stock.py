import pandas as pd
import numpy as np


def atr(data, period=14):
    """Calculate Average True Range"""
    data['high-low'] = data['high'] - data['low']
    data['high-close'] = np.abs(data['high'] - data['close'].shift())
    data['low-close'] = np.abs(data['low'] - data['close'].shift())
    tr = data[['high-low', 'high-close', 'low-close']
              ].max(axis=1, skipna=False)
    atr = tr.rolling(period).mean()
    return atr


def supertrend(data, period=14, multiplier=3):
    """
    Calculate Supertrend indicator

    Parameters:
    data (pd.DataFrame): DataFrame with OHLC data
    period (int): Period for ATR calculation (default: 14)
    multiplier (int): Multiplier for ATR (default: 3)

    Returns:
    pd.DataFrame: Original dataframe with Supertrend columns added
    """
    # Calculate ATR
    hl2 = (data['high'] + data['low']) / 2
    data['atr'] = atr(data, period)

    # Calculate Upper and Lower Bands
    data['upperband'] = hl2 + (multiplier * data['atr'])
    data['lowerband'] = hl2 - (multiplier * data['atr'])

    # Initialize Supertrend columns
    data['supertrend'] = np.nan
    data['in_uptrend'] = True

    # Calculate Supertrend
    for current in range(1, len(data)):
        previous = current - 1

        # Update upper band
        upper_condition = (
            data['upperband'].iloc[current] < data['upperband'].iloc[previous]
            or data['close'].iloc[previous] > data['upperband'].iloc[previous]
        )

        if upper_condition:
            data.loc[current, 'upperband'] = min(
                data['upperband'].iloc[current],
                data['upperband'].iloc[previous]
            )

        # Update lower band
        lower_condition = (
            data['lowerband'].iloc[current] > data['lowerband'].iloc[previous]
            or data['close'].iloc[previous] < data['lowerband'].iloc[previous]
        )

        if lower_condition:
            data.loc[current, 'lowerband'] = max(
                data['lowerband'].iloc[current],
                data['lowerband'].iloc[previous]
            )

        # Update trend direction
        if data['close'].iloc[current] > data['upperband'].iloc[previous]:
            data.loc[current, 'in_uptrend'] = True
        elif data['close'].iloc[current] < data['lowerband'].iloc[previous]:
            data.loc[current, 'in_uptrend'] = False
        else:
            data.loc[current, 'in_uptrend'] = data['in_uptrend'].iloc[previous]

        # Set Supertrend value
        if data['in_uptrend'].iloc[current]:
            data.loc[current, 'supertrend'] = data['lowerband'].iloc[current]
        else:
            data.loc[current, 'supertrend'] = data['upperband'].iloc[current]

    return data


# Example usage
if __name__ == "__main__":
    # Sample data
    data = {
        'open':  [100, 102, 104, 103, 105, 107, 108, 109, 110, 109],
        'high':  [102, 104, 106, 104, 107, 108, 110, 112, 111, 110],
        'low':   [99,  101, 103, 101, 104, 106, 107, 108, 108, 107],
        'close': [101, 103, 105, 102, 106, 107, 109, 111, 109, 108]
    }
    df = pd.DataFrame(data)

    # Calculate Supertrend
    result = supertrend(df, period=7, multiplier=3)

    # Display results
    print("\nSupertrend Analysis:")
    cols = ['close', 'supertrend', 'in_uptrend', 'upperband', 'lowerband']
    print(result[cols])
