# Standard library imports
import logging

# Third-party library imports
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QApplication
from openpyxl import load_workbook
from requests import request

# Local application imports
import api_key
import config as cfg
from PyQt6 import uic


# log setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(asctime)s:%(message)s')
file_handler = logging.FileHandler('repository.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class MyGui(QMainWindow):

    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi('tt.ui', self)
        self.show()
        self.setWindowTitle('Ticker Track')
        self.active_list.addItems(cfg.ACTIVE_TICKERS[:])
        self.inactive_list.addItems(cfg.INACTIVE_TICKERS[:])
        self.path_line_edit.setText(cfg.BOOK_NAME)
        self.is_running = False
        self.log_msg = ''
        self.file_path = self.path_line_edit.text()
        self.path_line_edit.textChanged.connect(self.ui_refresh)
        self.add_button.clicked.connect(lambda: self.add((self.ticker_line_edit.text().upper())))
        self.toggle_button.clicked.connect(lambda: self.toggle(self.ticker_line_edit.text().upper()))
        self.delete_button.clicked.connect(lambda: self.delete(self.ticker_line_edit.text().upper()))
        self.reset_date_button.clicked.connect(self.load_date)
        self.browse_button.clicked.connect(self.browse)
        self.run_button.clicked.connect(self.run)
        self.ui_refresh()
        self.load_date()
    
    # enable or disable run button based on file path
    def toggle_run_button(self):
        if self.file_path and not self.is_running:
            self.run_button.setEnabled(True)
        else:
            self.run_button.setEnabled(False)

    # init last closing day on startup or reset
    def load_date(self):
        self.year_line_edit.setText(cfg.YEAR)
        self.month_line_edit.setText(cfg.MONTH)
        self.day_line_edit.setText(cfg.DAY)

    # get file path from user selection and show user selection in UI
    def browse(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", "")
        self.path_line_edit.setText(file_name[0]) 

    # store current file path in config
    def save_file_path(self):
        cfg.config.set('FILE', 'book', self.file_path)
        with open('tt_config.ini', 'w') as configfile:
            cfg.config.write(configfile)
    
    # update ui
    def ui_refresh(self):
        self.active_list.clear()
        self.active_list.addItems(cfg.ACTIVE_TICKERS[:])
        self.inactive_list.clear()
        self.inactive_list.addItems(cfg.INACTIVE_TICKERS[:])
        self.console_message.setText(self.log_msg)
        self.console_message.setToolTip(self.log_msg)
        self.path_line_edit.setToolTip(self.path_line_edit.text())
        self.file_path = self.path_line_edit.text()
        self.save_file_path()
        self.toggle_run_button()

    # validate and add ticker input to active list
    def add(self, input):
        my_dict = {46: None, 63: None}
        ticker = input.translate(my_dict)
        if ticker and not ticker.isspace():
            url = f'https://api.marketdata.app/v1/stocks/quotes/{ticker}/?token={api_key.API_KEY}'
            response = request("GET", url)
            # check API for ticker data
            try:
                if bool(response.json()['s'] == 'ok'):
                    if ticker in cfg.ACTIVE_TICKERS:
                        self.log_msg = f'"{ticker}" already in active tickers.'
                        logger.info(f'"{ticker}" already in active tickers.')
                        self.ui_refresh()
                    elif ticker not in cfg.ACTIVE_TICKERS and ticker not in cfg.INACTIVE_TICKERS:
                        cfg.ACTIVE_TICKERS.append(ticker)
                        cfg.update_cfg()
                        self.log_msg = f'"{ticker}" added to active tickers.'
                        logger.info(f'"{ticker}" added to active tickers.')
                        self.ui_refresh()
                    else:
                        self.log_msg = f'"{ticker}" already in inactive tickers.'
                        logger.info(f'"{ticker}" already in inactive tickers.')
                        self.ui_refresh()
                else:
                    self.log_msg = f'API Response: {response.json()["errmsg"]}, Ticker: "{ticker}"'
                    logger.error(f'API Response: {response.json()["errmsg"]}, Ticker: "{ticker}"')
                    self.ui_refresh()
            except:
                self.log_msg = f'Exception: {response.json()["errmsg"]}'
                logger.error(f'Exception: {response.json()["errmsg"]}')
                self.ui_refresh()
        else:
            self.log_msg = 'No Ticker provided.'
            logger.info('No Ticker provided.')
            self.ui_refresh()

    # move ticker between active and inactive lists
    def toggle(self, ticker):
        if ticker and not ticker.isspace():
            if ticker in cfg.ACTIVE_TICKERS:
                cfg.INACTIVE_TICKERS.append(ticker)
                cfg.ACTIVE_TICKERS.remove(ticker)
                cfg.update_cfg()
                self.log_msg = f'"{ticker}" moved to inactive tickers.'
                logger.info(f'"{ticker}" moved to inactive tickers.')
                self.ui_refresh()
            elif ticker in cfg.INACTIVE_TICKERS:
                cfg.ACTIVE_TICKERS.append(ticker)
                cfg.INACTIVE_TICKERS.remove(ticker)
                cfg.update_cfg()
                self.log_msg = f'"{ticker}" moved to active tickers.'
                logger.info(f'"{ticker}" moved to active tickers.')
                self.ui_refresh()
            else:
                self.log_msg = f'"{ticker}" ticker has not yet been added.'
                logger.info(f'"{ticker}" ticker has not yet been added.')
                self.ui_refresh()
        else:
            self.log_msg = 'No Ticker provided.'
            logger.info('No Ticker provided.')
            self.ui_refresh()

    # remove ticker from either list
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
                    logger.info(f'"{ticker}" has been successfully removed.')
                    self.ui_refresh()
            else:
                self.log_msg = f'Removal unsuccessful. "{ticker}" not found.'
                logger.info(f'Removal unsuccessful. "{ticker}" not found.')
                self.ui_refresh()
        else:
            self.log_msg = 'No Ticker provided.'
            logger.info('No Ticker provided.')
            self.ui_refresh()

    # export data to file
    def run(self):
        self.is_running = True
        # pull date from UI user input
        day_string = f'{self.year_line_edit.text()}-{self.month_line_edit.text()}-{self.day_line_edit.text()}'
        try:
            # format date to string
            closing_day = str(cfg.parse(day_string))[:10]
            gets = []
            # GET requests to API
            for t in cfg.ACTIVE_TICKERS:
                url = f'https://api.marketdata.app/v1/stocks/candles/D/{t}?limit=1&date={closing_day}&headers=false&format=csv&columns=c&token={api_key.API_KEY}'
                response = request("GET", url)
                gets.append(response)
                if not cfg.isfloat(response.text.strip()):
                    logger.error(f'API Response: {response.text.strip()} for "{t}" on "{closing_day}"')
            close_prices = []
            # store price data from GET requests, check for valid price data and log exceptions
            for g in gets:
                if cfg.isfloat(g.text):
                    close_prices.append(g.text)
                else:
                    close_prices.append('No price data.')
            # write and save data
            try:
                book = load_workbook(self.file_path)
                sheet = book[cfg.SHEET_NAME]
                for i in range(len(close_prices)):
                    sheet.cell(row = i + 1, column = 1).value = closing_day
                row = 0   
                for t in cfg.ACTIVE_TICKERS:
                    row += 1
                    sheet.cell(row=row, column=2).value = t
                row = 0
                for c in close_prices:
                    row += 1
                    sheet.cell(row=row, column=4).value = c
                book.save(self.file_path)
                self.log_msg = f'Saved results to {self.file_path} for {closing_day}.'
                logger.info(f'Saved results to {self.file_path} for {closing_day}.')
                self.ui_refresh()
            except:
                self.log_msg = f'File "{self.file_path}" not found.'
                logger.info(f'File "{self.file_path}" not found.')
                self.ui_refresh()
        except ValueError as ve:
            self.log_msg = f'An error occurred: {ve}'
            logger.error(f'An error occurred: {ve}')
        finally:
            self.is_running = False
            self.ui_refresh()
    
def main():
    app = QApplication([])
    window = MyGui()
    app.exec()

if __name__ == '__main__':
    main()