"""
基于杰伦歌词来训练模型，用给定的起始词，结合长度，来进行AI歌词生成。
实现步骤：
1．获取数据，进行分词，获取词表。
2.数据预处理，构建数据集。
3.搭建RNN神经网络。
4.训练模型。
5.模型预测。
"""
#导包
import torch
import jieba
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
import time

# 1 获取数据，进行分词，获取词表。
def build_vocab():
    # 记录：去重后所有的词，每行文本分词结果
    unique_words, all_words = [], []
    # 遍历数据集，获取到每行文本
    for line in open('./jaychou_lyrics.txt','r',encoding='utf-8'):
        words = jieba.__lcut(line)
        all_words.append(words)
        for word in words:
            if word not in unique_words:
                unique_words.append(word)
    # 去重后词的数量
    word_count = len(unique_words)
    # 构建词表 字典形式，例如：{想要'：0，'有'：1，'直升机'：2，'\n'：3，...'冠军'：5701，'要大卖'：5702}
    word_index = {word:i for i, word in enumerate(unique_words)}
    # 歌词文本用词表索引表示
    idx = []
    # 获取每一行的词的索引
    for words in all_words:
        tmp = []
        for word in words:
            tmp.append(word_index[word])
        # 每行歌词用空格隔开
        tmp.append(word_index[' '])
        idx.extend(tmp) # 列表中添加文本而不是嵌套的列表
    return unique_words, word_index, word_count, idx

# 2 数据预处理，构建数据集。 数据->Tensor->数据集对象->数据加载器
# 定义数据集类，继承 torch.utils.data.Dataset
class LyricsDataset(torch.utils.data.Dataset):
    def __init__(self, idx, num_chars):
        # 文档数据中词对应索引
        self.idx = idx
        # 每次拿的词个数
        self.num_chars = num_chars
        self.idx_count = len(self.idx)
        # 句子数量
        self.number = self.idx_count // self.num_chars
    def __len__(self):
        return self.number
    def __getitem__(self, index):
        start = min(max(index, 0), self.number - self.num_chars - 1)
        end = start + self.num_chars
        x = self.idx[start:end] # 输入
        y = self.idx[start+1:end+1]
        return torch.tensor(x), torch.tensor(y)
# 3 搭建RNN神经网络模型
class TextGenerator(nn.Module):
    def __init__(self,unique_word_count):  # 去重词的数量
        super().__init__()
        # 初始化词嵌入层：词的数量，词向量的维度
        self.ebd = nn.Embedding(unique_word_count,128)
        # 循环网络层：词向量维度，隐藏层维度：256，网络层数：1
        self.rnn = nn.RNN(128,256,1)
        # 输出层（全连接层）：特征向量维度（和隐藏向量维度一致），词表中词个数
        self.out = nn.Linear(256,unique_word_count)

    # 前向传播方法
    def forward(self,inputs,hidden):
        # 初始化词嵌入层处理
        embd = self.ebd(inputs)  # embd格式：（batch句子数量，句子长度，词向量维度）
        # rnn 处理
        output, hidden = self.rnn(embd.transpose(0,1),hidden)
        # 全连接，输入是二维数据，词数量 * 词维度
        output = self.out(output.reshape(shape=(-1,output.shape[-1])))
        return output, hidden
    # 隐藏层初始化方法
    def init_hidden(self,bs):
        # [网络层数，batch，隐藏层向量维度]
        return torch.zeros(1,bs,256)
# 训练模型
def train():
    # 构建词典
    unique_words, word_to_index, word_count, corpus_idx = build_vocab()
    # 获取数据集
    lyrics = LyricsDataset(corpus_idx, 32)
    # 初始化神经网络模型
    model = TextGenerator(word_count)   # 预测5703每个词的概率
    # 创建数据加载器对象
    lyrics_dataloader = DataLoader(lyrics, batch_size=5, shuffle=True)
    # 定义损失函数
    criterion = nn.CrossEntropyLoss()
    # 定义优化器
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    # 开始训练
    epochs = 50
    # 记录本轮开始训练时间，迭代(批次)次数，训练总损失
    start, iter_num, total_loss = time.time(), 0, 0.0
    for epoch in range(epochs):
        # 本轮各批次训练
        # 调用getitem()方法，获取每个样本的数据和标签
        for x,y in lyrics_dataloader:
            # 获取隐藏层初始值
            hidden = model.init_hidden(5)
            # 模型计算
            output, hidden = model(x,hidden)
            # 计算损失,y形状{batch，seq_len句子长度,词向量维度}-> 转成一维向量->每个词的下标索引
            y = torch.transpose(y, 0, 1).reshape(shape=(-1,))
            loss = criterion(output, y)
            # 梯度清零，反向传播，更新参数
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # 累计损失（平均）  迭代次数
            total_loss += loss.item()
            iter_num += 1
        print(f'epoch {epoch+1}, time: {time.time() - start:.2f}s, loss {total_loss/iter_num:.4f}')
    # 保存模型
    torch.save(model.state_dict(), './model/text_generator.pth')
# 模型测试
def evaluate(start_word,length):
    # 构建词典
    unique_words, word_to_index, word_count, corpus_idx = build_vocab()
    # 获取模型
    model = TextGenerator(word_count)
    # 加载模型参数
    model.load_state_dict(torch.load('./model/text_generator.pth'))
    # 获取隐藏层初始值
    hidden = model.init_hidden(1)
    # 将输入词 转换 索引
    word_idx = word_to_index[start_word]
    # 定义列表存放预测词的索引
    generate_sentence = [word_idx]
    # 遍历句子长度 获取每个词
    for _ in range(length):
        # 模型预测
        output, hidden = model(torch.tensor([[word_idx]]), hidden) # 输入二维
        # 获取预测结果     从所有5703词的概率找最大值对应索引
        word_idx = torch.argmax(output)
        # 添加到列表中
        generate_sentence.append(word_idx)
    # 将索引转成词，打印
    for index in generate_sentence:
        print(unique_words[index], end='')


if __name__ == '__main__':
    # 获取数据，进行分词，获取词表。
    unique_words, word_index, word_count, idx = build_vocab()
    # dataset = LyricsDataset(idx, 5)
    # x, y = dataset[2]
    # print(f'x:{x}, y:{y}')
    # 创建模型对象
    # model = TextGenerator(word_count)
    # 查看参数
    # for name,param in model.named_parameters():
    #     print(f'参数名称:{name}, 参数维度:{param.shape}')
    # 训练并保存模型
    # train()
    evaluate('不要', 60)




