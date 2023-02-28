import requests
import pandas as pd
import openpyxl
import api_key
from io import StringIO

# variables
tickers = ['BIL', 'BNDX', 'EGIS', 'EPP', 'EWC', 'EWD', 'EWJ', 'EWL', 'EWU', 'EZU', 'FUTY', 'GIBIX', 'GOVT', 'HYLB', 'IAT', 'IVV', 'IWM', 'IXUS', 'LYFE', 'ONLN', 'PAVE', 'QQQ', 'SKYY', 'SMH', 'SRVR', 'STIP', 'UBER', 'UPST', 'USHY', 'USIG', 'VCIT', 'VCSH', 'VGSH', 'VMBS', 'VNLA', 'VTV', 'XTN']
gets = []
dfs = []
f_y = 2023
f_m = 2
f_d = 10
t_y = 2023
t_m = 2
t_d = 11
from_date = f'{f_y}-{f_m}-{f_d}'
to_date = f'{t_y}-{t_m}-{t_d}'

# func to convert response strings into dataframes
def str_to_df(str):
    StringData = StringIO(str.text)
    return pd.read_csv(StringData, sep =";")

# GET requests to API, store responses
for t in tickers:
    url = f'https://api.marketdata.app/v1/stocks/candles/D/{t}?from={from_date}&to={to_date}&headers=false&format=csv&columns=c&token={api_key.API_KEY}'
    gets.append(requests.request("GET", url))

# convert string data
for g in gets:
    dfs.append(str_to_df(g))

# write dataframes to existing excel file
with pd.ExcelWriter("ticker_book.xlsx",
                    mode = "a",
                    engine = "openpyxl",
                    if_sheet_exists = "overlay") as writer:
    c_row = -1
    for df in dfs:
        c_row += 1 
        df.to_excel(writer,
                    sheet_name = "Sheet1",
                    startcol = 2,
                    startrow = c_row)
        
# write date and ticker data to excel file
book = openpyxl.load_workbook('ticker_book.xlsx')
sheet = book['Sheet1']
for i in range(len(dfs)):
    sheet.cell(row = i + 1, column = 1).value = to_date
t_row = 0   
for t in tickers:
    t_row += 1 # increment row
    sheet.cell(row=t_row, column=2).value = t
book.save('ticker_book.xlsx')