import requests
import openpyxl
import api_key
import config as cfg
from PyQt6.QtWidgets import *
from PyQt6 import uic

'''UNC network pathing,
logging history of console,
period in ticker field crashes because of .upper()'''

class MyGui(QMainWindow):

    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi('tt.ui', self)
        self.show()
        self.setWindowTitle('Ticker Track')
        self.active_list.addItems(cfg.ACTIVE_TICKERS[:])
        self.inactive_list.addItems(cfg.INACTIVE_TICKERS[:])
        self.log_msg = ''
        self.load_date()
        self.add_button.clicked.connect(lambda: self.add((self.ticker_line_edit.text().upper())))
        self.toggle_button.clicked.connect(lambda: self.toggle(self.ticker_line_edit.text().upper()))
        self.delete_button.clicked.connect(lambda: self.delete(self.ticker_line_edit.text().upper()))
        self.run_button.clicked.connect(self.run)

    def load_date(self):
        if self.year_line_edit:
            self.year_line_edit.setText(cfg.YEAR)
            self.month_line_edit.setText(cfg.MONTH)
            self.day_line_edit.setText(cfg.DAY)
        else:
            pass

    def add(self, t):
        my_dict = {46:None}
        ticker = t.translate(my_dict)
        if ticker and not ticker.isspace():
            url = f'https://api.marketdata.app/v1/stocks/quotes/{ticker}/?token={api_key.API_KEY}'
            response = requests.request("GET", url)
            try:
                if bool(response.json()['s'] == 'ok'):
                    if ticker in cfg.ACTIVE_TICKERS:
                        self.log_msg = f'"{ticker}" already in active tickers.'
                        self.ui_refresh()
                    elif ticker not in cfg.ACTIVE_TICKERS and ticker not in cfg.INACTIVE_TICKERS:
                        cfg.ACTIVE_TICKERS.append(ticker)
                        cfg.update_cfg()
                        self.log_msg = f'"{ticker}" added to active tickers.'
                        self.ui_refresh()
                    else:
                        self.log_msg = f'"{ticker}" already in inactive tickers.'
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

    def toggle(self, ticker):
        if ticker and not ticker.isspace():
            if ticker in cfg.ACTIVE_TICKERS:
                cfg.INACTIVE_TICKERS.append(ticker)
                cfg.ACTIVE_TICKERS.remove(ticker)
                cfg.update_cfg()
                self.log_msg = f'"{ticker}" moved to inactive tickers.'
                self.ui_refresh()
            elif ticker in cfg.INACTIVE_TICKERS:
                cfg.ACTIVE_TICKERS.append(ticker)
                cfg.INACTIVE_TICKERS.remove(ticker)
                cfg.update_cfg()
                self.log_msg = f'"{ticker}" moved to active tickers.'
                self.ui_refresh()
            else:
                self.log_msg = f'"{ticker}" ticker has not yet been added.'
                self.ui_refresh()
        else:
            self.log_msg = 'No Ticker provided.'
            self.ui_refresh()

    def delete(self, ticker):
        if ticker and not ticker.isspace():
            if ticker in cfg.ACTIVE_TICKERS or ticker in cfg.INACTIVE_TICKERS:
                try:
                    cfg.ACTIVE_TICKERS.remove(ticker)
                except:
                    cfg.INACTIVE_TICKERS.remove(ticker)
                finally:
                    cfg.update_cfg()
                    self.log_msg = f'"{ticker}" has been successfully removed.'
                    self.ui_refresh()
            else:
                self.log_msg = f'Removal unsuccessful. "{ticker}" not found.'
                self.ui_refresh()
        else:
            self.log_msg = 'No Ticker provided.'
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
            url = f'https://api.marketdata.app/v1/stocks/candles/D/{t}?limit=1&to={self.closing_day}&headers=false&format=csv&columns=c&token={api_key.API_KEY}'
            gets.append(requests.request("GET", url))
        
        # pull string data from requests
        for g in gets:
            close_prices.append(g.text)

        # write date/ticker/price and save to excel
        try:
            book = openpyxl.load_workbook(cfg.FILE_NAME)
            sheet = book[cfg.SHEET_NAME]
            for i in range(len(close_prices)):
                sheet.cell(row = i + 1, column = 1).value = self.closing_day
                print(self.closing_day)
            row = 0   
            for t in cfg.ACTIVE_TICKERS:
                row += 1
                sheet.cell(row=row, column=2).value = t
            row = 0
            for c in close_prices:
                row += 1
                sheet.cell(row=row, column=4).value = c
            book.save(cfg.FILE_NAME)
            self.log_msg = 'Finished'
            self.ui_refresh()
        except:
            self.log_msg = f'File "{cfg.FILE_NAME}" not found.'
            self.ui_refresh()

def main():
    app = QApplication([])
    window = MyGui()
    app.exec()

if __name__ == '__main__':
    main()