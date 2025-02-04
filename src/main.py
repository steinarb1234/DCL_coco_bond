import os 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
TODO: Add AT1 bond data
TODO: Add shares outstanding data
TODO: Add market cap data
TODO: Add CET1 ratio data

TODO: Find risk free rates (Yield curve?)
TODO: Derive the following from the data:
- Volatility
- 


"""

def load_reuters_data(ticker, data_folder = "data/reuterseikonexports") -> pd.DataFrame: 
    """
    Stock price data exported from Reuters Eikon. The sheet has multiple different tables, 
    so we need to find the start row of the table with the stock price data.
    """

    def get_start_row(ticker, data_folder): 
        "Find first row with 'Close' column"
        df = pd.read_excel(f'{data_folder}/{ticker}.xlsx')
        for i, row in df.iterrows():
            if "Close" in row.values:
                return i + 1
        raise Exception("Could not find the start row")

    # Read in the data from the Excel file
    dataset = pd.read_excel(
        io = f'{data_folder}/{ticker}.xlsx', 
        skiprows = get_start_row(ticker, data_folder), 
        usecols = "A:B", # Date and Close columns
        # usecols = "A:I", # All columns
        index_col = 0, 
        parse_dates = True, 
    )

    dataset.dropna(inplace=True)
    dataset.sort_index(inplace=True)
    return dataset


def main():
    if not os.path.exists("../DCL_coco_bond"):
        raise Exception("You must run this script from the root directory of the project")
    
    ticker = "CSGN.S" # Credit Suisse
    # ticker = "DBKGn.DE" # Deutsche Bank
    # ticker = "LEHMQ.PK" # Lehman Brothers
    # ticker = "SVBQ.PK" # Silicon Valley Bank

    stock_data = load_reuters_data(ticker)

    # plot the closing price
    plt.figure(figsize=(10, 7))
    plt.plot(stock_data['Close'], label='Close Price history')
    plt.title(f'Close Price History ({ticker})')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.show()


if __name__ == "__main__":
    main()
