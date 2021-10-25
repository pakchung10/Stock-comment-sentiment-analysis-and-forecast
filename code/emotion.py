#@Author:pakchungy
#@Date:2021/4/27
#@Time:13:02
#@Project_name:codeofrich

import csv
import time
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
import jieba
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.metrics import BigramAssocMeasures
import random
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
import pandas as pd
import numpy as np
from gather import gather

# 读取文本文件
def get_corpus():
    '''
    读取积极与消极语料库(目前还是句子)
    :return:
    '''
    pos_file = ".\\comment\\allcomment\\NDSD\\result\\pos.txt"
    neg_file = ".\\comment\\allcomment\\NDSD\\result\\neg.txt"
    pos_corpus = []
    neg_corpus = []
    with open(pos_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for l in lines:
            # 去掉各种空格
            l = l.strip()
            if l != "":
                pos_corpus.append(l)
    with open(neg_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for l in lines:
            # 去掉各种空格
            l = l.strip()
            if l != "":
                neg_corpus.append(l)
    return pos_corpus, neg_corpus

# 将单个词作为特征
def feature_by_word(words):
    '''
    按单个字作为特征

    :param words: 语料库
    :return:
    '''
    s = ""
    for word in words:
        s += word
    return dict([(word, True) for word in s])

# 把双个词作为特征，并使用卡方统计的方法，选择排名前1000的双词
def feature_by_bigram(words, score_fn=BigramAssocMeasures.chi_sq, n=1000):
    '''
    按双字词语作为特征

    :param words: 语料库
    :param score_fn: 评分函数
    :param n: 取排名靠前的多少个返回
    :return:
    '''
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)  # 使用卡方统计的方法，选择排名前1000的词语
    newBigrams = [u + v for (u, v) in bigrams]
    return feature_by_word(newBigrams)

# 把单个字和词语一起作为特征
def bigram_words(words, score_fn=BigramAssocMeasures.chi_sq, n=1000):
    '''
    单个字和双字词语一起作为特征
    :param words: 语料库
    :param score_fn: 评分函数
    :param n: 取排名靠前的多少个返回
    :return:
    '''
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    new_Bigrams = [u + v for (u, v) in bigrams]
    a = feature_by_word(words)
    b = feature_by_word(new_Bigrams)
    # 把字典b合并到字典a中
    a.update(b)
    return a

def load_corpus(filename):
    '''
    读取自己的语料库，用结巴分词并去掉停用词
    :param filename:
    :return:
    '''
    stop = [line.strip() for line in open('.\\停用词.txt', 'r',
                                          encoding='utf-8').readlines()]
    print(filename)
    f = open(filename, 'r', encoding='utf-8')
    line = f.readline()
    corpus = []
    while line:
        s = line.split('\t')
        participle = jieba.cut(s[0], cut_all=False)
        corpus.append(list(set(participle) - set(stop)))
        line = f.readline()
    f.close()
    return corpus


def feature_by_jieba(n=1000):
    '''
    根据结巴分词的结果作为特征

    :param n:
    :return:
    '''
    posWords = []
    negWords = []
    for items in load_corpus(".\\comment\\allcomment\\NDSD\\result\\pos.txt"):
        for item in items:
            posWords.append(item)
    for items in load_corpus(".\\comment\\allcomment\\NDSD\\result\\neg.txt"):
        for item in items:
            negWords.append(item)
    word_fd = FreqDist()  # 可统计所有词的词频
    con_word_fd = ConditionalFreqDist()  # 可统计积极文本中的词频和消极文本中的词频
    for word in posWords:
        word_fd[word] += 1
        con_word_fd['pos'][word] += 1
    for word in negWords:
        word_fd[word] += 1
        con_word_fd['neg'][word] += 1
    pos_word_count = con_word_fd['pos'].N()  # 积极词的数量
    neg_word_count = con_word_fd['neg'].N()  # 消极词的数量
    # 一个词的信息量等于积极卡方统计量加上消极卡方统计量
    total_word_count = pos_word_count + neg_word_count
    word_scores = {}
    for word, freq in word_fd.items():
        pos_score = BigramAssocMeasures.chi_sq(con_word_fd['pos'][word], (freq,
                                                                          pos_word_count), total_word_count)
        neg_score = BigramAssocMeasures.chi_sq(con_word_fd['neg'][word], (freq,
                                                                          neg_word_count), total_word_count)
        word_scores[word] = pos_score + neg_score
        best_vals = sorted(word_scores.items(), key=lambda item: item[1], reverse=True)[:n]
        best_words = set([w for w, s in best_vals])
    return dict([(word, True) for word in best_words])


def build_feature():
    all_feature = feature_by_jieba(500)
    pos_words = load_corpus(".\\comment\\allcomment\\NDSD\\result\\pos.txt")
    neg_words = load_corpus(".\\comment\\allcomment\\NDSD\\result\\neg.txt")
    pos_features = []
    for items in pos_words:
        a = {}
        for item in items:
            if item in all_feature.keys():
                a[item] = 'True'
        if len(a) == 0:
            continue
        # 为积极文本赋予"pos"
        pos_features.append([a, 'pos'])
    neg_features = []
    for items in neg_words:
        a = {}
        for item in items:
            if item in all_feature.keys():
                a[item] = 'True'
        if len(a) == 0:
            continue
        # 为消极文本赋予"neg"
        neg_features.append([a, 'neg'])
    return pos_features, neg_features


def score(classifier, train, data, tag):
    classifier = SklearnClassifier(classifier)
    classifier.train(train)
    pred = classifier.classify_many(data)
    n = 0
    s = len(pred)
    for i in range(s):
        if (pred[i] == tag[i]):
            n = n + 1
    return n / s


# 处理输入的评论文本，使其成为可预测格式
def build_page(page, feature, stop):
    '''
    处理输入的评论文本，使其成为可预测格式

    :param page: 输入评论
    :return:
    '''
    temp = {}
    # 现采用结巴分词形式处理待测文本
    participle = jieba.cut(page, cut_all=False)
    for words in list(set(participle) - set(stop)):
        if words in feature:
            temp[words] = 'True'
    return temp


def train_classifier(classifier, train_data):
    '''
    训练模型

    :param classifier: 分类器
    :param train_data: 训练数据集
    :return:
    '''
    classifier = SklearnClassifier(classifier)
    classifier.train(train_data)
    return classifier


def predict_page(classifier, page):
    page = build_page(page)
    pred = classifier.classify_many(page)
    return pred


def find_best_classifier():
    '''
    找到最好的分类器的实验

    :return:
    '''
    posFeatures, negFeatures = build_feature()
    # 保存所有分数
    all_score = {"LogisticRegression": [], "SVC": [], "LinearSVC": [], "NuSVC": [], "MultinomialNB": [],
                 "BernoulliNB": []}
    # 做100次实验，取均值
    times = 100
    for i in range(times):
        # 打乱数据
        random.shuffle(posFeatures)
        random.shuffle(negFeatures)
        # 训练测试八二分
        train = posFeatures[:int(0.8 * len(posFeatures))] + negFeatures[:int(0.8 * len(negFeatures))]
        test = posFeatures[int(0.8 * len(posFeatures)):] + negFeatures[int(0.8 * len(negFeatures)):]
        data, tag = zip(*test)  # 分离测试集合的数据和标签，便于测试
        # 初始化所有分类器
        classifier1 = LogisticRegression()  # 逻辑回归
        classifier2 = SVC() # 支持向量机
        classifier3 = LinearSVC()   # 线性支持向量机
        classifier4 = NuSVC()   # 核支持向量分类
        classifier5 = MultinomialNB()   # 朴素贝叶斯
        classifier6 = BernoulliNB() # 伯努利贝叶斯
        all_score["LogisticRegression"].append(score(classifier1, train, data, tag))
        all_score["SVC"].append(score(classifier2, train, data, tag))
        all_score["LinearSVC"].append(score(classifier3, train, data, tag))
        all_score["NuSVC"].append(score(classifier4, train, data, tag))
        all_score["MultinomialNB"].append(score(classifier5, train, data, tag))
        all_score["BernoulliNB"].append(score(classifier6, train, data, tag))
    all_score = pd.DataFrame(all_score)
    # 计算均值
    # print(all_score.mean(), ignore_index=True)
    all_score = all_score.append(all_score.mean(), ignore_index=True)
    print("训练次数为：", times)
    print(all_score.iloc[50])
    # 将结果写进csv
    all_score.to_csv(".\\find_best_classifier.csv", index=False)

def get_score(comment_file, save_path):
    '''

    :return:
    '''
    posFeatures, negFeatures = build_feature()
    classifier = MultinomialNB()    # 朴素贝叶斯效果最佳
    # classifier = LinearSVC()   # 线性支持向量机效果最佳
    train = posFeatures[:] + negFeatures[:]
    classifier = train_classifier(classifier, train)
    # 读取评论
    data = pd.read_csv(comment_file)
    # 加载停用词
    stop = [line.strip() for line in open('.\\停用词.txt', 'r', encoding='utf-8').readlines()]
    feature = feature_by_jieba(1000)
    # 为每条评论进行情感分析
    # for comment, score in data.values:
    #     print(classifier.classify_many(build_page(comment, feature, stop)))
    data["score"] = data.apply(
        lambda x: 1 if classifier.classify_many(build_page(x["评论内容"], feature, stop))[0] == "pos" else -1,
        axis=1)
    data.to_csv(save_path, index=False)


if __name__ == '__main__':

    # find_best_classifier()  # 朴素贝叶斯分类效果更好
    get_score(".\\comment\\allcomment\\格林美吧_post_url(2).csv", ".\\comment_score\\GLM_score.csv")
    # get_score(".\\comment\\allcomment\\格林美吧_post_url(2).csv", ".\\comment_score\\NDSD_score.csv")
    print("finsh")
