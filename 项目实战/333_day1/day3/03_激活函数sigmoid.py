"""
案例：
绘制激活函数Sigmoid的函数图像和导数图像。
Sigmoid激活函数介绍：
    激活函数的目的：
        给模型增加非线性功能，让模型（神经元）既可以做分类，还可以做回归问题。
        激活函数的分类：
            Sigmoid:
            ReLU:
            Tanh:
            Softmax:
        Sigmoid激活函数：
            主要应用于二分类的输出层，且适用于浅层神经网络（不超过5层）。
            数据在[-6，6]之间有效果，在[-3，3]之间效果明显。
            求导后范围在[0，0.25]
        细节：
            绘制激活函数图像时出现以下提示，需要将anaconda3/Lib/site-packages/torch/lib目录下的Libiomp5md.dll文件删除
            OMP: Error #15: Initiatizing Libiomp5md.dll, but found Libiomp5md.dll already initialized.
        Tanh:
            主要应用于隐藏层，且适用于浅层神经网络（不超过5层）。
            数据在[-3，3]之间有效果，在[-1，1]之间效果明显，
            会将数据值映射到：[-1，1]求导后范围在[0，1]，
            较之于Sigmoid，收敛速度快。
        ReLU:
计算公式为：max（0，X），计算量相对较小，训练成本低。
多应用于隐藏层，且适合深层神经网络。求导后，值要么是0，要么是1，较之于Tanh，收敛速度更快。
默认情况下ReLU只考虑正样本，可以使用LeakyReLU，PReLU来考虑正负样本。
"""
# softmax
from matplotlib import pyplot as plt
import torch
plt.rcParams['font.sans-serif']=['SimHei']  #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False    #用来正常显示负号
#1.定义张量，记录：分类数据.
scores = torch.tensor([0.2, 0.02, 0.15, 0.15, 1.3, 0.5, 0.06, 1.1, 0.05, 3.75])
#2.dim = θ，按行计算
probabilities = torch.softmax(scores, dim=0)
print(probabilities)

