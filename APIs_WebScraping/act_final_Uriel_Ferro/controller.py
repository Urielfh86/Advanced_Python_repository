class Controller:
    def __init__(self, view, model):
        self.__view = view
        self.__model = model
        self.__connect_signals()

    def __connect_signals(self):
        button = self.__view.get_button()
        mail_enable_rb, mail_disable_rb = self.__view.get_radio_buttons()
        button.clicked.connect(self.__view.get_users_info)
        button.clicked.connect(self.__analyze_stock)
        mail_enable_rb.clicked.connect(self.__view.mail_enable_rb_clicked)
        mail_disable_rb.clicked.connect(self.__view.mail_disable_rb_clicked)

    def __analyze_stock(self):
        self.__model.execute_analysis(self.__view.stock_ticker, self.__view.email_sender, self.__view.password, self.__view.destination_email, self.__view.send_mail)
        
    
    

