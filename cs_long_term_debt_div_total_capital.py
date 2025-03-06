
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

cs_long_term_debt_div_total_capital, err = ek.get_data(ticker_ric, 
                        [
                            'TR.F.LTDebtPctofTotCap.date',
                            'TR.F.LTDebtPctofTotCap',
                        ], 
                        parameters={'SDate': start_date, 'EDate': end_date},
                        )
cs_long_term_debt_div_total_capital = cs_long_term_debt_div_total_capital.set_index("Date").drop(columns=["Instrument"])
cs_long_term_debt_div_total_capital.index = pd.to_datetime(cs_long_term_debt_div_total_capital.index).tz_localize(None)

print(err)
print(cs_long_term_debt_div_total_capital)

cs_long_term_debt_div_total_capital.plot(title="DataFrame Plot")
plt.show()
cs_long_term_debt_div_total_capital.to_excel(f"{DATA_DOLDER}/cs_long_term_debt_div_total_capital.xlsx")






