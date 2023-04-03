# Standard library imports
from configparser import ConfigParser
from datetime import date, timedelta, datetime

# Third-party imports
from dateutil.parser import parse
import ast


def generate_date_range(from_date, to_date):
    # validate input dates
    try:
        from_day = datetime.strptime(from_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Invalid from date: {from_date}")
    try:
        to_day = datetime.strptime(to_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Invalid to date: {to_date}")

    # generate a list of dates between the start and end dates
    date_range = [from_day + timedelta(days=x) for x in range((to_day-from_day).days + 1)]

    # format each date in the range as a YYYY-MM-DD string
    formatted_dates = [d.strftime("%Y-%m-%d") for d in date_range]

    # return the formatted dates
    return formatted_dates


# convert list data back into str and save into ini file
def update_cfg():
    config.set('TICKERS', 'active_tickers', str(ACTIVE_TICKERS))
    config.set('TICKERS', 'inactive_tickers', str(INACTIVE_TICKERS))
    with open('tt_config.ini', 'w') as configfile:
        config.write(configfile)


# return true if passed str can be converted into a float
def isfloat(s):
        try:
            float(s)
            return True
        except ValueError:
            return False


# store config file in memory on load for script use
config = ConfigParser()
config.read('tt_config.ini')

# excel config
BOOK_NAME = config['FILE']['book']
SHEET_NAME = config['FILE']['sheet']

# configparser stores all values as strings, convert to lists
ACTIVE_TICKERS = ast.literal_eval(config['TICKERS']['active_tickers'])
INACTIVE_TICKERS = ast.literal_eval(config['TICKERS']['inactive_tickers'])

# variables to populate previous day on launch
today = date.today()
yesterday = today - timedelta(days = 1)
YEAR = (str(yesterday.year))
MONTH = (str(yesterday.month))
DAY = (str(yesterday.day))