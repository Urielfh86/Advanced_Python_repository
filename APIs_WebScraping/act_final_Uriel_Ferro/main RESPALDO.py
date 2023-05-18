# Aplicación que brinda información de acciones de la bolsa de Estados Unidos utilizando la API de Alpha Vantage.
# Obtener la API Key --> https://www.alphavantage.co/support/#api-key

import requests

api_key = "AJLD7AN1I90YRW0B"
stock = "MSFT"

# COMPANY OVERVIEW

function = "OVERVIEW"
url = f'https://www.alphavantage.co/query?function={function}&symbol={stock}&apikey={api_key}'
response = requests.get(url)
data = response.json()
   
name = data["Name"]
country = data["Country"]
description = data["Description"]
pe_ratio = data["PERatio"]
eps = data["EPS"]

print(f"\n{description}")
print(f"\nThe company {name} with origin in {country} has a P/E Ratio of {pe_ratio} and an EPS of {eps}.")

# BALANCE SHEET

function = "BALANCE_SHEET"
url = f'https://www.alphavantage.co/query?function={function}&symbol={stock}&apikey={api_key}'
response = requests.get(url)
data = response.json()

fiscal_year_end = data["annualReports"][0]["fiscalDateEnding"]
activos = float(data["annualReports"][0]["totalAssets"])
pasivos = float(data["annualReports"][0]["totalLiabilities"])
number_of_stocks_in_circulation = int(data["annualReports"][0]["commonStockSharesOutstanding"])
patrimonio = activos - pasivos

print(f"\nIn the fiscal year ending on {fiscal_year_end}, the company {stock} has presented the following balance sheets:")
print(f"\nAssets: USD {activos}")
print(f"\nLiabilities: USD {pasivos}")
print(f"\nEquity: USD {patrimonio}")
print(f"\nShares outstanding: {number_of_stocks_in_circulation}")

# GLOBAL QUOTE

function = "GLOBAL_QUOTE"
url = f'https://www.alphavantage.co/query?function={function}&symbol={stock}&apikey={api_key}'
response = requests.get(url)
data = response.json()

open_price = data["Global Quote"]["02. open"]
previous_close_price = data["Global Quote"]["08. previous close"]
actual_price = data["Global Quote"]["05. price"]
latest_trading_day = data["Global Quote"]["07. latest trading day"]
change_percent = data["Global Quote"]["10. change percent"]
day_high = data["Global Quote"]["03. high"]
day_low = data["Global Quote"]["04. low"]

print(f"\nOn {latest_trading_day}, your shares closed with a price of USD {previous_close_price}.")
print(f"\nToday the shares opened with a price of USD {open_price} and have had a low of USD {day_low} and a high of USD {day_high}.")
print(f"\nThey currently have a price of USD {actual_price}, which translates to a change of {change_percent} from the market's closing day {latest_trading_day}.")

# TIME SERIES 

function = "TIME_SERIES_DAILY_ADJUSTED"
url = f'https://www.alphavantage.co/query?function={function}&symbol={stock}&apikey={api_key}'
respuesta = requests.get(url)
data = respuesta.json()

prices = [ float(value['4. close']) for value in data['Time Series (Daily)'].values() ]
lowest_price_1_year = min(prices)
highest_price_1_year = max(prices)

# ANÁLISIS DE LA ACCIÓN

precio_patrimonio = float(actual_price) / float(patrimonio)

if precio_patrimonio < 1: 
    print("\nThe price-equity ratio is low, indicating that the stock is a good buying opportunity.")
else:
        print("\nThe price-equity ratio is high, indicating that the stock may be overvalued.")

if float(actual_price) < float(lowest_price_1_year) * 0.9:
    print("\nThe current price is well below the 52-week low, it may be a good time to buy.")
elif float(actual_price) > float(highest_price_1_year) * 1.1:
    print("\nThe current price is well above the 52-week high, it may be a good time to sell.")
else:
    print("\nThe current price is within the 52-week range, there is no clear recommendation to buy or sell.")

print("\n¡¡ATTENTION!!")
print("\nIt is important to keep in mind that these analyses are only part of the evaluation of a stock and should not be the sole basis for an investment decision.")