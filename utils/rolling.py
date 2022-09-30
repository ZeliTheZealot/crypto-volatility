import pandas as pd
import datetime as dt

def rolling(df):
    blocks = int(dt.timedelta(days=1) / dt.timedelta(hours=1)) # 24
    result = df.rolling(blocks).sum()
    result.dropna(inplace=True)
    result.index += dt.timedelta(days=-1, hours=1)
    return result