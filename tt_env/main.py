import requests

url = "https://api.marketdata.app/v1/stocks/candles/D/AAPL?from=2023-2-13&to=2023-2-14"

response = requests.request("GET", url)

print(response.text)