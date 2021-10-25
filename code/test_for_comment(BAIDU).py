import pandas as pd
import datetime
from aip import AipNlp
import codecs
import time
import os

startdate = datetime.date(2020, 10, 31).strftime('%Y/%m/%d')
enddate = datetime.date(2020, 9, 18).strftime('%Y/%m/%d')
APP_ID = '23862642'
API_KEY = 'oEbqbjLG92HzuNZ7Qc9P0TkO'
SECRET_KEY = 'q5MCM3XTlefh92OVw9BjOeYprvmvmpa5'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

def get_sentiments(text, dates):
    try:
        sitems = client.sentimentClassify(text)['items'][0]  # 情感分析
        positive = sitems['positive_prob']  # 积极概率
        confidence = sitems['confidence']  # 置信度
        sentiment = sitems['sentiment']  # 0表示消极，1表示中性，2表示积极
        # tagitems = client.commentTag(text, {'type': 9})  # 评论观点
        # propertys=tagitems['prop']#属性
        # adj=tagitems['adj']#描述词
        output = '{}\t{}\t{}\t{}\n'.format(dates, positive, confidence, sentiment)
        f = codecs.open('sentiment.xls', 'a+', 'utf-8')
        f.write(output)
        f.close()
        print('Done')
    except Exception as e:
        print(e)

# def get_content():
#     data = pd.DataFrame(pd.read_excel('eastmoney.xlsx', sheet_name=0))
#     data.columns = ['Dates', 'viewpoints']  # 重设表头
#     data = data.sort_values(by=['Dates'])  # 按日期排列
#     vdata = data[data.Dates >= startdate]  # 提取对应日期的数据
#     newvdata = vdata.groupby('Dates').agg(lambda x: list(x))  # 按日期分组，把同一天的评论并到一起
#     return newvdata

def get_comment(file_path, file_name):
    # data = pd.DataFrame(pd.read_csv(path + 'SF_allcomment.csv'))
    # data.columns = ['用户名', '评论时间', '评论内容', '点赞数']
    # data = data.sort_values(by=['评论时间'])
    # vdata = data[data['评论时间'] >= startdate]
    # newdata = vdata.groupby('评论时间').agg(lambda x: list(x))
    # return newdata

    # 获取当前时间
    start_time = datetime.datetime.now()
    print(start_time)
    # 获取评论文件的目录
    # 创建一个dataframe存放数据
    data = pd.DataFrame()
    # 读取对应评论文件
    data = pd.read_csv(file_path + file_name + '.csv', header=None)
    data.columns = ['用户名', '评论时间', '评论内容', '点赞数']
    print("评论文件读取成功")
    print("评论总数为：", len(data))
    # print(data)
    return data

if __name__ == "__main__":
    path = 'D:\\PycharmProjects\\codeofrich\\comment\\allcomment\\'  # 该股票评论的文件夹路径
    name_of_comment = 'SF_allcomment'   #该股票评论的文件名
    viewdata = get_comment(path, name_of_comment)
    # print(viewdata)
    print("评论总数：",viewdata.shape[0])
    for i in range(viewdata.shape[0]):
        time.sleep(0.06)
        print('正在处理第{}条,还剩{}条'.format(i, viewdata.shape[0] - 1))
        dates = viewdata['评论时间'][i]
        for view in viewdata['评论内容'][i]:
            print(view)
            get_sentiments(view, dates)