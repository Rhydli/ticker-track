import requests
import pandas as pd
import openpyxl
from io import StringIO

# GET request to API endpoint
url = "https://api.marketdata.app/v1/stocks/candles/D/AAPL?from=2023-2-13&to=2023-2-14"
response = requests.request("GET", url)

# convert string into dataframe
StringData = StringIO(response.text)
df = pd.read_csv(StringData, sep =";")
 
# print dataframe
print(df)

# write to existing excel file
with pd.ExcelWriter('pandas_to_excel.xlsx') as writer:
    df.to_excel(writer, sheet_name='sheet1123123')

with pd.ExcelWriter('pandas_to_excel.xlsx') as writer:
   # writer.book = openpyxl.load_workbook('pandas_to_excel.xlsx')
    df.to_excel(writer, sheet_name='new_sheet1')
