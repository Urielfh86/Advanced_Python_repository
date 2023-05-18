# Obtener la API Key --> https://www.alphavantage.co/support/#api-key

import requests
from mail_sender import email_sender
import time

class Stock_Analyzer():

    __api_key = "AJLD7AN1I90YRW0B"

    def __init__(self, stock_ticker, send_mail, password, from_ = None, to = None):
        self.__stock_ticker = stock_ticker
        self.__send_mail = send_mail
        self.__password = password

        self.__name = None
        self.__country = None
        self.__description = None
        self.__pe_ratio = None
        self.__eps = None

        self.__fiscal_year_end = None
        self.__activos = None
        self.__pasivos = None
        self.__number_of_stocks_in_circulation = None
        self.__patrimonio = None

        self.__open_price = None
        self.__previous_close_price = None
        self.__actual_price = None
        self.__latest_trading_day = None
        self.__change_percent = None
        self.__day_high = None
        self.__day_low = None

        self.__lowest_price_1_year = None
        self.__highest_price_1_year = None

        self.__from_ = from_
        self.__to = to
        self.__subject = f"Resultado del análisis de {self.__stock_ticker}"
        self.__message = None

    def __company_overview(self):
        function = "OVERVIEW"
        url = f'https://www.alphavantage.co/query?function={function}&symbol={self.__stock_ticker}&apikey={Stock_Analyzer.__api_key}'
        response = requests.get(url)
        data = response.json()
        
        self.__name = data["Name"]
        self.__country = data["Country"]
        self.__description = data["Description"]
        self.__pe_ratio = data["PERatio"]
        self.__eps = data["EPS"]

        time.sleep(1)
        print(f"\n{self.__description}")
        print(f"\nThe company {self.__name} with origin in {self.__country} has a P/E Ratio of {self.__pe_ratio} and an EPS of {self.__eps}.")
    
    def __balance_sheet(self):
        function = "BALANCE_SHEET"
        url = f'https://www.alphavantage.co/query?function={function}&symbol={self.__stock_ticker}&apikey={Stock_Analyzer.__api_key}'
        response = requests.get(url)
        data = response.json()

        self.__fiscal_year_end = data["annualReports"][0]["fiscalDateEnding"]
        self.__activos = float(data["annualReports"][0]["totalAssets"])
        self.__pasivos = float(data["annualReports"][0]["totalLiabilities"])
        self.__number_of_stocks_in_circulation = int(data["annualReports"][0]["commonStockSharesOutstanding"])
        self.__patrimonio = self.__activos - self.__pasivos

        time.sleep(1)
        print(f"\nIn the fiscal year ending on {self.__fiscal_year_end}, the company {self.__stock_ticker} has presented the following balance sheets:")
        print(f"\nAssets: USD {self.__activos}")
        print(f"\nLiabilities: USD {self.__pasivos}")
        print(f"\nEquity: USD {self.__patrimonio}")
        print(f"\nShares outstanding: {self.__number_of_stocks_in_circulation}")

    def __global_quote(self):
        function = "GLOBAL_QUOTE"
        url = f'https://www.alphavantage.co/query?function={function}&symbol={self.__stock_ticker}&apikey={Stock_Analyzer.__api_key}'
        response = requests.get(url)
        data = response.json()

        self.__open_price = data["Global Quote"]["02. open"]
        self.__previous_close_price = data["Global Quote"]["08. previous close"]
        self.__actual_price = data["Global Quote"]["05. price"]
        self.__latest_trading_day = data["Global Quote"]["07. latest trading day"]
        self.__change_percent = data["Global Quote"]["10. change percent"]
        self.__day_high = data["Global Quote"]["03. high"]
        self.__day_low = data["Global Quote"]["04. low"]
        
        time.sleep(1)
        print(f"\nOn {self.__latest_trading_day}, your shares closed with a price of USD {self.__previous_close_price}.")
        print(f"\nToday the shares opened with a price of USD {self.__open_price} and have had a low of USD {self.__day_low} and a high of USD {self.__day_high}.")
        print(f"\nThey currently have a price of USD {self.__actual_price}, which translates to a change of {self.__change_percent} from the market's closing day {self.__latest_trading_day}.")

    def __time_series(self):
        function = "TIME_SERIES_DAILY_ADJUSTED"
        url = f'https://www.alphavantage.co/query?function={function}&symbol={self.__stock_ticker}&apikey={Stock_Analyzer.__api_key}'
        respuesta = requests.get(url)
        data = respuesta.json()

        prices = [ float(value['4. close']) for value in data['Time Series (Daily)'].values() ]
        self.__lowest_price_1_year = min(prices)
        self.__highest_price_1_year = max(prices)

    def execute_analysis(self):
        self.__company_overview()
        self.__balance_sheet()
        self.__global_quote()
        self.__time_series()

        intrinsic_value = int(self.__number_of_stocks_in_circulation) * float(self.__actual_price)
        precio_patrimonio = float(self.__actual_price) / float(self.__patrimonio)

        if precio_patrimonio < 1: 
            print("\nThe price-equity ratio is low, indicating that the stock is a good buying opportunity.")
        else:
            print("\nThe price-equity ratio is high, indicating that the stock may be overvalued.")

        if float(self.__actual_price) < float(self.__lowest_price_1_year) * 0.9:
            print("\nThe current price is well below the 52-week low, it may be a good time to buy.")
        elif float(self.__actual_price) > float(self.__highest_price_1_year) * 1.1:
            print("\nThe current price is well above the 52-week high, it may be a good time to sell.")
        else:
            print("\nThe current price is within the 52-week range, there is no clear recommendation to buy or sell.")

        if float(intrinsic_value) > float(self.__patrimonio):
            print("\nThe stock is trading above its intrinsic value and is not recommended for purchase at this time.")
        elif float(intrinsic_value) == float(self.__patrimonio):
            print("\nThe stock is trading equal to its intrinsic value, so it is a neutral decision if you want to buy at this time.")
        else:
            print("\nThe stock is trading below its intrinsic value and is therefore recommended for purchase at this time.")
         
        print("\n¡¡ATTENTION!!")
        print("\nIt is important to keep in mind that these analyses are only part of the evaluation of a stock and should not be the sole basis for an investment decision.")

        if self.__send_mail:
            try:
                self.__message = f"{self.__description}\n\nThe company {self.__name} with origin in {self.__country} has a P/E Ratio of {self.__pe_ratio} and an EPS of {self.__eps}.\n\nIn the fiscal year ending on {self.__fiscal_year_end}, the company {self.__stock_ticker} has presented the following balance sheets:\n\nAssets: USD {self.__activos}\n\nLiabilities: USD {self.__pasivos}\n\nEquity: USD {self.__patrimonio}\n\nShares outstanding: {self.__number_of_stocks_in_circulation}\n\nOn {self.__latest_trading_day}, your shares closed with a price of USD {self.__previous_close_price}.\n\nToday the shares opened with a price of USD {self.__open_price} and have had a low of USD {self.__day_low} and a high of USD {self.__day_high}.\n\nThey currently have a price of USD {self.__actual_price}, which translates to a change of {self.__change_percent} from the market's closing day {self.__latest_trading_day}."
                email_sender(self.__from_, self.__to, self.__subject, self.__message, self.__password)
                print("\nMAIL SENT CORRECTLY.")
            except:
                print("\nERROR WHEN TRYING TO SEND THE E-MAIL WITH THE INFORMATION.")
        else:
            print("\nMAIL SENDING DISABLED.")




