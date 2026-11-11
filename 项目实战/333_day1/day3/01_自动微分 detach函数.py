"""
演示 detach()函数的功能，解决 白动微分的弊端.
回顾:
自动微分=求导，即:基于损失函数，计算梯度.
结合权重更新公式:w新=w旧-学习率* 梯度，来更新权重的.

张量设置了自动微分，就不能直接转成numpy的ndarray对象了
需要通过detach函数
"""
import torch

t1 = torch.tensor([10,20], requires_grad=True, dtype=torch.float)
print(f't1:{t1},type:{type(t1)}')

# n1 = t1.numpy()     # 报错
n1 = t1.detach().numpy()
print(f'n1:{n1},type:{type(n1)}')

# 测试函数
t2 = t1.detach()
print(f't2:{t2},type:{type(t2)}')
t1.data[0] = 100   # 共享内存
print(f't1:{t1},type:{type(t1)}')
print(f't2:{t2},type:{type(t2)}')
# 判断t1,t2 能否自动微分
print(f't1:{t1.requires_grad}')
print(f't2:{t2.requires_grad}')
#*************************************************************************
"""
演示自动微分的真实应用场景。
1.先前向转播(正向传播)计算出 预测值(z)
2.基于损失函数，结合预测值(z)和真实值(y)，来计算梯度.
3.结合权重更新公式w新=w旧-学习率*梯度，来更新权重。
"""
# 二行五列，全1矩阵
x = torch.ones(2,5)
print(f'x:{x}')
# 二行三列，全0矩阵
y = torch.zeros(2,3)
print(f'y:{y}')
# 初始化，权重和偏置
w = torch.randn(5,3,requires_grad=True)  # x@w+b
print(f'w:{w}')
b = torch.randn(3,requires_grad=True)
print(f'b:{b}')
z = x@w+b
print(f'z:{z}')

# 定义损失函数
criterion = torch.nn.MSELoss()
loss = criterion(z,y) # 损失
print(f'loss:{loss}')
# 自动微分，更新权重
loss.backward()
# 打印更新w,b的梯度
print(f'w的梯度：{w.grad}')
print(f'b的梯度：{b.grad}')
w.data = w.data - 0.01 * w.grad
b.data = b.data - 0.01 * b.grad
print(f'w:{w}')
print(f'b:{b}')
