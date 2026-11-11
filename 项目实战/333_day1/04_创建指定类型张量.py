"""
data.type(torch.DoubleTensor)
    type(torch支持的数据类型)
data.half/double/float/short/int/long
"""
import torch

t1 = torch.tensor([1,2,3,4,6], dtype=torch.float)
print(f't1:{t1},（元素）类型:{t1.dtype},(张量)类型：{type(t1)}')
print('-' * 30)
# 创建张量后-> 做类型转换
    # type() 函数
t2 = t1.type(torch.int16)
print(f't2:{t2},（元素）类型:{t2.dtype},(张量)类型：{type(t2)}')
print('-' * 30)
    # half......
print(t2.half())        # float16
print(t2.float())       # float32 默认
print(t2.double())      # float64
print(t2.short())       # int16
print(t2.int())         # int32
print(t2.long())        # int64 默认



