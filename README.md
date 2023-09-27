# Ticker Track

Ticker Track is a Python application for tracking and analyzing stock data. It allows you to manage a list of stock tickers, retrieve historical stock prices, and save the data to an Excel file for further analysis.

## Features

- **Ticker Management:** Add, remove, and toggle between active and inactive stock tickers in your watchlist.
- **Data Retrieval:** Retrieve historical stock prices for a specified date or date range using the [Market Data API](https://marketdataapi.app/).
- **Data Export:** Save the retrieved stock price data to an Excel file for analysis.

## Prerequisites

Before using Ticker Track, ensure you have the following prerequisites:

- Python 3.x installed on your system.
- Required Python packages (PyQt6, openpyxl, requests) installed. You can install them using `pip install PyQt6 openpyxl requests`.

## Usage

1. Clone or download this repository to your local machine.
2. Install the required Python packages mentioned in the prerequisites.
3. Run the application using the following command:

   ```bash
   python main.py
