import json
import multiprocess

symbols_list_file_name = "binance_BTC_from_2019_05_01_to_2022_04_30.json"
with open(symbols_list_file_name, "r") as f:
    symbols_list = json.load(f)
    
def calculate_returns(symbol):
    import os
    import pandas as pd
    import numpy as np
    import pprint as pp
    import datetime as dt
    import pathlib
    import re
    import json
    import math
    exchange = "binance"
    # data_folder_name = "full_datasets_by_asset_" + exchange
    data_folder_name = "full_datasets_against_btc_" + exchange
    extension = ".gz"
    regex_match_to_strip = "\.csv.gz$"
    # returns_folder_name = "full_returns"
    returns_folder_name = "full_returns_against_btc"
    pattern = "(.*?)_(.*)" # date_ticker regex pattern
    first_day_first_minute = dt.datetime(2019, 5, 1)
    last_day_plus_one_first_minute = dt.datetime(2022, 5, 1)

    date_ticker_regex = re.compile(pattern)
    initial_time = dt.datetime.utcfromtimestamp(0)
    theoretical_first_minute = math.floor(
        (first_day_first_minute - initial_time) / dt.timedelta(minutes=1)
    )
    theoretical_last_minute_plus_one = math.floor(
        (last_day_plus_one_first_minute - initial_time) / dt.timedelta(minutes=1)
    )


    def time_is_in_day(a, timestamp):
        # is timestamp (in microseconds) is within 1 day in the future of a (datetime object)?
        b = dt.datetime.utcfromtimestamp(timestamp/1000000)
        return a <= b < a + dt.timedelta(days=1)

    def data_integrity_test(df, date_ticker_regex):
        date_ticker_regex_result = date_ticker_regex.match(data_name)
        file_name_date = date_ticker_regex_result.group(1)
        file_name_ticker = date_ticker_regex_result.group(2)
        file_name_datetime_object = dt.datetime.strptime(file_name_date, "%Y-%m-%d")

        first_time = df.iloc[0]['timestamp']
        last_time = df.iloc[-1]['timestamp']

        if not pd.Index(df['timestamp']).is_monotonic:
            print("Timestamp is not monotonic for " + data_name)

        if not pd.Index(df['id']).is_monotonic:
            print("ID is not monotonic for " + data_name)

        if not (time_is_in_day(file_name_datetime_object, first_time) and 
                time_is_in_day(file_name_datetime_object, last_time)):
            print("Time is out of range for " + data_name)

        if df.iloc[0]['symbol'] != file_name_ticker:
            print("Ticker is wrong for " + data_name)

    pathlib.Path(os.path.join(os.getcwd(), returns_folder_name)).mkdir(parents=True, exist_ok=True)

    # symbols_list = ['ethbtc'] # debug only

    def keep_latest_trades(df):
        df_latests = df.groupby(['minute', 'side']).timestamp.transform(max)
        df.drop(df[df.timestamp != df_latests].index, inplace=True)
    #     df = df[df.timestamp == df_latests]
        df.drop(columns=['timestamp'], inplace=True)

    def compute_best_sells(df):
        sell_df = df[df.side == 'sell'].drop(columns=['side'])
        sell_latests_priciest = sell_df.groupby(['minute']).price.transform(max)
        sell_df = sell_df[sell_df.price == sell_latests_priciest]
        return sell_df.groupby(['minute']).tail(1) # make each minute have at most one row

    def compute_best_buys(df):
        buy_df = df[df.side == 'buy'].drop(columns=['side'])
        buy_latests_cheapest = buy_df.groupby(['minute']).price.transform(min)
        buy_df = buy_df[buy_df.price == buy_latests_cheapest]
        return buy_df.groupby(['minute']).tail(1) # make each minute have at most one row

    def add_missing_minutes(df):
        return df.set_index('minute').reindex(range(theoretical_first_minute, theoretical_last_minute_plus_one), fill_value=np.NaN).reset_index()

    def fill_in_missing_trades(df):
        df.fillna(method='ffill', inplace=True) # uses best price from previous minute(s)
        df.fillna(method='bfill', inplace=True) # only affects the start of the dataset

    def compute_mid_prices(big_sell_df, big_buy_df):
        big_sell_df = big_sell_df.rename(columns={'price': 'sell'})
        big_buy_df = big_buy_df.drop(columns=['minute'])
        big_buy_df = big_buy_df.rename(columns={'price': 'buy'})
        big_df = pd.concat([big_sell_df, big_buy_df], axis=1)
        big_df['mid'] = (big_df['sell'] + big_df['buy']) / 2
        return big_df.drop(columns=['sell', 'buy'])

    def compute_log_returns(big_df):
        big_df['log_return'] = np.log(big_df['mid'] / big_df['mid'].shift(1))
        big_df.drop(columns=['mid'], inplace=True)
        big_df.fillna(value=0, inplace=True)
    
    dir_name = os.path.join(os.getcwd(), data_folder_name, symbol)
    sell_df_list = []
    buy_df_list = []
    for root, _, file_names in os.walk(dir_name):
        for file_name in file_names:
            if file_name.endswith(extension):
                file_path = os.path.join(root, file_name)
                data_name = re.sub(regex_match_to_strip, '', file_name)
#                 print(f"Walked to {file_path}")
                try:
                    df = pd.read_csv(file_path, compression='gzip')
                    df.drop(columns=['timestamp'], inplace=True)
                    df.rename(columns={'local_timestamp': 'timestamp'}, inplace=True)
                    data_integrity_test(df, date_ticker_regex)
                    
                    df = df[['timestamp', 'side', 'price']]
                    df.loc[:,'minute'] = df.timestamp.apply(lambda x: math.floor(dt.timedelta(microseconds=x) / dt.timedelta(minutes=1)))
                    
                    keep_latest_trades(df)
                    
                    sell_df = compute_best_sells(df)
                    sell_df_list.append(sell_df)
                    
                    buy_df = compute_best_buys(df)
                    buy_df_list.append(buy_df)
                except:
                    print("No data")
    # write stuff for that symbol
    big_sell_df = pd.concat(sell_df_list, ignore_index=True)
    big_buy_df = pd.concat(buy_df_list, ignore_index=True)
    
    big_sell_df = add_missing_minutes(big_sell_df)
    big_buy_df = add_missing_minutes(big_buy_df)
    fill_in_missing_trades(big_sell_df)
    fill_in_missing_trades(big_buy_df)
    
    big_df = compute_mid_prices(big_sell_df, big_buy_df)
    compute_log_returns(big_df)
    
    # structure: returns_folder_name/symbol/this df as csv.gz
    save_file_name = symbol + '.csv.gz'
    save_path = os.path.join(os.getcwd(), returns_folder_name, save_file_name)
    big_df.to_csv(save_path, compression='gzip', index=False)
    print(f"Saved returns for {symbol}")
    
    
num_workers = multiprocess.cpu_count()
with multiprocess.Pool(num_workers) as p:
    p.map(calculate_returns, symbols_list)