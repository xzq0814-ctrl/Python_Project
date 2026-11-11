"""
分类问题：
    多分类交又熵损失：CrossEntropyLoss
    二分类交又熵损失：BCELoss
回归问题：
    MAE：Mean AbsoLute Error，平均绝对误差。
    MSE：Mean Squared Error，均方误差。
    Smooth L1：结合上述两个的特点做的升级，优化。
分类交叉熵损失：CrossEntropyLoss
    设计思路：Loss = - ∑ylog(S(f(x)))
    简单记忆：
        x:样本
        f(x):加权求和
        S(f(x)):处理后的概率
        y:样本 x 属于某一个类别的真实概率。
    CrossEntropyLoss = softmax()+损失计算
"""
import torch
import torch.nn as nn

def dm01():
    # 手动创建样本真实值 -> 公式y
    # y_true = torch.tensor([[0,1,0],[0, 0, 1]],dtype=torch.float)
    y_true = torch.tensor([1, 2])
    # 手动创建样本预测值 -> f(x)
    y_pred = torch.tensor([[0.1, 0.8, 0.1],[0.2, 0.1, 0.7]], requires_grad=True, dtype=torch.float)
    # 创建多分类交叉熵损失函数
    criterion = nn.CrossEntropyLoss()  # 平均损失
    # 计算损失值
    loss = criterion(y_pred, y_true)
    print(loss)

if __name__ == '__main__':
    dm01()