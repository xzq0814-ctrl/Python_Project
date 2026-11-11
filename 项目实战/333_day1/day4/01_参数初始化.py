"""
演示参数初始化的7种方式。
参数初始化的目的：
    1.防止梯度消失或者梯度爆炸。
    2.提高收敛速度。
    3.打破对称性。
参数初始化的方式：
    无法打破对称性的：
        全0，全1，固定值
    可以打破对称性的：
        随机初始化，正态分布初始化，kaiming初始化，Xavier初始化
关于初始化的选择上：
    激活函数ReLU及其系列：优先用kaiming
    激活函数非ReLU：优先用xavier
    如果是浅层网络：可以考虑使用随机初始化
"""
import torch.nn as nn    # 神经网络
#1.均匀分布随机初始化
def dm01():
    # 创建一个线性层，输入维度5，输出维度3
    linear = nn.Linear(5,3)
    # 对权重w,偏置b进行随机初始化，0-1均匀分布产生参数
    nn.init.uniform_(linear.weight)
    nn.init.uniform_(linear.bias)
    print(linear.weight.data)
    print(linear.bias.data)
# 2.固定初始化
def dm02():
    linear = nn.Linear(5,3)
    nn.init.constant_(linear.weight, 3) # 设置固定值为3
    nn.init.constant_(linear.bias, 3)
    print(linear.weight.data)
    print(linear.bias.data)
# 3.全0初始化
def dm03():
    linear = nn.Linear(5,3)
    nn.init.zeros_(linear.weight)  # 全0初始化
    nn.init.zeros_(linear.bias)
    print(linear.weight.data)
    print(linear.bias.data)
# 4.全1初始化  ones_
# 5.正态分布随机初始化
def dm05():
    linear = nn.Linear(5,3)
    # 对权重w,进行随机初始化，正态分布初始化（均值为0，标准差为1）
    nn.init.normal_(linear.weight)
    print(linear.weight.data)
# 6. kaiming初始化
def dm06():
    linear = nn.Linear(5,3)
    # kaiming正态分布初始化
    nn.init.kaiming_normal_(linear.weight)
    # kaiming均匀分布初始化
    # nn.init.kaiming_uniform_(linear.weight)
    print(linear.weight.data)
# 7. xavier 初始化

# 测试
if __name__ == '__main__':
    # dm01()
    # dm02()
    # dm03()
    # dm05()
    dm06()











