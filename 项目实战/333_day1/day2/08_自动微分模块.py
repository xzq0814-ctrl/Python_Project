"""
权重更新公式：
  W新 = W旧 - 学习率 * 梯度
  梯度 = 损失函数的导数
关于损失函数的导数，无需我们手动计算，因为非常常用，所以 PyTorch模块内置 自动微分模块，专门实现针对于 不同的损失函数求导，
从而实现 结合 反向传播，更新 权重参数w 和偏置参数b
"""
import torch

# 定义变量  记录W旧
w = torch.tensor(10, requires_grad=True,dtype=torch.float)# 参数：初始值，是否求导，数据类型
# 定义损失函数
loss = 2*w**2
# print(f'梯度函数类型：{type(loss.grad_fn)}')
# print(loss.sum())

# 计算梯度，保证loss是一个标量，算完会记录到w.grad属性中
loss.sum().backward()
# 带入公式
w.data = w.data - 0.01 * w.grad
print(f'更新后的权重：{w},loss={loss}')




