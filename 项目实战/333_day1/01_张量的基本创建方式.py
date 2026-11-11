"""
张量：pytorch框架属于最常用的深度学习框架
    底层在处理数据时，都是用 张量 来处理的
    张量 -> 存储同一类型元素的容器，且元素是数值
创建方式：
    torch.tensor 根据指定数据创建张量
    torch.Tensor 根据形状创建张量，也可以用指定数据
    torch.IntTensor、torch.FloatTensor、torch.DoubleTensor 创建指定类型的张量

"""
import torch
import numpy as np
# 定义函数 torch.tensor 根据指定数据创建张量
def dm01():
    # 标量 张量
    t1 = torch.tensor(10)
    print(f't1:{t1},type:{type(t1)}')
    print('-' * 30)
    # 二维列表-> 张量
    data = [[1,2,3],[4,5,6]]
    t2 = torch.tensor(data)
    print(f't2:{t2},type:{type(t2)}')
    print('-' * 30)
    # numpy nd数组->张量
    data = np.random.randint(0,10,size=(2,3))
    t3 = torch.tensor(data, dtype=torch.float)
    print(f't3:{t3},type:{type(t3)}')
    print('-' * 30)
# 定义函数 torch.Tensor ...
def dm02():
    # 标量 张量
    t1 = torch.Tensor(10)
    print(f't1:{t1},type:{type(t1)}')
    print('-' * 30)
    # 二维列表-> 张量
    data = [[1,2,3],[4,5,6]]
    t2 = torch.Tensor(data)
    print(f't2:{t2},type:{type(t2)}')
    print('-' * 30)
    # numpy nd数组->张量
    data = np.random.randint(0,10,size=(2,3))
    t3 = torch.Tensor(data)
    print(f't3:{t3},type:{type(t3)}')
    print('-' * 30)
    t4 = torch.Tensor(2,3)
    print(f't4:{t4},type:{type(t4)}')
# 定义函数
def dm03():
    # 标量 张量
    t1 = torch.IntTensor(10)
    print(f't1:{t1},type:{type(t1)}')
    print('-' * 30)
    # 二维列表-> 张量
    data = [[1, 2, 3], [4, 5, 6]]
    t2 = torch.IntTensor(data)
    print(f't2:{t2},type:{type(t2)}')
    print('-' * 30)
    # numpy nd数组->张量
    data = np.random.randint(0, 10, size=(2, 3))
    t3 = torch.IntTensor(data)
    print(f't3:{t3},type:{type(t3)}')
    print('-' * 30)
    data = np.random.randint(0, 10, size=(2, 3))
    t4 = torch.FloatTensor(data)   # 默认类型为float32
    print(f't4:{t4},type:{type(t4)}')
    print('-' * 30)
#  测试函数
if __name__ == '__main__':
    # dm01()
    dm02()
    # dm03()

