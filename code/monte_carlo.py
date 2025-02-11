import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_stock_data(ticker="BAC", start="2007-01-01", end="2009-12-31"):
    """
    Fetches historical daily data (Open, High, Low, Close, Volume) for the specified ticker.
    Uses yfinance. Returns a Pandas DataFrame with a DateTime index.
    """
    data = yf.download(ticker, start=start, end=end)
    # We'll focus on the 'Close' column for an adjusted stock price
    data = data[['Close']]
    data.rename(columns={'Close': 'Price'}, inplace=True)
    return data

def simulate_coco_behavior(
    df_price, 
    debt_notional=200e9,     # Assume a total debt of $200B (example)
    shares_outstanding=10e9, # Assume 10B shares outstanding (example)
    leverage_trigger=25.0    # Example: triggers if Leverage >= 25
):
    """
    Given a DataFrame of daily prices and some assumed capital structure,
    compute a daily 'market leverage' and check if the CoCo bond would trigger.
    
    Leverage = Debt / (Equity_Market_Value)
    Equity_Market_Value = Price * shares_outstanding
    Trigger occurs if Leverage >= leverage_trigger.
    
    Returns the original DataFrame with new columns for Leverage and Trigger.
    """
    df = df_price.copy()
    
    # Compute Equity Market Value
    df['Equity_MV'] = df['Price'] * shares_outstanding
    
    # Compute Leverage ratio
    df['Leverage'] = debt_notional / df['Equity_MV']
    
    # Check if/when the CoCo triggers
    df['Triggered'] = df['Leverage'] >= leverage_trigger
    
    return df

def plot_coco_results(df, ticker="BAC", leverage_trigger=25.0):
    """
    Plot the stock price and leverage ratio over time, 
    highlighting days where trigger occurs.
    """
    fig, ax1 = plt.subplots(figsize=(10,6))

    # Plot Price on the left y-axis
    ax1.set_title(f"CoCo Bond Trigger Analysis for {ticker} (2007–2009)")
    ax1.plot(df.index, df['Price'], color='blue', label='Stock Price')
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Stock Price (USD)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Plot Leverage on the right y-axis
    ax2 = ax1.twinx()
    ax2.plot(df.index, df['Leverage'], color='red', label='Leverage Ratio')
    ax2.set_ylabel("Leverage Ratio", color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.axhline(leverage_trigger, color='grey', linestyle='--', label='Trigger Threshold')

    # Highlight trigger days
    trigger_days = df[df['Triggered']].index
    if len(trigger_days) > 0:
        # Mark them with vertical lines or scatter points
        ax2.scatter(trigger_days, df.loc[trigger_days, 'Leverage'],
                    color='black', marker='x', label='Trigger Event')

    # Combine legends
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    plt.tight_layout()
    plt.savefig("figures/coco_trigger_analysis.png")
    plt.show()

def main():
    # 1. Fetch historical data for a specific bank
    ticker = "BAC"  # Bank of America, as an example
    df_price = fetch_stock_data(ticker, start="2006-01-01", end="2010-12-31")

    # 2. Simulate CoCo bond behavior on this historical path
    #    (i.e., did it trigger on any days given a hypothetical threshold?)
    debt_notional = 200e9         # $200B (example)
    shares_outstanding = 10e9     # 10B shares (example)
    leverage_trigger = 25.0       # Arbitrary threshold for demonstration

    df_coco = simulate_coco_behavior(
        df_price=df_price, 
        debt_notional=debt_notional,
        shares_outstanding=shares_outstanding,
        leverage_trigger=leverage_trigger
    )

    # 3. Plot the results
    plot_coco_results(df_coco, ticker=ticker, leverage_trigger=leverage_trigger)


if __name__ == "__main__":
    main()
