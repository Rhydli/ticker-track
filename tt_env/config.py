import configparser
import ast
import os
from datetime import date
from datetime import timedelta
from dateutil.parser import parse

def update_cfg():
    #convert list data back into str and save into ini file
    config.set('TICKERS', 'active_tickers', str(ACTIVE_TICKERS))
    config.set('TICKERS', 'inactive_tickers', str(INACTIVE_TICKERS))
    with open('tt_config.ini', 'w') as configfile:
        config.write(configfile)

#file data
SERVER_PATH = '\\\\dt-file\\Software\\Test\\'
FILE_NAME = 'ticker_book.xlsx'
SHEET_NAME = 'Sheet1'
FILE_PATH = os.path.join(SERVER_PATH, FILE_NAME) 
#variables to populate previous day on launch
today = date.today()
yesterday = today - timedelta(days = 1)
YEAR = (str(yesterday.year))
MONTH = (str(yesterday.month))
DAY = (str(yesterday.day))
#store config file in memory on load for script use
config = configparser.ConfigParser()
config.read('tt_config.ini')
#config parser stores all values as strings, convert to lists
ACTIVE_TICKERS = ast.literal_eval(config['TICKERS']['active_tickers'])
INACTIVE_TICKERS = ast.literal_eval(config['TICKERS']['inactive_tickers'])

