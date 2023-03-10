import configparser
import ast
import datetime

#variables to populate current day on launch
today = datetime.datetime.now()
YEAR = (str(today.year))
MONTH = (str(today.month))
DAY = (str(today.day))
#store config file in memory on load for script use
config = configparser.ConfigParser()
config.read('tt_config.ini')
#config parser stores all values as strings, convert to lists
ACTIVE_TICKERS = ast.literal_eval(config['TICKERS']['active_tickers'])
INACTIVE_TICKERS = ast.literal_eval(config['TICKERS']['inactive_tickers'])

def update_cfg():
    #convert list data back into str and save into ini file
    config.set('TICKERS', 'active_tickers', str(ACTIVE_TICKERS))
    config.set('TICKERS', 'inactive_tickers', str(INACTIVE_TICKERS))
    with open('tt_config.ini', 'w') as configfile:
        config.write(configfile)
