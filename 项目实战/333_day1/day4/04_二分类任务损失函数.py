"""
二分类任务的损失函数（BCELoss）：
公式：
Loss = -ylog(预测值）- (1- y)log(1- 预测值)
细节：
因为公式中没有包含Sigmoid激活函数，所以使用BCELoss的时候，还需要手动指定Sigmoid.

todo:演示回归任务的损失函数介绍.
回归任务常用损失函数如下：
    MAE: Mean Absolute Error，平均绝对误差.
        公式:  误差绝对值之和/样本总数
        类似于L1正则化，权重可以降维0，数据会变得稀疏。
    弊端：
        在0点不平滑，可能错过最小值.
    MSE: Mean Squared Error，均方误差. 欧氏距离
        公式： 误差平方之和/样本总数
         如果差值过大，可能存在梯度爆炸的情况，
    Smooth L1:
    就是基于MAE和MSE做的综合，在[-1，1]是L2（MSE），其它段时L1.
    这样既解决了L1不平滑的问题（0点不可导，可能错过最小值）
    又解决了L2（MSE）的梯度爆炸的问题
"""
import torch
import torch.nn as nn

def dm01():
    y_true = torch.tensor([0, 1, 0], dtype=torch.float)
    y_pred = torch.tensor([0.6912, 0.5414, 0.3521])
    criterion = nn.BCELoss()
    loss = criterion(y_pred, y_true)  # mean -> 均值
    print(f'损失值: {loss}')

def ret01():
    y_true = torch.tensor([2.0, 2.0, 2.0], dtype=torch.float)
    y_pred = torch.tensor([1.0, 1.4, 1.9],requires_grad=True)
    criterion = nn.L1Loss()
    loss = criterion(y_pred, y_true)
    print(f'MAE: {loss}')

def ret02():
    y_true = torch.tensor([2.0, 2.0, 2.0], dtype=torch.float)
    y_pred = torch.tensor([1.0, 1.4, 1.9],requires_grad=True)
    criterion = nn.MSELoss()
    loss = criterion(y_pred, y_true)
    print(f'MSE: {loss}')

def ret03():
    y_true = torch.tensor([2.0, 2.0, 2.0], dtype=torch.float)
    y_pred = torch.tensor([1.0, 1.4, 1.9],requires_grad=True)
    criterion = nn.SmoothL1Loss()
    loss = criterion(y_pred, y_true)
    print(f'Smooth L1: {loss}')
if __name__ == '__main__':
    # dm01()
    ret01()
    ret02()
    ret03()