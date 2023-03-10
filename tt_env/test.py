import requests
import api_key

ticker = 'AAPL'

url = f'https://api.marketdata.app/v1/stocks/quotes/{ticker}/?columns=s&token={api_key.API_KEY}'
response = requests.request("GET", url)

print(response.json()['s'])
print(bool(response.json()['s'] == 'ok'))

string = 'aapl'
print(string.upper())


