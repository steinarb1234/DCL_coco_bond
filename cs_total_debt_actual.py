
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


cs_total_debt_actual, err = ek.get_data(ticker_ric, 
                               [
                                    'TR.TotalDebtActValue.date',
                                    'TR.TotalDebtActValue',
                                ],
                                parameters={'SDate': start_date, 'EDate': end_date},
                               )
# cs_total_debt['Date'] = pd.to_datetime(cs_total_debt['Date']).dt.date
cs_total_debt_actual = cs_total_debt_actual.set_index("Date").drop(columns=["Instrument"])
cs_total_debt_actual.index = pd.to_datetime(cs_total_debt_actual.index).tz_localize(None)

print(err)
print(cs_total_debt_actual)
cs_total_debt_actual.plot()
plt.show()
cs_total_debt_actual.to_excel(f"{DATA_DOLDER}/cs_total_debt_actual.xlsx")




