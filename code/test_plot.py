# -*- coding: utf-8 -*-
'''
保存暂时弃用的代码
'''
# @Time : 2021/3/22 9:23 
# @Author : LINYANZHEN
# @File : test.py
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import math
from snownlp import SnowNLP
import os
import math
import pandas
import numpy as np
import csv
import datetime
import matplotlib.pyplot as plt
import random

# path = "comment/analyzed/stock_GLMcomments_analyzed.csv"
path = "comment/analyzed/stock_SFcomments_analyzed.csv"
# new_path = "comment/analyzed/stock_GLMcomments_analyzed_sort.csv"
new_path = "comment/analyzed/stock_SFcomments_analyzed_sort.csv"

stock_price_path = "stock_price/002352 - 副本.csv"


# stock_price_path = "stock_price/002340.SZ - 副本.csv"


# path = "comment/snownlp/SF_allcomment_snownlp.csv"
# new_path = "comment/snownlp/SF_allcomment_snownlp_sort.csv"


# path = "comment/snownlp/GLM_allcomment_snownlp.csv"
# new_path = "comment/snownlp/GLM_allcomment_snownlp_sort.csv"


def summarize_score():
    data = pandas.read_csv(path)
    data.columns = ['用户名', '评论时间', '评论内容', '点赞数', "snow评分"]
    time = data["评论时间"]
    for i in range(len(time)):
        time[i] = time[i][:10]
    # print(time)
    time = set(data["评论时间"].tolist())
    # print(time)
    df = pandas.DataFrame(columns=["date", "sum"])
    count = 0
    for t in time:
        d = data[data["评论时间"] == t]
        sum = 0
        pos = 0
        neg = 0
        for i in d.values:
            # if i[4] >= 0.6:
            #     # pos += 1 + math.log(i[3] + 1, 2)
            #     pos += 1
            # # elif i[4] <= 0.4:
            # else:
            #     # neg += 1 + math.log(i[3] + 1, 2)
            #     neg +=1
            sum += i[4]
        # sum = (pos / (pos + neg + 0.0001) - 0.5) * math.log(len(d.values) + 1, 2)
        # sum = np.log((1 + pos) / (1 + neg))
        # sum += (i[3] + 1) * i[4]
        sum /= len(d.values)
        df.loc[count] = {"date": t, "sum": sum}
        count += 1
    print(df)
    df = df.sort_values(by="date")
    print(df)
    # 创建一个新csv文件存放获取的所有评论以及分数
    with open(new_path, 'w', encoding='utf-8', newline="")as f:
        csv_writer = csv.writer(f)
        # csv_writer.writerow(['用户名', '评论时间', '评论内容', '点赞数'])
        for i in df.values:
            # print(i)
            csv_writer.writerow(i)


def draw():
    data = pandas.read_csv(new_path, header=None, parse_dates=True)
    data.columns = ["date", "sum"]
    datestart = "2019-12-02"
    dateend = "2020-10-31"

    datestart = datetime.datetime.strptime(datestart, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(dateend, '%Y-%m-%d')
    date_list = []
    date_list_without = []
    date_list.append(datestart.strftime('%Y-%m-%d'))
    while datestart < dateend:
        # 日期叠加一天
        datestart += datetime.timedelta(days=+1)
        # 日期转字符串存入列表
        date_list.append(datestart.strftime('%Y-%m-%d'))
    score_list = []
    for i in range(len(date_list)):
        # t = datetime.datetime.strptime(date_list[i], '%Y-%m-%d')
        # if t.weekday() in (5, 6):
        #     # 是星期六日，这些天的分数加到周五
        #     if date_list[i] in data["date"].tolist():
        #         score_list[-1] += data[data["date"] == date_list[i]]["sum"]
        #     else:
        #         # 对于没有分数的那一天，即那天没有评论，值取中性
        #         score_list[-1] += (1 / (1 + 1 + 0.0001) - 0.5) * math.log(2 + 1, 2)
        #         # score_list.append(score_list[-1])
        #     # date_list.remove(date_list[i])
        # else:
        if date_list[i] in data["date"].tolist():
            score_list.append(data[data["date"] == date_list[i]]["sum"])
        else:
            # 对于没有分数的那一天，即那天没有评论，值取中性
            score_list.append((1 / (1 + 1 + 0.0001) - 0.5) * math.log(2 + 1, 2))
            # score_list.append(score_list[-1])
        # date_list_without.append(date_list[i])

    print(len(date_list_without))
    print(len(score_list))
    plt.subplot(2, 1, 1)
    plt.plot(date_list, score_list, "b", label="comment")
    # # 画一条中性的基准线，方便观察
    # plt.plot(date_list, [0 for i in range(len(date_list))], "r",
    #          label="baseline")
    plt.legend()
    plt.subplot(2, 1, 2)
    stock_data = pandas.read_csv(stock_price_path, usecols=['trade_date', 'close'])
    # stock_data = stock_data.iloc[::-1]
    # stock_data.index.name = "trade_date"
    print(stock_data["close"])
    plt.plot(stock_data["close"], "r-")
    plt.show()

    # fig, ax1 = plt.subplots(figsize=(12, 2.4))
    # ax2 = ax1.twinx()
    # ax1.set_ylabel('price')
    # ax2.set_ylabel('comment score')
    # ax1.plot(stock_data, 'r-')
    # ax2.plot(data, 'g-')
    # plt.title('bqlg(600733)')
    # plt.show()


if __name__ == '__main__':
    summarize_score()
    draw()
