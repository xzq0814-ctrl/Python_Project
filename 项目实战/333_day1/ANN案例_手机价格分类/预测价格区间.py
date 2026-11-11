"""
ANN（人工神经网络）案例：手机价格分类案例。
背景：
基于手机的20列特征→预测手机的价格区间(4个区间），可以用机器学习做，也可以用深度学习做（推荐）
ANN案例的实现步骤：
    1.构建数据集。
    2.搭建神经网络。
    3.模型训练。
    4.模型测试。
"""
# 导包
import torch                                       # pytorch框架 封装张量的操作
from torch._dynamo.polyfills import os
from torch.utils.data import TensorDataset         # 数据集对象  数据->Tensor->数据集->数据加载器
from torch.utils.data import DataLoader            # 数据加载器
import torch.nn as nn                              # 封装神经网络的操作
import torch.optim as optim                        # 优化器
from sklearn.model_selection import train_test_split  # 训练集和测试集的划分
import matplotlib.pyplot as plt                    # 绘图
import numpy as np                                 # 矩阵操作
import pandas as pd                                # 数据处理
import time
from torchsummary import summary                   # 模型结构可视化


# todo 1. 构建数据集
def create_dataset():
    # 加载csv文件数据集
    data1 = pd.read_csv('./train.csv')  # 训练集 2000
    data2 = pd.read_csv('./test.csv')   # 测试集 1000
    # print(f' data:{data2.head()}')
    # print(f' data:{data2.shape}')
    # 获取x 特征列 和 y 标签列
    x_train,y_train = data1.iloc[:,:-1],data1.iloc[:,-1]
    x_test,y_test = data2.iloc[:,:-1],data2.iloc[:,-1]
    # print(f'x:{x.head()},{x.shape}')
    # print(f'y:{y.head()},{y.shape}')
    # 转成浮点型
    x_train = x_train.astype(np.float32)
    x_test = x_test.astype(np.float32)
    # 把数据集封装成张量数据集
    train_dataset = TensorDataset(torch.tensor(x_train.values),torch.tensor(y_train.values))
    test_dataset = TensorDataset(torch.tensor(x_test.values),torch.tensor(y_test.values))
    # print(f'train_dataset:{train_dataset},test_dataset:{test_dataset}')
    #                                   20 充当 输入特征数  4 输出标签数
    return train_dataset,test_dataset, x_train.shape[1],len(np.unique(y_train))
# todo 2.搭建神经网络
class NetModel(nn.Module):
    def __init__(self, input_dim, output_dim): # 输入与输出
        # 初始化父类成员
        super().__init__()
        # 搭建神经网络
        self.linear1 = nn.Linear(input_dim, 128)
        self.linear2 = nn.Linear(128, 256)
        self.output = nn.Linear(256, output_dim)

    def forward(self, x):
        # 隐藏层一： 加权求和+激活函数relu
        x =torch.relu(self.linear1(x))
        # 隐藏层二：一样的
        x = torch.relu(self.linear2(x))
        # 输出层：只需要加权求和。后续用多分类交叉熵损失函数CrossEntropyLoss替代
        x = self.output(x)
        return x

# todo 3.模型训练。
def train(train_dataset, input_dim, output_dim):
    # 创建数据加载器
    train_loader = DataLoader(train_dataset, batch_size=20, shuffle=True)
    # 创建神经网络模型
    model = NetModel(input_dim, output_dim)
    # 损失函数
    criterion = nn.CrossEntropyLoss()
    # 优化器对象
    optimizer = optim.SGD(model.parameters(), lr=0.001)
    # 模型训练
    epochs = 100
    for epoch in range(epochs):
        total_loss, batch_num = 0.0, 0
        start_time = time.time()
        for x, y in train_loader:
            # 切换模型（状态）
            model.train() # 训练模式   model.eval() 测试模式
            # 模型预测
            y_pred = model(x)
            #计算损失
            loss = criterion(y_pred, y)
            # 梯度清零 反向传播 优化参数
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # 累计损失值
            total_loss += loss.item()   # 把本轮的每批次 平均损失累计起来
            batch_num += 1
        print(f'epoch:{epoch+1}, loss:{total_loss/batch_num:.4f}, time:{time.time()-start_time:.2f}s')
    # 保存模型参数
    # print(f'\n\n模型参数信息：{model.state_dict()}\n\n')
    torch.save(model.state_dict(), './model.pth')  # pth pkl pickle 均可

# todo 4.模型测试。
def evaluate(test_dataset, input_dim, output_dim):
    # 创建神经网络分类对象
    model = NetModel(input_dim, output_dim)
    # 加载模型参数
    model.load_state_dict(torch.load('./model.pth'))
    # 创建测试集数据加载器
    test_loader = DataLoader(test_dataset, batch_size=10, shuffle=False)
    # 定义变量  记录预测正确的样本数
    correct = 0
    # 从数据加载器中获取每批次的数据
    for x, y in test_loader:
        # 模型切换
        model.eval()
        y_pred = model(x)
        # print(f'y_pred:{y_pred}')
        # 根据加权求和得到类别，用argmax()获取最大值对应下标
        y_pred = torch.argmax(y_pred, dim=1)    # dim=1 表示逐行处理
        # print(f'y_pred:{y_pred}')
        # print(f'y:{y}')
        # 统计预测正确样本个数
        # print(y_pred == y)
        # print((y_pred == y).sum())
        correct += (y_pred == y).sum()
    # 模型预测结束，打印准确率
    print(f'accuracy:{100 * correct / len(test_dataset):.2f}%')

if __name__ == '__main__':
    # 准备数据集
    train_dataset, test_dataset, input_dim, output_dim = create_dataset()
    # 构建神经网络模型
    model = NetModel(input_dim, output_dim)
    # 计算模型参数      批次大小， 输入特征数
    # summary(model, input_size=(16, input_dim))
    # 模型训练
    train(train_dataset, input_dim, output_dim)
    # 模型测试
    evaluate(test_dataset, input_dim, output_dim)