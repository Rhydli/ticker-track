import requests
import openpyxl
import api_key

# variables
ACTIVE_TICKERS = ['BIL', 'BNDX', 'EGIS', 'EPP', 'EWC', 'EWD', 'EWJ', 'EWL', 'EWU', 'EZU', 'FUTY', 'GIBIX', 'GOVT', 'HYLB', 'IAT', 'IVV', 'IWM', 'IXUS', 'LYFE', 'ONLN', 'PAVE', 'QQQ', 'SKYY', 'SMH', 'SRVR', 'STIP', 'UBER', 'UPST', 'USHY', 'USIG', 'VCIT', 'VCSH', 'VGSH', 'VMBS', 'VNLA', 'VTV', 'XTN']
#ACTIVE_TICKERS = ['GIBIX', 'IAT', 'PAVE', 'SMH', 'USHY', 'USIG']
INACTIVE_TICKERS = []
CLOSE_PRICES = []
FILE_NAME = 'ticker_book.xlsx'
SHEET_NAME = 'Sheet1'
YEAR = 2023
MONTH = 3
DAY = 1
DATE = f'{YEAR}-{MONTH}-{DAY}'

'''pass in non constant lists for active and inactive tickers
which are made from CONSTANT all tickers'''

def get_close_prices():
    # GET requests to API, store responses
    gets = []
    for t in ACTIVE_TICKERS:
        url = f'https://api.marketdata.app/v1/stocks/candles/D/{t}?limit=1&to={DATE}&headers=false&format=json&columns=c&token={api_key.API_KEY}'
        gets.append(requests.request("GET", url))
        #print(requests.request("GET", url))
    
    # slice requests strings
    for g in gets:
        CLOSE_PRICES.append(g.text)

def export_data():
    # write date/ticker/price and save to excel
    book = openpyxl.load_workbook(FILE_NAME)
    sheet = book[SHEET_NAME]
    for i in range(len(CLOSE_PRICES)):
        sheet.cell(row = i + 1, column = 1).value = DATE
    row = 0   
    for t in ACTIVE_TICKERS:
        row += 1
        sheet.cell(row=row, column=2).value = t
    row = 0
    for c in CLOSE_PRICES:
        row += 1
        sheet.cell(row=row, column=4).value = c

    book.save(FILE_NAME)

get_close_prices()
export_data()
