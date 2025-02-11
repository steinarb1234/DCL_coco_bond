import os 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
TODO: Add AT1 bond data
TODO: Add shares outstanding data
TODO: Add market cap data
TODO: Add CET1 ratio data
TODO: Add number of shares outstanding data

TODO: Find risk free rates (Yield curve?)
TODO: Derive the following from the data:
- Volatility
- 

Ratios:
Total debt / Total equity
Total debt / Total capital (Tier 1 plus Tier 2 capital)


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


def add_book_values(stock_data: pd.DataFrame, ticker: str) -> None:
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
    
    ticker = "CSGN.S" # Credit Suisse
    # ticker = "DBKGn.DE" # Deutsche Bank
    # ticker = "LEHMQ.PK" # Lehman Brothers
    # ticker = "SVBQ.PK" # Silicon Valley Bank

    stock_data = load_reuters_data(ticker)

    stock_data = add_book_values(stock_data, ticker)



    print(stock_data.head())

    # plot the closing price and the book value of debt on separate axes
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(stock_data.index, stock_data['Close'], 'g-')
    ax2.plot(stock_data.index, stock_data['Book value of debt'], 'b-')
    plt.show()


    


if __name__ == "__main__":
    main()
