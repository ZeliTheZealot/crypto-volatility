from tardis_dev import datasets, get_exchange_details
import logging
import datetime
import dateutil.parser
import pytz
import json

# prevents weird issue
import nest_asyncio
nest_asyncio.apply()

my_api_key = "TD.BDDr5Mkdv9P7jcBv.HGl8KnCzXgfUQSx.GiAyuItybr9u2tg.5DBEOQ-S7tzj-sN.p9Z42Wlj-bksdHl.rpdN"
exchange = "binance"
TOKEN_WANTED = ["BTC"]
start = pytz.UTC.localize(datetime.datetime(2019, 5, 1))
end = pytz.UTC.localize(datetime.datetime(2022, 5, 1)) 
save_destination = (
    exchange + "_" + "_".join(TOKEN_WANTED) + 
    "_from_" + start.strftime("%Y_%m_%d") + 
    "_to_" + end.strftime("%Y_%m_%d") + ".json"
)
exchange_details = get_exchange_details(exchange)
12345678901234567890123456789012345678901234567890123456789012345678901234567890
def is_wanted(pair_name):
    # checks if any string in TOKEN_WANTED is a substring of pair_name
    return any(str.casefold(i) in str.casefold(pair_name) for i in TOKEN_WANTED)

count = 0
symbols_list = []
for item in exchange_details['availableSymbols']:
    available_since = dateutil.parser.isoparse(item['availableSince'])
    def lasts_till_end():
        try:
            return end < dateutil.parser.isoparse(item['availableTo'])
        except KeyError:
            return True
    pair_name = item['id']
    if available_since < start and lasts_till_end() and is_wanted(pair_name):
        symbols_list.append(pair_name)
        count += 1

with open(save_destination, "w") as f:
    json.dump(symbols_list, f)

print(symbols_list) # 43 BTC, 73 if also include ETH in huobi (2 year horizon; 0 if 3 year)
# 14 BTC, 18 if with ETH in Coinbase (3 year)
# 26, 50 in Binance (3 year horizon)
# 24 in OKEX (3 year)
# the above two has high overlap (30 total only)
# bitstamp, bitfinex, bitmex all terrible