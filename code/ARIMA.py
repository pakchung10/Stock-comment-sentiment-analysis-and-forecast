#@Author:pakchungy
#@Date:2021/4/29
#@Time:15:09
#@Project_name:codeofrich

from __future__ import print_function
import pandas as pd
import numpy as np
from scipy import  stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot

stock_price = ".\\stock_price\\002340.SZ.csv"
price = pd.read_csv(stock_price, usecols=["Date", "Close"], parse_dates=['Date'], index_col=["Date"])
plt.plot(price['Date'], "b", label="date")
plt.plot(price['Close'], "r-", label="price")

plt.legend()
plt.show()