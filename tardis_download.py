from tardis_dev import datasets, get_exchange_details
import logging
import os
import pandas as pd
import pprint as pp
import datetime
import dateutil.parser
import pytz
import gzip
import re
import json
# prevents weird issue
import nest_asyncio
nest_asyncio.apply()

my_api_key = "TD.BDDr5Mkdv9P7jcBv.HGl8KnCzXgfUQSx.GiAyuItybr9u2tg.5DBEOQ-S7tzj-sN.p9Z42Wlj-bksdHl.rpdN"

# comment out to disable debug logs
logging.basicConfig(level=logging.DEBUG)

# default get_filename (flat structure)
def default_file_name(exchange, data_type, date, symbol, format):
    return f"{exchange}_{data_type}_{date.strftime('%Y-%m-%d')}_{symbol}.{format}.gz"

# (arbitrary) customisable get_filename (nested structure)
def file_name_nested(exchange, data_type, date, symbol, format):
    return f"{exchange}/{data_type}/{date.strftime('%Y-%m-%d')}_{symbol}.{format}.gz"

exchange = "binance"
file_name = "binance_BTC_from_2019_05_01_to_2022_04_30.json"
with open(file_name, "r") as f:
    symbols_list = json.load(f)

for symbol in symbols_list:
    datasets.download(
        exchange=exchange, # one of https://api.tardis.dev/v1/exchanges with supportsDatasets:true - use 'id' value
        data_types=["trades"],
        from_date="2022-04-14", # inclusive
        to_date="2022-04-29", # non inclusive
        symbols=[symbol],
        api_key=my_api_key,
        download_dir="./datasets_by_asset_" + exchange + "/" + symbol, # default = './datasets'
        get_filename=file_name_nested,
    )