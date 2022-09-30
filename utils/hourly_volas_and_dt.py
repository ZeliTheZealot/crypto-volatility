import os
import pandas as pd
import datetime as dt
import math

def hourly_volas_and_dt(symbol, input_folder_name):
    # symbol = 'adabtc'
    file_name = symbol + '.csv.gz'
    path = os.path.join(os.getcwd(), input_folder_name, file_name)
    df = pd.read_csv(path, compression='gzip')

    nums = df.index
    first_day_first_minute = dt.datetime(2019, 5, 1)
    initial_time = dt.datetime.utcfromtimestamp(0)
    theoretical_first_minute = math.floor(
        (first_day_first_minute - initial_time) / dt.timedelta(minutes=1)
    )
    dt_index = pd.to_datetime(theoretical_first_minute + nums, unit="m")
    df.set_index(dt_index, inplace=True)
    squared_returns = df.pow(2)
    volas = squared_returns.groupby(pd.Grouper(freq="H")).sum()
    return volas