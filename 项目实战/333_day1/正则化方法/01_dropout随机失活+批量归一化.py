"""
正则化的作用：
    缓解模型的过拟合情况。
正则化的方式：
    L1正则化：权重可以变为0，相当于：降维。
    L2正则化：权重可以无限接近0
    DropOut：随机失活，每批次样本训练时，随机让一部分神经元死亡，防止一些特征对结果的影响较大（防止过拟合)

    BN（批量归一化)：…
    思路:
    先对数据做标准化（会丢失一些信息），然后再对数据做缩放（Λ，理解为：W权重）和平移（β，理解为：b偏置），再找补回一些信息。
    应用场景：批量归一化在计算机视觉领域使用较多。

    BatchNorm1d：主要应用于全连接层或处理一维数据的网络，例如文本处理。它接收形状为（N，num_features）的张量作为输入。
    BatchNorm2d：主要应用于卷积神经网络，处理二维图像数据或特征图。它接收形状为（N，C，H，W）的张量作为输入。
    BatchNorm3d：主要用于三维卷积神经网络（3D CNN），处理三维数据，例如视频或医学图像。它接收形状为（N，C，D，H，W）的张量作为输入。
"""

import torch
import torch.nn as nn

def regular01():
    # 创建隐藏层 输出结果
    t1 = torch.randint(0, 10, size=(1, 4)).float()
    print(f't1:{t1}')
    # 一层线性神经网络   创建全连接层（充当线性层）
    linear1 = nn.Linear(4, 5)
    # 加权求和
    l1 = linear1(t1)
    print(f'l1: {l1}')
    # relu激活函数
    output = torch.relu(l1)
    print(f'output: {output}')
    # dropout 随机失活  -> 只有训练阶段有，测试阶段没有
    dropout = nn.Dropout(p=0.5) # 每个神经元有50%的概率被kill
    d1 = dropout(output)        # 未被失活的进行缩放，比例 1/(1-p) = 2
    print(f'd1(随机失活后的数据): {d1}')

def feature_scaling2():
    # 1. 创建图像样本数据 1张图片，2个通道，3行4列（像素点）
    input_2d = torch.randn(size=(1,2,3,4))
    print(f'input_2d:{input_2d}')
    # 2. 创建批量归一化层（BN）
    # 参数：1 输入特征数=图片通道数，2噪声值(小常数)，3动量值 计算移动平均统计量，4使用可学习的变换参数（λ，β） 对归一化后数据进行缩放平移
    bn2d = nn.BatchNorm2d(num_features=2,eps=1e-5, momentum=0.1, affine=True)
    # 对数据进行批量归一化处理
    output_2d = bn2d(input_2d)
    print(f'output_2d:{output_2d}')

def feature_scaling1():
    # 2行2列：两条样本，每个样本有俩特征
    input_1d = torch.randn(size=(2,2))
    print(f'input_1d:{input_1d}')
    # 创建线性层
    linear1 = nn.Linear(2,4)
    # 对数据进行线性变换
    l1 = linear1(input_1d)
    print(f'l1:{l1}')
    # 创建BN层
    bn1d = nn.BatchNorm1d(num_features=4)
    # 对线性处理结果l1 进行批量归一化处理
    output_1d = bn1d(l1)
    print(f'output_1d:{output_1d}')

if __name__ == '__main__':
    # regular01()
    # feature_scaling2()
    feature_scaling1()