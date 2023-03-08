import requests
import openpyxl
import api_key
from PyQt6.QtWidgets import *
from PyQt6 import uic

# variables
#ACTIVE_TICKERS = ['BIL', 'BNDX', 'EGIS', 'EPP', 'EWC', 'EWD', 'EWJ', 'EWL', 'EWU', 'EZU', 'FUTY', 'GIBIX', 'GOVT', 'HYLB', 'IAT', 'IVV', 'IWM', 'IXUS', 'LYFE', 'ONLN', 'PAVE', 'QQQ', 'SKYY', 'SMH', 'SRVR', 'STIP', 'UBER', 'UPST', 'USHY', 'USIG', 'VCIT', 'VCSH', 'VGSH', 'VMBS', 'VNLA', 'VTV', 'XTN']
ACTIVE_TICKERS = ['a']
INACTIVE_TICKERS = ['s']
CLOSE_PRICES = []
FILE_NAME = 'ticker_book.xlsx'
SHEET_NAME = 'Sheet1'
YEAR = 2023
MONTH = 3
DAY = 1
DATE = f'{YEAR}-{MONTH}-{DAY}'

class MyGui(QMainWindow):

    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi('tt.ui', self)
        self.show()
        self.setWindowTitle('Ticker Track')
        self.active_list.addItems(ACTIVE_TICKERS[:])
        self.inactive_list.addItems(INACTIVE_TICKERS[:])
        self.log_msg = ''

        self.add_button.clicked.connect(lambda: self.add(self.ticker_line_edit.text()))
        self.delete_button.clicked.connect(lambda: self.delete(self.ticker_line_edit.text()))
        self.toggle_button.clicked.connect(self.toggle)
        self.run_button.clicked.connect(self.run)

    def add(self, ticker):
        '''TODO check if ticker is valid on api'''
        if ticker and not ticker.isspace():
            if ticker in INACTIVE_TICKERS:
                ACTIVE_TICKERS.append(ticker)
                INACTIVE_TICKERS.remove(ticker)
                self.log_msg = f'{ticker} moved to active tickers.'
                self.ui_refresh()
            elif ticker not in ACTIVE_TICKERS:
                ACTIVE_TICKERS.append(ticker)
                self.log_msg = f'{ticker} added to active tickers.'
                self.ui_refresh()
            else:
                self.log_msg = f'{ticker} already in actively tracked tickers.'
                self.ui_refresh()
        else:
            self.log_msg = 'No Ticker provided.'
            self.ui_refresh()

    def delete(self, ticker):
        if ticker and not ticker.isspace():
            if ticker in ACTIVE_TICKERS:
                INACTIVE_TICKERS.append(ticker)
                ACTIVE_TICKERS.remove(ticker)
                self.log_msg = f'{ticker} moved to inactive tickers.'
                self.ui_refresh()
            else:
                self.log_msg = f'{ticker} not found in actively tracked tickers.'
                self.ui_refresh()
        else:
            self.log_msg = 'No Ticker provided.'
            self.ui_refresh()

    def toggle(self):
        pass

    def ui_refresh(self):
        self.active_list.clear()
        self.active_list.addItems(ACTIVE_TICKERS[:])
        self.inactive_list.clear()
        self.inactive_list.addItems(INACTIVE_TICKERS[:])
        self.console_message.setText(self.log_msg) 

    def run(self):
        # GET requests to API, retuns <class 'requests.models.Response'>
        gets = []
        for t in ACTIVE_TICKERS:
            url = f'https://api.marketdata.app/v1/stocks/candles/D/{t}?limit=1&to={DATE}&headers=false&format=csv&columns=c&token={api_key.API_KEY}'
            gets.append(requests.request("GET", url))
        
        # pull string data from requests
        for g in gets:
            CLOSE_PRICES.append(g.text)

        # write date/ticker/price and save to excel
        book = openpyxl.load_workbook(FILE_NAME)
        sheet = book[SHEET_NAME]
        for i in range(len(CLOSE_PRICES)):
            sheet.cell(row = i + 1, column = 1).value = DATE
        row = 0   
        for t in ACTIVE_TICKERS:
            row += 1
            sheet.cell(row=row, column=2).value = t
        row = 0
        for c in CLOSE_PRICES:
            row += 1
            sheet.cell(row=row, column=4).value = c
        book.save(FILE_NAME)

def main():
    app = QApplication([])
    window = MyGui()
    app.exec()

if __name__ == '__main__':
    main()