# from tardis_dev import datasets
import multiprocess
# import tardis_dev
import logging
import json
import nest_asyncio
nest_asyncio.apply()



logging.basicConfig(level=logging.DEBUG)

# (arbitrary) customisable get_filename (nested structure)



file_name = "binance_BTC_from_2019_05_01_to_2022_04_30.json" 
# yes i didn't change the file name by 1

with open(file_name, "r") as f:
    symbols_list = json.load(f)

def download_data(symbol):
    from tardis_dev import datasets
    dataset_prefix = "full_datasets_by_asset_"
    exchange = "binance"
    my_api_key = "TD.34Q-uNaLfiYDgGrL.ASWs359NTrG3xtC.hJ6BeUBTavJthip.bv88e75OfyB8uWY.Fj9Bir3R4yU8vBo.V8aa"
    from_date_string = "2019-05-01"
    to_date_string = "2022-05-01"
    def file_name_nested(exchange, data_type, date, symbol, format):
        return f"{exchange}/{data_type}/{date.strftime('%Y-%m-%d')}_{symbol}.{format}.gz"
    datasets.download(
        exchange=exchange, 
        data_types=["trades"],
        from_date=from_date_string, # inclusive
        to_date=to_date_string, # non inclusive
        symbols=[symbol],
        api_key=my_api_key,
        download_dir="./" + dataset_prefix + exchange + "/" + symbol, 
        get_filename=file_name_nested,
    )

num_workers = multiprocess.cpu_count()
with multiprocess.Pool(num_workers) as p:
    p.map(download_data, symbols_list)