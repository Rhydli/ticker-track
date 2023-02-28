import requests
import pandas as pd
import openpyxl
import api_key
from io import StringIO

# variables
tickers = ['BIL', 'BNDX', 'EGIS', 'EPP', 'EWC', 'EWD', 'EWJ', 'EWL', 'EWU', 'EZU', 'FUTY', 'GIBIX', 'GOVT', 'HYLB', 'IAT', 'IVV', 'IWM', 'IXUS', 'LYFE', 'ONLN', 'PAVE', 'QQQ', 'SKYY', 'SMH', 'SRVR', 'STIP', 'UBER', 'UPST', 'USHY', 'USIG', 'VCIT', 'VCSH', 'VGSH', 'VMBS', 'VNLA', 'VTV', 'XTN']
gets = []
close_prices = []
f_y = 2023
f_m = 1
f_d = 27
from_date = f'{f_y}-{f_m}-{f_d}'

# GET requests to API, store responses
for t in tickers:
    url = f'https://api.marketdata.app/v1/stocks/candles/D/{t}?limit=1&from={from_date}&exchange=mutf&headers=false&format=csv&columns=c&token={api_key.API_KEY}'
    gets.append(requests.request("GET", url))
    
# slice requests strings
for g in gets:
    c = g.text
    #close_prices.append(c[6:-2])
    close_prices.append(c)
        
# write and save date, ticker, and price data to excel file
book = openpyxl.load_workbook('ticker_book.xlsx')
sheet = book['Sheet1']
for i in range(len(close_prices)):
    sheet.cell(row = i + 1, column = 1).value = from_date
t_row = 0   
for t in tickers:
    t_row += 1
    sheet.cell(row=t_row, column=2).value = t
c_row = 0
for c in close_prices:
    c_row += 1
    sheet.cell(row=c_row, column=4).value = c

book.save('ticker_book.xlsx')