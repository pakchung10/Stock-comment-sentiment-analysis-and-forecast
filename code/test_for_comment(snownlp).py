#editor:pakchungy
#date:2021-03-19
import numpy as np
import pandas as pd
import os
from snownlp import SnowNLP
import datetime
import csv

#获取当前时间
start_time = datetime.datetime.now()
print(start_time)

#获取评论文件的目录
path = 'D://PycharmProjects//codeofrich//comment//' #该股票评论的文件夹路径
name_of_comment = 'SF_allcomment'
#创建一个dataframe存放数据
data = pd.DataFrame()

#读取对应评论文件
data = pd.read_csv(path + name_of_comment + '.csv', header=None)
print("评论文件读取成功")
print("评论总数为：",len(data))
# print(data)

#赋予dataframe列名并输出检查
data.columns = ['用户名', '评论时间', '评论内容', '点赞数']

#创建新data方便作修改
copy_data = data.copy()

# for i in copy_data.values:
#     print(i)

#调用snownlp对评论赋予分数
score_snownlp = []
for i in copy_data['评论内容']:
    if type(i) == float:
        score_snownlp.append(0)
    else:
        text = SnowNLP(i)
        result = text.sentiments
        score_snownlp.append(result)
print("snownlp评分工作完成")
finish1time = datetime.datetime.now()
print('评分时间:',(finish1time-start_time).seconds,'seconds')
# print(score_snownlp)
#
#在新data存放分数
copy_data['snownlp分数'] = score_snownlp
# print(copy_data)
print("评论总数：",len(copy_data))
print("新data（snownlp）")
# print(copy_data)
print("snownlp评分已放入复制框架")
print(copy_data['snownlp分数'])

# 创建一个新txt文件存放获取的所有评论以及分数
new_path = "D://PycharmProjects//codeofrich//comment//"
with open(new_path + 'SF_allcomment_snownlp.csv', 'w', encoding='utf-8', newline="")as f:
    for i in copy_data.values:
        print(i)
        # csv_writer.writerow = (['用户名', '评论时间', '评论内容', '点赞数', '分数'])
        csv_writer = csv.writer(f)
        csv_writer.writerow(i)
print("新数据csv写入完成")
finish2time = datetime.datetime.now()
print('工作时长:',(finish2time-start_time).seconds,'seconds')