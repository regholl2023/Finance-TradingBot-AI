import yfinance as yf
import numpy as np


def supertrend(df, period, multiplier, column_prefix):
    df = df.copy()

    df[f'{column_prefix}_tr0'] = abs(df['High'] - df['Low'])
    df[f'{column_prefix}_tr1'] = abs(df['High'] - df['Close'].shift())
    df[f'{column_prefix}_tr2'] = abs(df['Low'] - df['Close'].shift())
    df[f'{column_prefix}_tr'] = df[[f'{column_prefix}_tr0', f'{
        column_prefix}_tr1', f'{column_prefix}_tr2']].max(axis=1)
    df[f'{column_prefix}_atr'] = df[f'{
        column_prefix}_tr'].rolling(period).mean()

    df[f'{column_prefix}_upperband'] = (
        df['High'] + df['Low']) / 2 + (multiplier * df[f'{column_prefix}_atr'])
    df[f'{column_prefix}_lowerband'] = (
        df['High'] + df['Low']) / 2 - (multiplier * df[f'{column_prefix}_atr'])
    df[f'{column_prefix}_in_uptrend'] = True

    for i in range(1, len(df)):
        current_close = df['Close'].iloc[i]
        prev_upperband = df[f'{column_prefix}_upperband'].iloc[i-1]
        prev_lowerband = df[f'{column_prefix}_lowerband'].iloc[i-1]
        prev_in_uptrend = df[f'{column_prefix}_in_uptrend'].iloc[i-1]

        if current_close > prev_upperband:
            df.loc[df.index[i], f'{column_prefix}_in_uptrend'] = True
        elif current_close < prev_lowerband:
            df.loc[df.index[i], f'{column_prefix}_in_uptrend'] = False
        else:
            df.loc[df.index[i], f'{
                column_prefix}_in_uptrend'] = prev_in_uptrend

            if prev_in_uptrend and df[f'{column_prefix}_lowerband'].iloc[i] < \
                    prev_lowerband:
                df.loc[df.index[i], f'{
                    column_prefix}_lowerband'] = prev_lowerband
            if not prev_in_uptrend and \
                    df[f'{column_prefix}_upperband'].iloc[i] > prev_upperband:
                df.loc[df.index[i], f'{
                    column_prefix}_upperband'] = prev_upperband

    df[f'{column_prefix}_supertrend'] = np.where(
        df[f'{column_prefix}_in_uptrend'],
        df[f'{column_prefix}_lowerband'],
        df[f'{column_prefix}_upperband']
    )

    return df[[f'{column_prefix}_supertrend', f'{column_prefix}_in_uptrend']]


# Download sample data
symbol = "RANI"  # Decling Stock currently
data = yf.download(symbol, start="2022-01-01", end="2023-01-01")

# Calculate SuperTrend with different parameters
st1 = supertrend(data, period=12, multiplier=3, column_prefix='st1')
st2 = supertrend(data, period=10, multiplier=1, column_prefix='st2')
st3 = supertrend(data, period=11, multiplier=2, column_prefix='st3')

# Merge the results with the original data
data = data.join([st1, st2, st3])

print(data.head(15))
