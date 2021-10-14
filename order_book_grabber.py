import sched
import time
import json
import os
from binance.client import Client
import pandas
import logging
import datetime
import warnings

warnings.filterwarnings('ignore')


os.chdir('/Users/uknowit/Binance')

with open('api_key.json') as json_file:
    api_stuff = json.load(json_file)

KEY = api_stuff['api_key']
SECRET = api_stuff['secret'] 

client = Client(KEY, SECRET, {"verify": False, "timeout": 20})

logger = logging.getLogger('hey')
logger.setLevel(10) #Debug level

# initialize df

event_schedule = sched.scheduler(time.time, time.sleep)

def initialize_df():
    print('getting orders first time')
    orders = client.futures_order_book(symbol = "ETHUSDT", limit = 500)
    return pandas.DataFrame.from_dict(orders)


print('program initializing')
df = initialize_df()
print(df)

def grab_order_book(df):
    logger.debug('grabbing order book ...')
    print('grabbing book from func')
    orders = client.futures_order_book(symbol = "ETHUSDT", limit = 500)
    df_append = pandas.DataFrame.from_dict(orders)
    print('appending dataframe')
    df = df.append(df_append)
    event_schedule.enter(30, 1, grab_order_book, argument = (df,))

def save_order_book(df):
    logger.debug('saving df')
    print('saving')
    df.to_csv(f"./klines_{datetime.datetime()}.csv")
    del df
    df = initialize_df()
    event_schedule.enter(60*60*0.1, 5, save_order_book, argument = (df,))
    


event_schedule.enter(1, 30, grab_order_book, argument=(df,))
print('first event entered')
event_schedule.enter(60*60*1, 5, save_order_book, argument =(df,))
print('second event entered')
event_schedule.run()
print('running')