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
end_date = '2025-01-01'


print("======================= TR Field =========================")


# ek.TR_Field()


print("==========================================================\n")




print("====================== Metrics ===========================")
cs_metrics, err = ek.get_data([ticker_ric], 
                         ['TR.TotalAssets'])
print(err)
print(cs_metrics)
cs_metrics.to_excel(f"{DATA_DOLDER}/cs_metrics.xlsx")
print("==========================================================\n")

print("====================== Balance Sheet =====================")

cs_balance_sheet, err = ek.get_data(ticker_ric, 
                               [
                                   'TR.TotalAssets.date',
                                    'TR.TotalAssets',
                                    'TR.TotalLiabilities',
                                    'TR.TotalEquity', 
                                    'TR.ShareholdersEquityActual' # The companys actual value normailzed to reflect the I/B/E/S default currency and stock plits. 
                                ], 
                               parameters={'SDate': start_date, 'EDate': end_date}
                               )
print(err)
print(cs_balance_sheet)
cs_balance_sheet.to_excel(f"{DATA_DOLDER}/cs_balance_sheet.xlsx")
print("==========================================================\n")


print("====================== Credit Spread =====================")
cds_spread, err = ek.get_data('CSGN5YEUAM=R', ['TR.MidSpread'], 
                               parameters={'SDate': start_date, 'EDate': end_date})
print(err)
print(cds_spread)
cds_spread.to_excel(f"{DATA_DOLDER}/cds_spread.xlsx")
print("==========================================================\n")

print("=================== DCL Data =============================")
cs_dcl_data, err = ek.get_data(ticker_ric, 
                        [
                            # 'TR.NumberofSharesOutstandingActual.date',
                            # 'TR.NumberofSharesOutstandingActual',
                            'TR.CompanyMarketCap.Date',
                            'TR.CompanyMarketCap',
                            'TR.CompanyMarketCap.Currency',
                            'TR.F.ComShrOutsTot',
                            'TR.TtlCmnSharesOut',
                            'TR.F.ShrUsedToCalcBasicEPSIssue',
                            'TR.F.ShrUsedToCalcDilEPSTot',
                            'TR.F.ComShrOutstTotPoPAvg',

                            # 'TR.CurrTtlLatestSharesOut.date'
                            # 'TR.CurrTtlLatestSharesOut'
                            # 'TR.MARKETCAPITALIZATION', 
                            # 'TR.TotalDebt', 
                            # 'TR.ShareholdersEquity', 
                            # 'TR.Volatility30D',
                            # 'TR.PCTotDebtToToEquPct'
                        ], 
                        parameters={'SDate': start_date, 'EDate': end_date, 'FRQ': 'D'}
                        )
print(err)
print(cs_dcl_data)
# cs_dcl_data.plot(title="DataFrame Plot")
# plt.show()
cs_dcl_data.to_excel(f"{DATA_DOLDER}/cs_dcl_data.xlsx")
print("==========================================================\n")


print("=================== Shares outstanding =============================")
cs_shares_outstanding, err = ek.get_data(ticker_ric, 
                        [
                            # 'TR.NumberofSharesOutstandingActual.date',
                            # 'TR.NumberofSharesOutstandingActual',
                            'TR.F.ComShrOutsTot.date',
                            'TR.F.ComShrOutsTot',
                            # 'TR.TtlCmnSharesOut',
                        ], 
                        parameters={'SDate': start_date, 'EDate': end_date, 'FRQ': 'D'}
                        )
print(err)
print(cs_shares_outstanding)
# cs_shares_outstanding.plot(title="DataFrame Plot")
# plt.show()
cs_shares_outstanding.to_excel(f"{DATA_DOLDER}/cs_shares_outstanding.xlsx")
print("==========================================================\n")

print("=================== Market cap =============================")
cs_market_cap, err = ek.get_data(ticker_ric, 
                        [
                            'TR.CompanyMarketCap.Date',
                            'TR.CompanyMarketCap',
                            'TR.CompanyMarketCap.Currency',
                        ], 
                        parameters={'SDate': start_date, 'EDate': end_date, 'FRQ': 'D'}
                        )
print(err)
print(cs_market_cap)
# cs_market_cap.plot(title="DataFrame Plot")
# plt.show()
cs_market_cap.to_excel(f"{DATA_DOLDER}/cs_market_cap.xlsx")
print("==========================================================\n")








print("=================== Timeseries ===========================")
cs_timeseries = ek.get_timeseries(ticker_ric, 
                            start_date=start_date, 
                            end_date=end_date, 
                            interval='daily')
print(cs_timeseries)
cs_timeseries.to_excel(f"{DATA_DOLDER}/cs_timeseries.xlsx")
print("==========================================================\n")




