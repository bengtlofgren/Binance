''' Python file for making moneys'''
import json
import os
from binance.client import Client
import datetime

import pandas

import warnings
warnings.filterwarnings('ignore')

os.chdir('/Users/uknowit/Binance')

with open('api_key.json') as json_file:
    api_stuff = json.load(json_file)

KEY = api_stuff['api_key']
SECRET = api_stuff['secret'] 

client = Client(KEY, SECRET, {"verify": False, "timeout": 20})

# depth = client.get_order_book(symbol = 'ETHUSDT')

class Klines():
    def __init__(self, klines_list):
        self.list = klines_list
        self.dict = self.to_dict(self.list)
        self.df = self.to_df(self.list) 
    
    def to_dict(self, klines):
        ''' Creates a dict of dicts with the kline key = open_time of the kline'''

        kline_dict = dict()
        for kline in klines:
            kline_to_add = {
                kline[0]: {
                    "open_time": kline[0],
                    "open": kline[1],
                    "high": kline[2],
                    "low": kline[3],
                    "close": kline[4],
                    "volume": kline[5],
                    "close_time": kline[6],
                    "quote_asset_volume": kline[7],
                    "no_of_trades": kline[8],
                    "taker_buy_base_asset_volume": kline[9],
                    "taker_buy_quote_asset_volume": kline[10],
                }
            }
            kline_dict.update(kline_to_add)
        return kline_dict

    def to_df(self, klines):
        kline_columns = [
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_asset_volume",
                "no_of_trades",
                "taker_buy_base_asset_volume",
                "taker_buy_quote_asset_volume",
                "ignore"
                ]
        df = pandas.DataFrame(klines, columns = kline_columns)

        return df




klines1 = Klines(client.futures_klines(symbol = 'ETHUSDT', interval = client.KLINE_INTERVAL_15MINUTE, limit = 1000))

df = klines1.df

df.drop(columns="ignore", inplace = True)
df.open_date = pandas.to_datetime(df.open_time)
df.head()

df.to_csv(f"./klines_{datetime.date.today()}.csv")