import requests
import openpyxl
import api_key
import config as cfg
from PyQt6.QtWidgets import *
from PyQt6 import uic

class MyGui(QMainWindow):

    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi('tt.ui', self)
        self.show()
        self.setWindowTitle('Ticker Track')
        self.active_list.addItems(cfg.ACTIVE_TICKERS[:])
        self.inactive_list.addItems(cfg.INACTIVE_TICKERS[:])
        self.log_msg = ''
        self.year_line_edit.setText(cfg.YEAR)
        self.month_line_edit.setText(cfg.MONTH)
        self.day_line_edit.setText(cfg.DAY)
        self.add_button.clicked.connect(lambda: self.add(self.ticker_line_edit.text().upper()))
        self.delete_button.clicked.connect(lambda: self.delete(self.ticker_line_edit.text().upper()))
        self.toggle_button.clicked.connect(self.toggle)
        self.run_button.clicked.connect(self.run)

    def add(self, ticker):
        if ticker and not ticker.isspace():
            url = f'https://api.marketdata.app/v1/stocks/quotes/{ticker}/?token={api_key.API_KEY}'
            #response = requests.request("GET", url)
            response = True #bypass gets
            try:
                #if bool(response.json()['s'] == 'ok'):
                if response: #bypass gets
                    if ticker in cfg.INACTIVE_TICKERS:
                        cfg.ACTIVE_TICKERS.append(ticker)
                        cfg.INACTIVE_TICKERS.remove(ticker)
                        cfg.update_cfg()
                        self.log_msg = f'"{ticker}" moved to active tickers.'
                        self.ui_refresh()
                    elif ticker not in cfg.ACTIVE_TICKERS:
                        cfg.ACTIVE_TICKERS.append(ticker)
                        cfg.update_cfg()
                        self.log_msg = f'"{ticker}" added to active tickers.'
                        self.ui_refresh()
                    else:
                        self.log_msg = f'"{ticker}" already in actively tracked tickers.'
                        self.ui_refresh()
                else:
                    self.log_msg = f'API Response: {response.json()["errmsg"]}, Ticker: "{ticker}"'
                    self.ui_refresh()
            except:
                '''log errors'''
                self.log_msg = f'Exception: {response.json()["errmsg"]}'
                self.ui_refresh()
        else:
            self.log_msg = 'No Ticker provided.'
            self.ui_refresh()

    def delete(self, ticker):
        if ticker and not ticker.isspace():
            if ticker in cfg.ACTIVE_TICKERS:
                cfg.INACTIVE_TICKERS.append(ticker)
                cfg.ACTIVE_TICKERS.remove(ticker)
                cfg.update_cfg()
                self.log_msg = f'"{ticker}" moved to inactive tickers.'
                self.ui_refresh()
            else:
                self.log_msg = f'"{ticker}" not found in actively tracked tickers.'
                self.ui_refresh()
        else:
            self.log_msg = 'No Ticker provided.'
            self.ui_refresh()

    def toggle(self):
        cfg.update_cfg()
        self.ui_refresh()
        
    def ui_refresh(self):
        self.active_list.clear()
        self.active_list.addItems(cfg.ACTIVE_TICKERS[:])
        self.inactive_list.clear()
        self.inactive_list.addItems(cfg.INACTIVE_TICKERS[:])
        self.console_message.setText(self.log_msg) 
        self.closing_day = f'{self.year_line_edit.text()}-{self.month_line_edit.text()}-{self.day_line_edit.text()}'

    def run(self):
        # GET requests to API, retuns <class 'requests.models.Response'>
        gets = []
        close_prices = []
        for t in cfg.ACTIVE_TICKERS:
            url = f'https://api.marketdata.app/v1/stocks/candles/D/{t}?limit=1&to={DATE}&headers=false&format=csv&columns=c&token={api_key.API_KEY}'
            gets.append(requests.request("GET", url))
        
        # pull string data from requests
        for g in gets:
            close_prices.append(g.text)

        # write date/ticker/price and save to excel
        try:
            book = openpyxl.load_workbook(cfg.FILE_NAME)
            sheet = book[cfg.SHEET_NAME]
            for i in range(len(close_prices)):
                sheet.cell(row = i + 1, column = 1).value = DATE
            row = 0   
            for t in cfg.ACTIVE_TICKERS:
                row += 1
                sheet.cell(row=row, column=2).value = t
            row = 0
            for c in close_prices:
                row += 1
                sheet.cell(row=row, column=4).value = c
            book.save(cfg.FILE_NAME)
        except:
            self.log_msg = f'File "{cfg.FILE_NAME}" not found.'
            self.ui_refresh()
def main():
    app = QApplication([])
    window = MyGui()
    app.exec()

if __name__ == '__main__':
    main()