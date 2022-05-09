import os
import pandas as pd
import pprint as pp
import datetime
import gzip
import re
import json

symbols_list_file_name = "binance_BTC_from_2019_05_01_to_2022_04_30.json"
with open(symbols_list_file_name, "r") as f:
    symbols_list = json.load(f)

exchange = "binance"
data_folder_name = "datasets_by_asset_" + exchange
# dir_name = os.path.join(os.getcwd(), data_folder_name)
extension = ".gz"
regex_match_to_strip = "\.csv.gz$"
returns_folder_name = "returns"
pattern = "(.*?)_(.*)" # date_ticker regex pattern

date_ticker_regex = re.compile(pattern)

def time_is_in_day(a, timestamp):
    # checks if timestamp (in microseconds) is within 1 day in the future of a (a datetime object)
    b = datetime.datetime.utcfromtimestamp(timestamp/1000000)
    return a <= b < a + datetime.timedelta(days=1)

def data_integrity_test(df, date_ticker_regex):
    date_ticker_regex_result = date_ticker_regex.match(data_name)
    file_name_date = date_ticker_regex_result.group(1)
    file_name_ticker = date_ticker_regex_result.group(2)
    file_name_datetime_object = datetime.datetime.strptime(file_name_date, "%Y-%m-%d")
    
    first_time = df.iloc[0]['timestamp']
    last_time = df.iloc[-1]['timestamp']

    if not pd.Index(df['timestamp']).is_monotonic:
        print("Timestamp is not monotonic for " + data_name)

    if not pd.Index(df['id']).is_monotonic:
        print("ID is not monotonic for " + data_name)

    if not (time_is_in_day(file_name_datetime_object, first_time) and time_is_in_day(file_name_datetime_object, last_time)):
        print("Time is out of range for " + data_name)
    
    if df.iloc[0]['symbol'] != file_name_ticker:
        print("Ticker is wrong for " + data_name)

# data_dict = {}
pathlib.Path(os.path.join(os.getcwd(), returns_folder_name)).mkdir(parents=True, exist_ok=True)
date_ticker_regex = re.compile(pattern)

def data_integrity_test(df, date_ticker_regex):
    date_ticker_regex_result = date_ticker_regex.match(data_name)
    file_name_date = date_ticker_regex_result.group(1)
    file_name_ticker = date_ticker_regex_result.group(2)
    file_name_datetime_object = datetime.datetime.strptime(file_name_date, "%Y-%m-%d")
    
    first_time = df.iloc[0]['timestamp']
    last_time = df.iloc[-1]['timestamp']

    if not pd.Index(df['timestamp']).is_monotonic:
        print("Timestamp is not monotonic for " + data_name)

    if not pd.Index(df['id']).is_monotonic:
        print("ID is not monotonic for " + data_name)

    if not (time_is_in_day(file_name_datetime_object, first_time) and time_is_in_day(file_name_datetime_object, last_time)):
        print("Time is out of range for " + data_name)
    
    if df.iloc[0]['symbol'] != file_name_ticker:
        print("Ticker is wrong for " + data_name)

for symbol in symbols_list:
    dir_name = os.path.join(os.getcwd(), data_folder_name, symbol)
    sell_df_list = []
    buy_df_list = []
    for root, _, file_names in os.walk(dir_name):
        for file_name in file_names:
            if file_name.endswith(extension):
                file_path = os.path.join(root, file_name)
                data_name = re.sub(regex_match_to_strip, '', file_name)
                print(f"Walked to {file_path}")
                try:
                    df = pd.read_csv(file_path, compression='gzip')
                    data_integrity_test(df, date_ticker_regex)
                    
                    df = df[['timestamp', 'side', 'price']]
                    df.loc[:,'minute'] = df.timestamp.apply(lambda x: math.floor(dt.timedelta(microseconds=x) / dt.timedelta(minutes=1)))
                    
                    df_latests = df.groupby(['minute', 'side']).timestamp.transform(max)
                    df = df[df.timestamp == df_latests]
                    
                    sell_df = df[df.side == 'sell']
                    sell_latests_priciest = sell_df.groupby(['minute', 'side']).price.transform(max)
                    sell_df = sell_df[sell_df.price == sell_latests_priciest]
                    sell_df = sell_df.groupby(['minute']).tail(1) # make each minute have at most one row
                    sell_df_list.append(sell_df)
                    
                    buy_df = df[df.side == 'buy']
                    buy_latests_cheapest = buy_df.groupby(['minute', 'side']).price.transform(min)
                    buy_df = buy_df[buy_df.price == buy_latests_cheapest]
                    buy_df = buy_df.groupby(['minute']).tail(1) # make each minute have at most one row
                    buy_df_list.append(buy_df)
                except:
                    print("No data")