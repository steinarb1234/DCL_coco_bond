
import pandas as pd
import matplotlib.pyplot as plt
import eikon as ek  # the Eikon Python wrapper package
import configparser as cp
import warnings

# Ignore eikon deprication warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
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


# Set eikon api key from config file
cfg = cp.ConfigParser()
cfg.read('eikon.config')
ek.set_app_key(cfg['eikon']['app_key'])

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

ticker_ric = "CSGN.S^F23"
start_date = '2017-01-01'
end_date = '2025-01-01'
for data_type in data_types:
    data, err = get_data(ticker_ric, start_date, end_date, data_type)
    print(err)
    print(data)
    
    # data.plot()
    # plt.show()

    data.to_excel(f"{DATA_DOLDER}/{ticker_ric}/{data_type}.xlsx")

