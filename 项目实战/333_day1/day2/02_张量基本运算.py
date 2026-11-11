"""
涉及的API
加减乘除取负号:
add(), sub()、 mul(), div()、 neg()
add_、sub_、mul_、div_、neg_(其中带下划线的版本会修改原数据) inplace = True
"""
import torch
t1 = torch.tensor([1, 2, 3])
# t2 = t1.add(10)
t2 = t1 + 10      # 效果相同
# t1.add_(10)
t1 += 10          # 改变原数据

t3 = t1.sub(1)
t4 = t1.mul(2)
t5 = t1.div(2)
t6 = t1.neg()
print(f't1:{t1}')
print(f't2:{t2}')
print(f't3:{t3}')
print(f't4:{t4}')
print(f't5:{t5}')
print(f't6:{t6}')


