#@Author:pakchungy
#@Date:2021/4/27
#@Time:11:18
#@Project_name:codeofrich

import os
import re

def walkFile(file_path):
    for root, dirs, files in os.walk(file_path):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        file_list = []
        for f in files:
            # print("文件：", os.path.join(root, f))
            file_list.append(os.path.join(root, f))
        return file_list

def gather(path):
    file_list = walkFile(path)
    # print(file_list)
    pos_file_path_list = []
    neg_file_path_list = []
    for file in file_list:
        # if "NDSD_pos" in file:  # 仅是NDSD
        if "pos" in file:
            pos_file_path_list.append(file)
        # if "NDSD_neg" in file:  # 仅是NDSD
        if "neg" in file:
            neg_file_path_list.append(file)
    print("遍历积极语料列表：", pos_file_path_list)
    print("遍历消极语料列表：", neg_file_path_list)

    pos_path = "D:\\PycharmProjects\\codeofrich\\comment\\allcomment\\NDSD\\result\\pos.txt"
    neg_path = "D:\\PycharmProjects\\codeofrich\\comment\\allcomment\\NDSD\\result\\neg.txt"

    # 融合积极语料
    pos_list = []
    for pos_file_path in pos_file_path_list:
        with open(pos_file_path, 'r', encoding='utf-8')as f:
            pos_list.extend(f.readlines())
    # print(type(pos_list))
    # print(len(pos_list))
    with open(pos_path, 'w', encoding="utf-8")as f:
        f.writelines(pos_list)

    print("积极语料总数：", len(pos_list))

    # 融合消极语料
    neg_list = []
    for neg_file_path in neg_file_path_list:
        with open(neg_file_path, 'r', encoding='utf-8')as f:
            neg_list.extend(f.readlines())
    # print(type(neg_list))
    # print(len(neg_list))
    with open(neg_path, 'w', encoding="utf-8")as f:
        f.writelines(neg_list)

    print("消极语料总数：",len(neg_list))
if __name__ == "__main__":
    file_path = "D:\\PycharmProjects\\codeofrich\\comment\\allcomment\\NDSD\\mid_result"
    gather(file_path)
    print("语料库融合完成")