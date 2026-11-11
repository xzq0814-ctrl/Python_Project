"""
公式:
W新=W旧-学习率*（本次的)梯度
存在的问题：
1.遇到平缓区域，梯度下降（权重更新)可能会慢。
2.可能会遇到鞍点(梯度为0)
3.可能会遇到局部最小值。
解决思路：
从上述的学习率或者梯度入手，进行优化，于是有了：动量法Momentum，自适应学习率AdaGrad，RMSProp，综合衡量：Adam
动量法Momentum:
    动量法公式：
    St = β * St-1 + (1 - β) * Gt
    St:    本次的指数移动加权平均结果。
    β:     调节权重系数，越大，数据越平缓，历史指数移动加权平均比重越大，本次梯度权重越小。
    St-1:  历史的指数移动加权平均结果。
    Gt:    本次计算出的梯度（不考虑历史梯度）.
    加入动量法后的梯度更新公式：
        W新=WI旧 -学习率*St
    自适应学习率：AdaGrad
        公式：
            累计平方梯度：St = St-1 + Gt * Gt
        st:累计平方梯度
        St-1:历史累计平方梯度。
        Gt:本次的梯度。
        学习率 = 学习率 /(sqrt(St）+小常数)
        小常数：1e-10，目的：防止分母变为0
        梯度下降公式：W新=W旧-调整后的学习率*Gt
        缺点：可能会导致学习率过早，过量的降低，导致模型后期学习率太小，较难找到最优解
    自适应学习率：RMSProp -> 对AdaGrad的优化 加入调和权重系数
        指数加权平均累计历史平方梯度： St = β * St-1 + (1 - β) * Gt * Gt
    自适应矩估计：Adam  既优化学习率，又优化梯度。
        公式:
            一阶矩：算均值。Mt = β1 * Mt-1 + (1 - β1) * Gt  充当：梯度
                        St = β2 * St-1 + (1 - β2) * Gt * Gt  充当：学习率
            二阶矩：梯度的方差。
                Mt^ = Mt / (1 - β1 ^ t)
                St^ = St / (1 - β2 ^ t)
            权重更新公式：  W新=W旧 - 学习率/(sqrt(St^）+小常数) * Mt^
"""
import torch
import torch.nn as nn
import torch.optim as optim

# 动量法
def dm01_momentum():
    # 初始化权重参数
    w = torch.tensor([1.0],requires_grad=True,dtype = torch.float)
    criterion = ((w ** 2)/2.0)  # 定义损失函数
    # 3.创建优化器（函数对象）→基于SGD（随机梯度下降），加入参数momentum，就是动量法。
    # 参1：（待优化的)参数列表，参2：学习率，参3：动量参数。
    optimizer = optim.SGD(params=[w], lr = 0.01, momentum = 0.9)  # momentum = 0 为默认值，只考虑本次梯度
    # 计算梯度值： 梯度清零+反向传播+参数更新
    optimizer.zero_grad()
    criterion.sum().backward()
    optimizer.step()
    print(f'w:{w},w.grad:{w.grad}')

    # 重复步骤  更新权重
    criterion = ((w ** 2) / 2.0)
    optimizer.zero_grad()
    criterion.sum().backward()
    optimizer.step()
    print(f'w:{w},w.grad:{w.grad}')

# 自适应学习率
def dm02_ada_grad():
    w = torch.tensor([1.0],requires_grad=True,dtype = torch.float)
    criterion = ((w ** 2) / 2.0)
    # 参1：（待优化的)参数列表，参2：学习率
    optimizer = optim.Adagrad(params=[w], lr=0.01)
    # 计算梯度值： 梯度清零+反向传播+参数更新
    optimizer.zero_grad()
    criterion.sum().backward()
    optimizer.step()
    print(f'w:{w},w.grad:{w.grad}')

    # 重复步骤  更新权重
    criterion = ((w ** 2) / 2.0)
    optimizer.zero_grad()
    criterion.sum().backward()
    optimizer.step()
    print(f'w:{w},w.grad:{w.grad}')

def dm03_rms_prop():
    w = torch.tensor([1.0],requires_grad=True,dtype = torch.float)
    criterion = ((w ** 2) / 2.0)
    # 参1：（待优化的)参数列表，参2：学习率
    optimizer = optim.RMSprop(params=[w], lr=0.01)
    # 计算梯度值： 梯度清零+反向传播+参数更新
    optimizer.zero_grad()
    criterion.sum().backward()
    optimizer.step()
    print(f'w:{w},w.grad:{w.grad}')

    # 重复步骤  更新权重
    criterion = ((w ** 2) / 2.0)
    optimizer.zero_grad()
    criterion.sum().backward()
    optimizer.step()
    print(f'w:{w},w.grad:{w.grad}')

def dm04_adam():
    w = torch.tensor([1.0], requires_grad=True, dtype=torch.float)
    criterion = ((w ** 2) / 2.0)
    # 参1：（待优化的)参数列表，参2：学习率   参3：（梯度，学习率）衰减系数
    optimizer = optim.Adam(params=[w], lr=0.01, betas=(0.9, 0.999))
    # 计算梯度值： 梯度清零+反向传播+参数更新
    optimizer.zero_grad()
    criterion.sum().backward()
    optimizer.step()
    print(f'w:{w},w.grad:{w.grad}')

    # 重复步骤  更新权重
    criterion = ((w ** 2) / 2.0)
    optimizer.zero_grad()
    criterion.sum().backward()
    optimizer.step()
    print(f'w:{w},w.grad:{w.grad}')


if __name__ == '__main__':
    # dm01_momentum()
    # dm02_ada_grad()
    # dm03_rms_prop()
    dm04_adam()