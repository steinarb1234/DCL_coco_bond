import os 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
TODO: Add AT1 bond data
TODO: Add CET1 ratio data
TODO: Add shares outstanding data (NS_{k-1})
TODO: Calculate market caps

TODO: Find risk free rates (Yield curve?)
TODO: Derive the following from the data:
    RQ_k = Q * ((1 + r)^k + (1 - (1 + r)^k)/(1 - (1 + r)^{-N_m})) # Note that this only applies if the triggers are not breached
    Leverage ratio = Total debt / (Total equity + Total debt) = RQ_k / (RQ_k + NS_{k-1} * S_k)
    alpha = RQ_k / (RQ_k + Book value of non CoCo debt)
"""

# ================================================================
#                           Constants
# ================================================================
ticker = "CSGN.S"   # Credit Suisse
# ticker = "DBKGn.DE" # Deutsche Bank
# ticker = "LEHMQ.PK" # Lehman Brothers
# ticker = "SVBQ.PK"  # Silicon Valley Bank

T = 10       # Number of years to maturity for DCL bonds
L_min = 0.05 # Minimum leverage ratio
L_c = 0.1    # Critical leverage ratio


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
    # TODO: Add number of shares outstanding data
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


def load_book_values(stock_data: pd.DataFrame, ticker: str) -> None:
    """
    Add book value of debt to the stock data. 
    """

    # Load the book value data
    # book_value_data = pd.read_excel(f'data/book_values/{ticker}.xlsx', index_col=0, parse_dates=True)
    book_value_data = pd.read_excel(f'data/book_values/CSGN.xlsx', index_col=0, parse_dates=True)

    # Merge the book value data with the stock data
    stock_data = stock_data.merge(book_value_data, left_index=True, right_index=True, how='left')

    # Fill missing values
    stock_data['Book value of debt'] = stock_data['Book value of debt'].ffill()
    stock_data['Book value of debt'] = stock_data['Book value of debt'].bfill()

    return stock_data


def calculate_alpha(stock_data: pd.DataFrame) -> None:
    """
    Calculate the ratio of CoCos to total debt. 
    """

    stock_data['Alpha'] = stock_data['CoCo'] / (stock_data['CoCo'] + stock_data['Book value of debt'])



def main():
    if not os.path.exists("../DCL_coco_bond"):
        raise Exception("You must run this script from the root directory of the project")
    
    stock_data = load_reuters_data(ticker)
    stock_data = load_book_values(stock_data, ticker)
    # print(stock_data.head())

    # plot the closing price, the book value of debt in subplots
    fig, ax = plt.subplots(2, 1, sharex=True)
    ax[0].plot(stock_data.index, stock_data['Close'], label='Close')
    ax[0].set_title('Stock price')
    ax[1].plot(stock_data.index, stock_data['Book value of debt'], label='Book value of debt')
    ax[1].set_title('Book value of debt')
    plt.show()


if __name__ == "__main__":
    main()
