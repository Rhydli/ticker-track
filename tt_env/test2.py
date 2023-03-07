from PyQt6.QtWidgets import *
from PyQt6 import uic

ACTIVE_TICKERS = ['BIL', 'BNDX', 'EGIS']

class MyGui(QMainWindow):

    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi('tt.ui', self)
        self.show()
        self.setWindowTitle('Ticker Track')

        self.add_button.clicked.connect(lambda: self.add(self.ticker_line_edit.text()))
        self.delete_button.clicked.connect(self.delete)

    def add(self, msg):
        ACTIVE_TICKERS.append(msg)
        print(f'{msg} added.')

    def delete(self):
        print(ACTIVE_TICKERS)

def main():
    app = QApplication([])
    window = MyGui()
    app.exec()

if __name__ == '__main__':
    main()