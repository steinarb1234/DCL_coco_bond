
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


# Set eikon api key from config file
cfg = cp.ConfigParser()
cfg.read('eikon.config')
ek.set_app_key(cfg['eikon']['app_key'])

ticker_ric = "CSGN.S^F23"
start_date = '2018-01-01'
end_date = '2025-01-01'


print("================= Close price timeseries ==================")
cs_close = ek.get_timeseries(ticker_ric, 
                            fields="Close",
                            start_date=start_date, 
                            end_date=end_date, 
                            interval='daily')
cs_close = cs_close[["CLOSE"]].rename(columns={"CLOSE": "Close"})
print(cs_close)
cs_close.to_excel(f"{DATA_DOLDER}/cs_close.xlsx")
cs_close.plot()
plt.show()
print("==========================================================\n")




