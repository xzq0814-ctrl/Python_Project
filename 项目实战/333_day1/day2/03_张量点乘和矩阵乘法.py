"""
点乘：两个张量维度一致，对应元素做相应的运算
    API:
    t1 * t2
    t1.mul(t2)  #multiply:乘法
矩阵乘法:两个张量，第一个张量的列数，等于第二个张量的行数(A列=B行)
结果:A行B列
API:
t1 @ t2
t1.matmul(t2)
t1.dot(t2)
扩展:只针对于一维张量有效.
"""
import torch
def dm01():
    t1 = torch.tensor([[1, 2, 3],[4, 5, 6]])
    print(f't1:{t1}')
    t2 = torch.tensor([[1, 2, 3],[4, 5, 6]])
    print(f't2:{t2}')

    t3 = t1 * t2
    # t3 = t1.mul(t2)
    print(f't3:{t3}')
def dm02():  # 矩阵乘法
    t1 = torch.tensor([[1, 2, 3],[4, 5, 6]])
    print(f't1:{t1}')
    t2 = torch.tensor([[1, 2, 3],[4, 5, 6],[7,8,9]])
    print(f't2:{t2}')

    t3 = t1 @ t2
    # t3 = t1.matmul(t2)   # matrix multiply
    print(f't3:{t3}')

    # t3 = t1.dot(t2)        # 报错
    t4 = torch.tensor([1, 2, 3])
    t5 = torch.tensor([4, 5, 6])
    t6 = t4.dot(t5)
    print(f't6:{t6}')

if __name__ == '__main__':
    dm01()
    dm02()
