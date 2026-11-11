"""
torch.ones 和 torch.ones_like 创建全1张量
torch.zeros 和 torch.zeros_like 创建全0张量
torch.full和 torch.full_like 创建全为指定值张量
"""
import torch

# 一：创建全1张量
t1 = torch.ones(2, 3)
print(f't1:{t1},type:{type(t1)}')
print('-' * 30)
t2 = torch.tensor([[1,2],[3,4],[5,6]])
    # t3基于t2形状创建全1
t3 = torch.ones_like(t2)
print(f't3:{t3},type:{type(t3)}')
print('*' * 30)
# 二：创建全0张量
t1 = torch.zeros(2, 3)
print(f't1:{t1},type:{type(t1)}')
print('-' * 30)
t2 = torch.tensor([[1,2],[3,4],[5,6]])
    # t3基于t2形状创建全0
t3 = torch.zeros_like(t2)
print(f't3:{t3},type:{type(t3)}')
print('*' * 30)
# 三：创建全为指定值张量
t1 = torch.full(size=(2, 3), fill_value=255) # 二行三列 255张量
print(f't1:{t1},type:{type(t1)}')
print('-' * 30)
t2 = torch.tensor([[1,2],[3,4],[5,6]])
    # t3基于t2形状创建全0
t3 = torch.full_like(t2,255)
print(f't3:{t3},type:{type(t3)}')
print('*' * 30)