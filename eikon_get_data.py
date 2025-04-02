
import pandas as pd
import matplotlib.pyplot as plt
import eikon as ek
import configparser as cp
import warnings
import os

# Ignore eikon deprication warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Check if eikon.config file extists
if os.path.exists('eikon.config'):
    pass
else:
    raise FileNotFoundError("Create the eikon.config file and set your eikon api key with: \n`\n[eikon]\napp_key=<YOUR_EIKON_APP_KEY>\n`")

# Set eikon api key from config file
cfg = cp.ConfigParser()
cfg.read('eikon.config')
ek.set_app_key(cfg['eikon']['app_key'])
DATA_DOLDER = "data"

def get_data(ticker_ric, start_date, end_date, data_type):
    df, err = ek.get_data(ticker_ric, 
        [
            f'{data_type}.date',
            f'{data_type}',
        ],
        parameters={'SDate': start_date, 'EDate': end_date},
    )
    df = df.set_index("Date").drop(columns=["Instrument"])
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df, err

data_types = [
    'TR.TotalDebtOutstanding',        # Total debt outstanding (Book value)
    'TR.CompanyMarketCapitalization', # Market capitalization (Daily)
    'TR.IssueSharesOutstanding',      # Real time shares outstanding (Daily, TODO: common or total?)
    'TR.TotalAssets',                 # Total Assets (Book value)
    'TR.TotalDebtActValue',           # Actual value after default (this returns an empty list for non-defaulted companies)
    # 'TR.TotalLongTermDebt',
]

tickers = {
    "CSGN.S^F23": { # Credit Suisse
        "start_date": "2015-01-01",
        "end_date": "2025-01-01",
    },
    "DBKGn.DE": { # Deutsche Bank
        "start_date": "2015-01-01",
        "end_date": "2025-01-01",
    },
    "LEHMQ.PK^C12": { # Lehman Brothers
        "start_date": "2000-01-01",
        "end_date": "2010-01-01",
    },
    "SIVBQ.PK^K24": { # Silicon Valley Bank
        "start_date": "2015-01-01",
        "end_date": "2025-01-01",
    },
    "UBSG.S": { # UBS
        "start_date": "2015-01-01",
        "end_date": "2025-01-01",
    },
    "ARION.IC": { # Arion Banki
        "start_date": "2015-01-01",
        "end_date": "2025-01-01",
    },
    "ISB.IC": { # Íslandsbanki
        "start_date": "2015-01-01",
        "end_date": "2025-01-01",
    },
    "GS": { # Goldman Sachs
        "start_date": "2015-01-01",
        "end_date": "2025-01-01",
    },
    "MS": { # Morgan Stanley
        "start_date": "2015-01-01",
        "end_date": "2025-01-01",
    },
    "JPM": { # JP Morgan Chase
        "start_date": "2015-01-01",
        "end_date": "2025-01-01",
    },
}

for ticker_ric, dates in tickers.items():
    start_date = dates["start_date"]
    end_date = dates["end_date"]
    for data_type in data_types:
        print(f"Getting data for {ticker_ric} - {data_type}")
        data, err = get_data(ticker_ric, start_date, end_date, data_type)
        if err:
            raise ValueError(f"Error getting {ticker_ric} - {data_type}")
        data = data.dropna()
        if not os.path.exists(f"{DATA_DOLDER}/{ticker_ric}"):
            os.makedirs(f"{DATA_DOLDER}/{ticker_ric}")
        data.to_excel(f"{DATA_DOLDER}/{ticker_ric}/{data_type}.xlsx")
        print(err)
        print(data)
        print()
        # data.plot()
        # plt.show()

    # Close price timeseries is a special case (uses get_timeseries instead of get_data)
    print(f"Getting data for {ticker_ric} - Close")
    max_retries = 3
    attempts = 0
    while attempts <= max_retries:
        close = ek.get_timeseries(ticker_ric, 
                                    fields="Close",
                                    start_date=start_date, 
                                    end_date=end_date, 
                                    interval='daily')
        if close is None:
            continue
        else:
            break
        
    close = close[["CLOSE"]].rename(columns={"CLOSE": "Close"})
    close.to_excel(f"{DATA_DOLDER}/{ticker_ric}/Close.xlsx")
    print(close)
    # close.plot()
    # plt.show()

