
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

cs_market_cap, err = ek.get_data(ticker_ric, 
                        [
                            'TR.CompanyMarketCapitalization.date',
                            'TR.CompanyMarketCapitalization',
                        ], 
                        parameters={'SDate': start_date, 'EDate': end_date},
                        )
cs_market_cap = cs_market_cap.set_index("Date").drop(columns=["Instrument"])
cs_market_cap.index = pd.to_datetime(cs_market_cap.index).tz_localize(None)

print(err)
print(cs_market_cap)
cs_market_cap.plot(title="DataFrame Plot")
plt.show()
cs_market_cap.to_excel(f"{DATA_DOLDER}/cs_market_cap.xlsx")






