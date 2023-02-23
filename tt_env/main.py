import requests
import pandas as pd
import openpyxl
import api_key
from io import StringIO

# create variables
#tickers = ['BIL', 'BNDX', 'EGIS', 'EPP', 'EWC', 'EWD', 'EWJ', 'EWL', 'EWU', 'EZU', 'FUTY', 'GIBIX', 'GOVT', 'HYLB', 'IAT', 'IVV', 'IWM', 'IXUS', 'LYFE', 'ONLN', 'PAVE', 'QQQ', 'SKYY', 'SMH', 'SRVR', 'STIP', 'UBER', 'UPST', 'USHY', 'USIG', 'VCIT', 'VCSH', 'VGSH', 'VMBS', 'VNLA', 'VTV', 'XTN'] # tracked tickers
tickers = ['BIL', 'BNDX', 'EGIS', 'EPP', 'EWC', 'EWD', 'EWJ', 'EWL', 'EWU', 'EZU']
gets = [] # string data
dfs = [] # dataframes
col = -1 # start column
row = -1 # start row
f_y = 2023
f_m = 2
f_d = 10
t_y = 2023
t_m = 2
t_d = 11
from_date = f'{f_y}-{f_m}-{f_d}'
to_date = f'{t_y}-{t_m}-{t_d}'
resp_count = 0 # DEBUG

# func to convert response strings into dataframes
def str_to_df(str):
    StringData = StringIO(str.text)
    return pd.read_csv(StringData, sep =";")

# GET requests to API, store responses
for t in tickers:
    url = f'https://api.marketdata.app/v1/stocks/candles/D/{t}?from={from_date}&to={to_date}&headers=false&format=csv&columns=c&token={api_key.API_KEY}'
    gets.append(requests.request("GET", url))
    #df = pd.DataFrame(requests.request("GET", url))
    #resp_count += 1 # DEBUG
    #print(f'API responses = {resp_count}') # DEBUG
    #print(df) # DEBUG

# convert string data
for g in gets:
    dfs.append(str_to_df(g))

print(f'Items in gets =', len(gets)) # DEBUG
print(f'Items in dfs =', len(dfs)) # DEBUG

# write dataframes to existing excel file
with pd.ExcelWriter("ticker_book.xlsx",
                    mode = "a",
                    engine = "openpyxl",
                    if_sheet_exists = "overlay") as writer:
    
    for t in tickers:
        pass

    for df in dfs:
        col += 0 # increment column
        row += 1 # increment row
        df.to_excel(writer,
                    sheet_name = "Sheet1",
                    startcol = col+3,
                    startrow = row)
        
# write date and ticker data to excel file
book = openpyxl.load_workbook('ticker_book.xlsx')
sheet = book['Sheet1']
for i in range(len(dfs)):
    sheet.cell(row=i+1, column=1).value = to_date
    for t in tickers:
        sheet.cell(row=i+1, column=2).value = t
book.save('ticker_book.xlsx')


#sheet['c1'] = 1 # cell notation
#sheet.cell(row=2, column=2).value = 2 # row and column notation

# old data
'''wb = openpyxl.load_workbook('ticker_book.xlsx')
sheet = wb['Sheet1']
sheet['A1'] = 'hello world'
wb.save('ticker_book.xlsx')'''

'''StringData = StringIO(response.text)
df = pd.read_csv(StringData, sep =";")'''