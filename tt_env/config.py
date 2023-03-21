import configparser
import ast
from datetime import date
from datetime import timedelta
from dateutil.parser import parse


def update_cfg(): # convert list data back into str and save into ini file
    config.set('TICKERS', 'active_tickers', str(ACTIVE_TICKERS))
    config.set('TICKERS', 'inactive_tickers', str(INACTIVE_TICKERS))
    with open('tt_config.ini', 'w') as configfile:
        config.write(configfile)


def isfloat(s): # return true if passed str can be converted into a float
        try:
            float(s)
            return True
        except ValueError:
            return False


config = configparser.ConfigParser()
config.read('tt_config.ini') # store config file in memory on load for script use

# excel config
BOOK_NAME = config['FILE']['book']
SHEET_NAME = config['FILE']['sheet']

# config parser stores all values as strings, convert to lists
ACTIVE_TICKERS = ast.literal_eval(config['TICKERS']['active_tickers'])
INACTIVE_TICKERS = ast.literal_eval(config['TICKERS']['inactive_tickers'])

# variables to populate previous day on launch
today = date.today()
yesterday = today - timedelta(days = 1)
YEAR = (str(yesterday.year))
MONTH = (str(yesterday.month))
DAY = (str(yesterday.day))