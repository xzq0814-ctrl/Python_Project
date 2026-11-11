"""
自动微分模块，循环实现计算梯度，更新参数
需求：求y=X**2+20 的极小值点并打印y是最小值时w的值(梯度)

解题步骤:
1.定义点 x=10 requires_grad=True dtype=torch.float32
2.定义函数y=X**2+20
3.利用梯度下降法 循环迭代100 求最优解
3.1 正向计算(前向传播)  ?????
3.2 梯度清零x.grad.zero_()
3.3 反向传播
3.4 梯度更新x.data =x.data -0.01 * x.grad
"""
import torch
w = torch.tensor(10, requires_grad=True,dtype=torch.float)
loss = w**2+20
print(f'权重初始值：{w},(0.01 * w.grad):无, loss:{loss}')
for i in range(0,100):
    # 正向计算
    loss = w ** 2 + 20
    if w.grad is not None:  # 第一次没有计算梯度，w.grad=None,要做非空判断
        w.grad.zero_()
    # 反向传播，此时才有梯度
    loss.sum().backward()
    # print(f'梯度值为：{w.grad}')
    w.data = w.data - 0.01 * w.grad
    print(f'第{i+1}次，权重初始值{w},学习率*梯度{0.01*w.grad:.4f}，loss:{loss:.4f}')
print(f'权重：{w},梯度：{w.grad:.4f},loss:{loss:.4f}')
