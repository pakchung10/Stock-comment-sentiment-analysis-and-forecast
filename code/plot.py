#@Author:pakchungy
#@Date:2021/4/28
#@Time:17:37
#@Project_name:codeofrich

import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas.tseries.offsets as pto


def sort_comment(comment_data, price_data, save_path):
    '''
    为评论排序，使用看涨公式映射到每一个交易日中

    :param data: 评论数据
    :return:
    '''
    price_data["pos"] = [0 for i in range(len(price_data))]
    price_data["neg"] = [0 for i in range(len(price_data))]
    for date, score in comment_data.values:
        d = date.date()
        # 判断日期，如果是周六，合并到周五，如果是周日，合并到周一
        if date.weekday() == 6:
            d = (d + pto.DateOffset(days=-1)).date()
        elif date.weekday() == 7:
            d = (d + pto.DateOffset(days=1)).date()
        # print(d)
        if score > 0:
            price_data.loc[d:d, "pos"] += 1
        else:
            price_data.loc[d:d, "neg"] += 1

    # 用看涨公式汇总分数
    price_data["score"] = price_data.apply(lambda x: np.log(((1 + x["pos"]) / (1 + x["neg"]))), axis=1)
    # 对分数进行一阶差分
    # s = price_data["score"].diff()
    # s[0] = 0
    # price_data["score"] = s
    # 平滑处理


    # # 对股价进行一阶差分
    c = price_data["Close"].diff()
    c[0] = 0
    price_data["Close"] = c

    # 把分数和股价归一化
    max_min_scaler = lambda x: (x - np.min(x)) / (np.max(x) - np.min(x))
    price_data['score'] = price_data[['score']].apply(max_min_scaler)
    price_data['Close'] = price_data[['Close']].apply(max_min_scaler)
    print(price_data)
    price_data.to_csv(save_path)
    print("数据已保存")
    return


if __name__ == '__main__':
    # 格林美
    save_path = ".\\stock_price\\sort\\GLM_sort_score_zqj.csv"
    stock_price = ".\\stock_price\\002340.SZ.csv"
    stock_comment = ".\\comment_score\\GLM_score.csv"

    # 宁德时代
    # save_path = ".\\stock_price\\sort\\NDSD_sort_score_zqj.csv"
    # stock_price = ".\\stock_price\\300750.SZ.csv"
    # stock_comment = ".\\comment_score\\NDSD_score.csv"

    # 算分
    price = pd.read_csv(stock_price, usecols=["Date", "Close"], parse_dates=['Date'], index_col=["Date"])
    comment = pd.read_csv(stock_comment, usecols=["评论时间", "score"], parse_dates=['评论时间'])
    sort_comment(comment, price, save_path)

    # 读取保存好的数据
    price = pd.read_csv(save_path, parse_dates=['Date'], index_col=["Date"])
    # 画图
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.plot(price["score"], "b", label="comment")
    plt.plot(price["Close"], "r-", label="price")
    # plt.title("格林美")
    # plt.title("宁德时代")
    # plt.title("格林美")
    # plt.title("宁德时代")
    plt.title("格林美_一阶差分")
    # plt.title("宁德时代_一阶差分")
    plt.legend()
    plt.show()
    # plt.savefig('machine_learning/glm.jpg', dpi=256)
    # plt.savefig('machine_learning/ndsd.jpg', dpi=256)
    print("finsh")