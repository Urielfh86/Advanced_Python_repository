from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QFormLayout
from PyQt6.QtWidgets import QRadioButton
from PyQt6.QtWidgets import QButtonGroup
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtCore import Qt

class View(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle('Stock Analyzer by Uriel Ferro')
        self.setFixedSize(480, 250)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.stock_ticker = None
        self.email_sender = None
        self.password = None
        self.destination_email = None
        self.send_mail = None

        self.__general_layout = QVBoxLayout(central_widget)

        self.__create_fields()

    def __create_fields(self):
        self.__form_layout = QFormLayout()
        self.stock_ticker_field = QLineEdit()
        self.__form_layout.addRow('Stock ticker to be analyzed (US only):', self.stock_ticker_field)

        self.__mail_enable_rb = QRadioButton("Enable")
        self.__mail_disable_rb = QRadioButton("Not enable")
        self.__mail_enable_rb.setChecked(True)

        self.__mail_rb_group = QButtonGroup()
        self.__mail_rb_group.addButton(self.__mail_enable_rb)
        self.__mail_rb_group.addButton(self.__mail_disable_rb)

        self.__form_layout.addRow("Do you want to enable sending mails?", self.__mail_enable_rb)
        self.__form_layout.addRow("", self.__mail_disable_rb)

        self.__widget = QLabel("If you have enabled the sending of mails, complete the following fields ▼")
        self.__h_layout = QHBoxLayout()
        self.__h_layout.addWidget(self.__widget)
        self.__form_layout.addRow(self.__h_layout)

        self.mail_sender_field = QLineEdit()
        self.password_field = QLineEdit()
        self.destination_mail_field = QLineEdit()

        self.__form_layout.addRow('e-mail sender:', self.mail_sender_field)
        self.__form_layout.addRow('Password:', self.password_field)
        self.__form_layout.addRow('Destination e-mail:', self.destination_mail_field)
        self.__general_layout.addLayout(self.__form_layout)

        self.__button = QPushButton("Analyze")
        self.__h_button_layout = QHBoxLayout()
        self.__h_button_layout.addStretch()
        self.__h_button_layout.addWidget(self.__button)
        self.__h_button_layout.addStretch()
        self.__general_layout.addLayout(self.__h_button_layout)

    def get_button(self):
        return self.__button

    def get_radio_buttons(self):
        return self.__mail_enable_rb, self.__mail_disable_rb

    def get_users_info(self):
        self.stock_ticker = self.stock_ticker_field.text()
        self.email_sender = self.mail_sender_field.text()
        self.password = self.password_field.text()
        self.destination_email = self.destination_mail_field.text()
        self.send_mail = self.__mail_enable_rb.isChecked()

    def mail_enable_rb_clicked(self):
        self.mail_sender_field.setHidden(False)
        self.password_field.setHidden(False)
        self.destination_mail_field.setHidden(False)
        self.__widget.setHidden(False)

    def mail_disable_rb_clicked(self):
        self.mail_sender_field.setHidden(True)
        self.password_field.setHidden(True)
        self.destination_mail_field.setHidden(True)
        self.__widget.setHidden(True)


        
            

