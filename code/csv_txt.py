#@Author:pakchungy
#@Date:2021/4/19
#@Time:21:15
#@Project_name:codeofrich

import pandas as pd
import datetime

def csv_txt(comment_path, comment_name, result_file):
    # 创建一个dataframe存放数据
    data = pd.DataFrame()

    # 读取对应评论文件
    data = pd.read_csv(comment_path + comment_name + '.csv', header=None)
    print("评论文件读取成功")
    print("评论总数为：", len(data))

    # 赋予dataframe列名并输出检查
    data.columns = ['用户名', '评论时间', '评论内容', '点赞数']

    # 创建新data方便作修改
    copy_data = data.copy()
    # print(type(copy_data["评论内容"]))
    # for value in copy_data["评论内容"].values:
    #     print(type(value))

    # 写入txt文本
    with open(result_file, 'a', encoding='utf-8')as f:
        all_num = 0
        success_num = 0
        for value in copy_data["评论内容"].values:
            # value = str(value)
            if type(value) != str:
                pass
            else:
                f.write(value)
                f.write("\n")
                success_num += 1
            all_num += 1
        print("已处理评论数：", all_num)
        print("有效评论数：", success_num)

if __name__ =="__main__":
    # 获取当前时间
    start_time = datetime.datetime.now()
    print(start_time)

    # 获取评论文件的目录
    # path_of_comment = 'D:\\PycharmProjects\\codeofrich\\comment\\allcomment\\'  # 该股票评论的文件夹路径
    # name_of_comment = 'SF_allcomment' #该股票评论的文件名
    # path_result_file = 'D:\\PycharmProjects\\codeofrich\\comment\\allcomment\\SF.txt' #评论结果存放绝对地址

    path_of_comment = 'D:\\PycharmProjects\\codeofrich\\comment\\allcomment\\'  # 该股票评论的文件夹路径
    name_of_comment = '宁德时代吧_post_url(1)' #该股票评论的文件名
    path_result_file = 'D:\\PycharmProjects\\codeofrich\\comment\\allcomment\\NDSD.txt' #评论结果存放绝对地址

    csv_txt(path_of_comment, name_of_comment, path_result_file)