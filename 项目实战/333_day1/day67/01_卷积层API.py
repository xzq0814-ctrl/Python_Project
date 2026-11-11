"""
演示卷积层的API，用于提取图像的局部特征，获取：特征图(FeatureMap）
卷积神经网络介绍：
    概述: 全称叫：Convolutional neural network，即：包含卷积层的神经网络。
    组成：
        卷积层(Convolutional）：
            用于提取图像的局部特征，结合卷积核（每个卷积核=1个神经元）实现，处理后的结果叫：特征图。
        池化层(Pooling)：
            用于 降维，降采样
        全连接层(Full Connected，fc，Linear):
            用于预测结果，并输出结果的。
特征图计算方式：
N = (W - F + 2*P) / S  + 1
W：输入图像的大小
F：卷积核的大小
P：填充的大小
S：步长
N：输出图像的大小（特征图大小）
"""

import torch
import torch.nn as nn
import matplotlib.pyplot as plt

img = plt.imread('../../../Py_learn/钟离.jpeg')
# print(f'{img},{img.shape}')











