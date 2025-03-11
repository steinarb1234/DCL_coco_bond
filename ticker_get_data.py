
import pandas as pd
import matplotlib.pyplot as plt
import eikon as ek  # the Eikon Python wrapper package
import configparser as cp
import warnings

# Ignore eikon deprication warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
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
    'TR.TotalDebtOutstanding', # Total debt outstanding
    # 'TR.F.LTDebtPctofTotCap',  # Long term debt divided by total capital
    'TR.CompanyMarketCapitalization', # Market capitalization
    'TR.IssueSharesOutstanding', # Real time shares outstanding
    'TR.TotalAssets', # Total Assets
    'TR.TotalDebtOutstanding', # Total debt outstanding
    'TR.TotalDebtActValue', # Actual value after default
    # 'TR.TotalLongTermDebt',
]

# ticker_ric = "CSGN.S^F23" # Credit Suisse
# ticker_ric = "DBKGn.DE"   # Deutsche Bank
# ticker_ric = "LEHMQ.PK^C12"   # Lehman Brothers
ticker_ric = "SIVBQ.PK^K24"    # Silicon Valley Bank


start_date = '2015-01-01'
end_date = '2025-01-01'

for data_type in data_types:
    print(f"Getting data for {data_type}")
    data, err = get_data(ticker_ric, start_date, end_date, data_type)
    data.to_excel(f"{DATA_DOLDER}/{ticker_ric}/{data_type}.xlsx")
    print(err)
    print(data)
    print()
    # data.plot()
    # plt.show()

# Close price timeseries is a special case (uses get_timeseries instead of get_data)
close = ek.get_timeseries(ticker_ric, 
                            fields="Close",
                            start_date=start_date, 
                            end_date=end_date, 
                            interval='daily')
close = close[["CLOSE"]].rename(columns={"CLOSE": "Close"})
close.to_excel(f"{DATA_DOLDER}/{ticker_ric}/Close.xlsx")
print(close)
# close.plot()
# plt.show()


