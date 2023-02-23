import requests
import pandas as pd
import api_key
from io import StringIO

# GET requests to API, store responses
headers = {'Authorization': api_key.API_KEY}
tickers = ['AAPL', 'BIN', 'BNDX'] # tracked tickers
dfs = []
for t in tickers:
    #url = f'https://api.marketdata.app/v1/stocks/candles/D/{t}?from=2023-2-13&to=2023-2-14'
    url = f'https://api.marketdata.app/v1/stocks/candles/D/{t}?from=2023-2-13&to=2023-2-14&token={api_key.API_KEY}'
    #dfs.append(pd.DataFrame(requests.request("GET", url)))
    df = pd.DataFrame(requests.request("GET", url, headers=headers))
    #df = pd.DataFrame([requests.request("GET", url)],
                  #columns=[], index=[])
    print(df)

#print(dfs)

for df in dfs:
    #print(df.at[0, 0])
    #print(df.loc[0])
    pass

'''# create variables
tickers = ['AAPL', 'BIN', 'AAPL'] # tracked tickers
gets = [] # string data
dfs = [] # dataframes
resp_count = 0 # DEBUG

# func to convert response strings into dataframes
def str_to_df(str):
    StringData = StringIO(str.text)
    return pd.read_csv(StringData, sep =";")

# GET requests to API, store responses
for t in tickers:
    url = f'https://api.marketdata.app/v1/stocks/candles/D/{t}?from=2023-2-13&to=2023-2-14'
    gets.append(requests.request("GET", url))
    resp_count += 1 # DEBUG
    print(f'API responses = {resp_count}') # DEBUG

# convert string data
for g in gets:
    dfs.append(str_to_df(g))

print(f'Items in gets =', len(gets)) # DEBUG
print(f'Items in dfs =', len(dfs)) # DEBUG

# write to existing excel file
with pd.ExcelWriter("ticker_book.xlsx",
                    mode = "a",
                    engine = "openpyxl",
                    if_sheet_exists = "overlay") as writer:
    col = -1 # start column
    row = -1 # start row
    for df in dfs:
        col += 0 # increment column
        row += 1 # increment row
        df.to_excel(writer,
                    sheet_name = "Sheet1",
                    startcol = col,
                    startrow = row)'''