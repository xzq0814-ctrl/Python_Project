"""
torch.cat()函数可以将多个张量根据指定的维度拼接起来，不改变维度数。
            拼接的维度数必须保持一致
torch.stack()函数会在一个新的维度上连接一系列张量，这会增加一个新维度
            所有的维度都必须保持一致
"""
import torch

# 创建两个张量
t1 =torch.randint(1,10,size=(2,3))
print(f't1={t1},shape={t1.shape}')
t2 = torch.randint(1,10,size=(2,3))
print(f't2={t2},shape={t2.shape}')

# 演示拼接 cat()函数
t3 = torch.cat((t1,t2),dim=0)  # 列(2,3)+(2,3)=(4,3)
print(f't3={t3},shape={t3.shape}')
t4 = torch.cat((t1,t2),dim=1)  # 行(2,3)+(2,3)=(2,6) ,dim = -1效果相同
print(f't4={t4},shape={t4.shape}')

print('-'*30)

# stack（）拼接张量，可以新增新维度,不能有未知维度
t7 = torch.stack((t1,t2),dim=0) # (2,3)+(2,3)=(2*,2,3)
print(f't7={t7},shape={t7.shape}')

t8 = torch.stack((t1,t2),dim=1) # (2,3)+(2,3)=(2,2*,3)
print(f't8={t8},shape={t8.shape}')

t9 = torch.stack((t1,t2),dim=2) # (2,3)+(2,3)=(2,3,2*)
print(f't9={t9},shape={t9.shape}')
