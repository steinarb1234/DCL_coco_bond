
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
start_date = '2017-01-01'
end_date = '2025-01-01'


cs_total_debt, err = ek.get_data(ticker_ric, 
                               [
                                    'TR.TotalDebtOutstanding.date',
                                    'TR.TotalDebtOutstanding',
                                ],
                                parameters={'SDate': start_date, 'EDate': end_date},
                               )
cs_total_debt = cs_total_debt.set_index("Date").drop(columns=["Instrument"])
cs_total_debt.index = pd.to_datetime(cs_total_debt.index).tz_localize(None)

print(err)
print(cs_total_debt)
cs_total_debt.plot()
plt.show()
cs_total_debt.to_excel(f"{DATA_DOLDER}/cs_total_debt.xlsx")




