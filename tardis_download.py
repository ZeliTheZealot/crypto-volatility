from tardis_dev import datasets, get_exchange_details
import logging
import json
# prevents weird issue
import nest_asyncio
nest_asyncio.apply()

# for 2022-04-14 to 29 only
# my_api_key = "TD.BDDr5Mkdv9P7jcBv.HGl8KnCzXgfUQSx.GiAyuItybr9u2tg.5DBEOQ-S7tzj-sN.p9Z42Wlj-bksdHl.rpdN"
my_api_key = "TD.34Q-uNaLfiYDgGrL.ASWs359NTrG3xtC.hJ6BeUBTavJthip.bv88e75OfyB8uWY.Fj9Bir3R4yU8vBo.V8aa"
from_date_string = "2019-05-01"
to_date_string = "2022-05-01"

# comment out to disable debug logs
logging.basicConfig(level=logging.DEBUG)

# default get_filename (flat structure)
def default_file_name(exchange, data_type, date, symbol, format):
    return f"{exchange}_{data_type}_{date.strftime('%Y-%m-%d')}_{symbol}.{format}.gz"

# (arbitrary) customisable get_filename (nested structure)
def file_name_nested(exchange, data_type, date, symbol, format):
    return f"{exchange}/{data_type}/{date.strftime('%Y-%m-%d')}_{symbol}.{format}.gz"

exchange = "binance"
file_name = "binance_BTC_from_2019_05_01_to_2022_04_30.json" # yes i didn't change the file name by 1
with open(file_name, "r") as f:
    symbols_list = json.load(f)

for symbol in symbols_list:
    datasets.download(
        exchange=exchange, # one of https://api.tardis.dev/v1/exchanges with supportsDatasets:true - use 'id' value
        data_types=["trades"],
        from_date=from_date_string, # inclusive
        to_date=to_date_string, # non inclusive
        symbols=[symbol],
        api_key=my_api_key,
        download_dir="./datasets_by_asset_" + exchange + "/" + symbol, # default = './datasets'
        get_filename=file_name_nested,
    )