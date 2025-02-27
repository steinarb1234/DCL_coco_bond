import os 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import eikon as ek  # the Eikon Python wrapper package
# import cufflinks as cf  # Cufflinks
import configparser as cp
import warnings

# Ignore all FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

DATA_DOLDER = "data"


ticker = "CSGN.S"   # Credit Suisse
# ticker = "DBKGn.DE" # Deutsche Bank
# ticker = "LEHMQ.PK" # Lehman Brothers
# ticker = "SVBQ.PK"  # Silicon Valley Bank

T = 10       # Number of years to maturity for DCL bonds
r = 0.05     # Risk free rate
L_min = 0.20 # Minimum leverage ratio
L_c = 0.8    # Critical leverage ratio

# Set eikon api key from config file
cfg = cp.ConfigParser()
cfg.read('eikon.config')
ek.set_app_key(cfg['eikon']['app_key'])

# df, err = ek.get_data(
#     instruments=[ticker],
#     fields=["TR.OpenPrice", "TR.ClosePrice"]
# )
# print(df)
print("========================")

print(ek.get_symbology("CSGN", to_symbol_type="RIC"))
print("========================")


print("========================")
ric_search = ek.get_symbology('CH0012138530', from_symbol_type='ISIN', to_symbol_type='RIC')
print(ric_search)
print("========================")

# print(ric_search["RIC"][0])
ticker_ric = ric_search["RIC"][0]
# ticker_ric = "CSGN.S^F23"

start_date = '2018-01-01'
end_date = '2024-01-01'


print("======================= TR Field =========================")


# ek.TR_Field()


print("==========================================================\n")




print("====================== Metrics ===========================")
cs_metrics = ek.get_data([ticker_ric], 
                         ['TR.TotalAssets'])
print(cs_metrics[1])
print(cs_metrics[0])
cs_metrics[0].to_excel(f"{DATA_DOLDER}/cs_metrics.xlsx")
print("==========================================================\n")

print("====================== Balance Sheet =====================")

cs_balance_sheet = ek.get_data(ticker_ric, 
                               [
                                   'TR.TotalAssets.date',
                                    'TR.TotalAssets',
                                    'TR.TotalLiabilities',
                                    'TR.TotalEquity', 
                                    'TR.ShareholdersEquityActual' # The companys actual value normailzed to reflect the I/B/E/S default currency and stock plits. 
                                ], 
                               parameters={'SDate': start_date, 'EDate': end_date}
                               )
print(cs_balance_sheet[1])
print(cs_balance_sheet[0])
cs_balance_sheet[0].to_excel(f"{DATA_DOLDER}/cs_balance_sheet.xlsx")
print("==========================================================\n")


print("====================== Credit Spread =====================")
cds_spread = ek.get_data('CSGN5YEUAM=R', ['TR.MidSpread'], 
                               parameters={'SDate': start_date, 'EDate': end_date})
print(cds_spread[1])
print(cds_spread[0])
cds_spread[0].to_excel(f"{DATA_DOLDER}/cds_spread.xlsx")
print("==========================================================\n")

print("=================== DCL Data =============================")
cs_dcl_data = ek.get_data(ticker_ric, 
                        [
                            'TR.MARKETCAPITALIZATION', 
                            'TR.TotalDebt', 
                            # 'TR.ShareholdersEquity', 
                            # 'TR.Volatility30D',
                            # 'TR.PCTotDebtToToEquPct'
                        ], 
                        parameters={'SDate': start_date, 'EDate': end_date}
                        )
print(cs_dcl_data[1])
print(cs_dcl_data[0])
cs_dcl_data[0].to_excel(f"{DATA_DOLDER}/cs_dcl_data.xlsx")
print("==========================================================\n")


print("=================== Timeseries ===========================")
cs_timeseries = ek.get_timeseries(ticker_ric, 
                            start_date=start_date, 
                            end_date=end_date, 
                            interval='daily')
print(cs_timeseries)
cs_timeseries.to_excel(f"{DATA_DOLDER}/cs_timeseries.xlsx")
print("==========================================================\n")




