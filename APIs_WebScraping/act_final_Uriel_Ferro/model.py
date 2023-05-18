from stock_analyzer import Stock_Analyzer

class Model:

    def __init__(self):
        self.__stock_ticker = None
        self.__send_mail = None
        self.__from_ = None
        self.__to = None
        self.__password = None
        
    def execute_analysis(self, stock_ticker, from_, password, to, send_mail):
        self.__stock_ticker = stock_ticker
        self.__send_mail = send_mail
        self.__from_ = from_
        self.__to = to
        self.__password = password

        self.__stock = Stock_Analyzer(self.__stock_ticker, self.__send_mail, self.__password, self.__from_, self.__to)
        self.__stock.execute_analysis()
