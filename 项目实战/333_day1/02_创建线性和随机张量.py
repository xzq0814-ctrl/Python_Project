"""
torch.arange() 和 torch.linspace() 创建线性张量
torch.random.initial_seed()和 torch.random.manual_seed() 随机种子设置
torch.rand/randn() 创建随机浮点类型张量
torch.randint(low,high,size=()) 创建随机整数类型张量

"""
import torch
# 1. 定义函数，创建线性张量
def demo01():
    # 参数：起始值，结束值，步长
    t1 = torch.arange(0, 10, 2)
    print(f't1:{t1},type:{type(t1)}')
    print('-' * 30)
    # 指定范围的 线性张量 -> 等差数列
    # 参数：起始值，结束值，元素个数
    t2 = torch.linspace(1, 10, 4)
    print(f't2:{t2},type:{type(t2)}')
# 2. 定义函数，创建随机张量
def demo02():
    # todo: 1. 设置随机种子
    # torch.initial_seed() # 采用当前系统时间戳作为随机种子
    torch.manual_seed(3)   # 设置随机种子
    # todo: 2. 创建随机张量,均匀分布的（0，1）随机张量
    t1 = torch.rand(size=(2, 3))
    print(f't1:{t1},type:{type(t1)}')
    print('-' * 30)
    # 符合正态分布的随机张量
    t2 = torch.randn(size=(2, 3))
    print(f't2:{t2},type:{type(t2)}')
    print('-' * 30)
    # 创建指定范围的随机整数张量
    t3 = torch.randint(1, 10, size=(3, 5))
    print(f't3:{t3},type:{type(t3)}')

# 3. 测试函数
if __name__ == '__main__':
    demo01()
    demo02()

