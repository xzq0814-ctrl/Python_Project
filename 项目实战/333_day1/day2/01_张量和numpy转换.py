"""
涉及的API：
    张量-> numpy nd数组对象
        张量对象.numpy()        共享内存
        张量对象.numpy.copy()   不共享内存
    numpy nd数组 -> 张量
        from_numpy()            共享内存
        torch.tensor(nd数组)     不共享内存
    从标量张量中提取内容
        标量张量.item()
"""
import numpy as np
import torch


# 张量 -> numpy
def dm01():
    t1 = torch.tensor([1,2,3,4,6])
    print(f't1:{t1}, type:{type(t1)}')
    # n1 = t1.numpy()
    n1 = t1.numpy().copy() # 不共享
    print(f'n1:{n1}, type:{type(n1)}')
    # 共享内存
    n1[0] = 100
    print(f'n1:{n1}')
    print(f't1:{t1}')



# numpy -> 张量
def dm02():
    n1 = np.array([11,22,33])
    print(f'n1:{n1}, type:{type(n1)}')

    # t1 = torch.from_numpy(n1)  # 默认是int64,共享内存
    t1 = torch.from_numpy(n1).type(torch.float) # 不共享
    print(f't1:{t1}, type:{type(t1)}')
    t2 = torch.tensor(n1)         # 默认是int64，不共享
    print(f't2:{t2}, type:{type(t2)}')
    # 测试
    n1[0] = 123
    print(f'n1:{n1}')
    print(f't1:{t1}')
    print(f't2:{t2}')
# 提取标量内容
def dm03():
    # t1 = torch.tensor(100)
    t1 = torch.tensor([180, ])  # 只能有一个值
    print(f't1:{t1}, type:{type(t1)}')
    val = t1.item()
    print(f'val:{val}, type:{type(val)}')
if __name__ == '__main__':
    dm01()
    dm02()
    dm03()