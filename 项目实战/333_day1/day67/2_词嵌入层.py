"""
RNN介绍：
全称叫 Recurrent neural network，循环神经网络，主要处理序列数据的。
序列数据：后边数据对前边的数据有依赖，例如：天气预测，股市分析，文本生成。.
组成：
词嵌入层
循环网络层
输出层
词嵌入层介绍（作用）：
把词（或者词对应的索引）转成词向量。
"""
import torch
import torch.nn as nn
import jieba  # jieba 分词器
# 演示词嵌入层的API
def dm01():
    text = '北京冬奥的进度条已经过半，不少外国运动员在完成自己的比赛后踏上归途。'
    words = jieba.__lcut(text)
    print(f'分词结果：{words}')
    # 创建词嵌入层
    embed = nn.Embedding(len(words), 4)
    # 获取每个词对象的下标索引
    for index,word in enumerate(words):
        # 把词索引(张量)转成词向量
        word_vector = embed(torch.tensor(index)) # 随机的
        print(f'词：{word},\t\t词向量：{word_vector}')


if __name__ == '__main__':
    dm01()