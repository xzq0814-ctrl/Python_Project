from matplotlib import pyplot as plt
import torch
plt.rcParams['font.sans-serif']=['SimHei']  #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False    #用来正常显示负号
# 创建画布和坐标轴 1行2列
fig, axes = plt.subplots(1, 2)#函数图像
# 生成数据点
x = torch.linspace(-20, 20, 1000)
# 计算1000个点，tanh处理后的值
y = torch.tanh(x)
# 在一个子图中绘制tanh激活函数的图像
axes[0].plot(x, y)
axes[0].grid()
axes[0].set_title('Tanh函数图像')
#导数图像
x = torch.linspace(-20, 20, 1000, requires_grad=True)
torch.tanh(x).sum().backward()
axes [1].plot(x.detach(), x.grad)
axes[1].grid()
axes[1].set_title('Tanh导数图像')
plt.show()