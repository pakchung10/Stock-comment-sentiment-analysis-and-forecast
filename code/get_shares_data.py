#@Author:pakchungy
#@Date:2021-03-19
#@Time:11:18
#@Project_name:codeofrich

from numpy import *
import tushare as ts
import pandas as pd

pro = ts.pro_api('9a9bd2445e9b0fb2e34b2449269d3ecb369edd10adeffbc84cf2631e') #个人接口
df = pro.daily(ts_code='002352.sz', start_date='20200101', end_date='20201231') #ts_code股票代码，start_date开始日期，end_date结束日期
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
data = pd.DataFrame()
file=open("D://PycharmProjects//codeofrich//002352.sz-20191130_20201031","w+")
file.write(str(df))
file.close()
print(df)