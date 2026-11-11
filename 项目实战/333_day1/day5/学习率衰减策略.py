"""
学习率衰减策略介绍：
较之于AdaGrad，RMSProp，Adam方式，我们可以通过等间隔，指定间隔，指数等方式，来手动控制学习率的调整。
    分类：等间隔学习率衰减
         指定间隔学习率衰减
         指数学习率衰减
等间隔学习率衰减：
    step_size： 间隔的轮数，即：多少轮调整一次学习率。
    gamma:     学习率衰减系数，即：lr新=lr旧*gamma
指定间隔学习率衰减：
    milestones = [50, 125, 160]
    gamma:  学习率衰减系数， lr新 = lr旧 * gamma
指数间隔学习率衰减：
    前期学习率衰减快，中期慢，后期更慢，符合梯度下降规律
    公式:Lr新= lrl旧* gamma ** epoch
"""
import torch
from torch import optim
import matplotlib.pyplot as plt
# 分类一:
def lear_rat01():
    # 1.定义变量，记录初始学习率，训练轮数，每轮批次数
    lr,epochs,iteration = 0.1,200,10
    # 2.创建数据集. y_true, x, w
    y_true = torch.tensor([0])
    x = torch.tensor([1.0], dtype=torch.float32)
    w = torch.tensor([1.0],requires_grad=True,dtype=torch.float32)
    # 3.创建优化器对象， 动量法-> 加速模型收敛减小震荡
    optimizer = optim.SGD([w],lr=lr,momentum=0.9)
    # todo:4.创建 等间隔 学习率衰减对象**
    scheduler = optim.lr_scheduler.StepLR(optimizer,step_size = 50, gamma=0.5)
    # 5.创建俩列表，分别表示训练轮数和训练用的学习率
    lr_list,epoch_list=[],[]
    # 6.循环遍历训练轮数
    for epoch in range(epochs):
        # 7.获取当前学习率和轮数，保存到列表中
        epoch_list.append(epoch+1)
        lr_list.append(scheduler.get_last_lr()) # 获取最后的学习率
        # 8. 循环遍历，每轮每批次进行训练
        for batch in range(iteration):
            # 计算预测值，基于损失函数计算损失
            y_pre = w * x
            # 计算损失，最小二乘法
            loss = (y_pre - y_true) ** 2
            # 梯度清零+反向传播+更新参数
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        # 更新学习率
        scheduler.step()
    # 13.打印结果
    print(f'lr_list:{lr_list}')
    # 14.可视化
    plt.plot(epoch_list,lr_list)
    plt.xlabel('epoch')
    plt.ylabel('learning rate')
    plt.legend(['Step LR Scheduler'])
    plt.show()

# 分类二：
def lear_rat02():
    # 1.定义变量，记录初始学习率，训练轮数，每轮批次数
    lr, epochs, iteration = 0.1, 200, 10
    # 2.创建数据集. y_true, x, w
    y_true = torch.tensor([0])
    x = torch.tensor([1.0], dtype=torch.float32)
    w = torch.tensor([1.0], requires_grad=True, dtype=torch.float32)
    # 3.创建优化器对象， 动量法-> 加速模型收敛减小震荡
    optimizer = optim.SGD([w], lr=lr, momentum=0.9)
    # todo:4.创建 指定间隔 学习率衰减对象**
    # 定义变量 手动记录要修改学习率的轮数
    milestones = [50, 125, 160]
    scheduler = optim.lr_scheduler.MultiStepLR(optimizer, milestones=milestones, gamma=0.5)
    # 5.创建俩列表，分别表示训练轮数和训练用的学习率
    lr_list, epoch_list = [], []
    # 6.循环遍历训练轮数
    for epoch in range(epochs):
        # 7.获取当前学习率和轮数，保存到列表中
        epoch_list.append(epoch + 1)
        lr_list.append(scheduler.get_last_lr())  # 获取最后的学习率
        # 8. 循环遍历，每轮每批次进行训练
        for batch in range(iteration):
            # 计算预测值，基于损失函数计算损失
            y_pre = w * x
            # 计算损失，最小二乘法
            loss = (y_pre - y_true) ** 2
            # 梯度清零+反向传播+更新参数
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        # 更新学习率
        scheduler.step()
    # 13.打印结果
    print(f'lr_list:{lr_list}')
    # 14.可视化
    plt.plot(epoch_list, lr_list)
    plt.xlabel('epoch')
    plt.ylabel('learning rate')
    plt.legend(['MultiStepLR Scheduler'])
    plt.show()

# 分类三：
def lear_rat03():
    # 1.定义变量，记录初始学习率，训练轮数，每轮批次数
    lr, epochs, iteration = 0.1, 200, 10
    # 2.创建数据集. y_true, x, w
    y_true = torch.tensor([0])
    x = torch.tensor([1.0], dtype=torch.float32)
    w = torch.tensor([1.0], requires_grad=True, dtype=torch.float32)
    # 3.创建优化器对象， 动量法-> 加速模型收敛减小震荡
    optimizer = optim.SGD([w], lr=lr, momentum=0.9)
    # todo:4.创建 指数 学习率衰减对象**
    scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.95)
    # 5.创建俩列表，分别表示训练轮数和训练用的学习率
    lr_list, epoch_list = [], []
    # 6.循环遍历训练轮数
    for epoch in range(epochs):
        # 7.获取当前学习率和轮数，保存到列表中
        epoch_list.append(epoch + 1)
        lr_list.append(scheduler.get_last_lr())  # 获取最后的学习率
        # 8. 循环遍历，每轮每批次进行训练
        for batch in range(iteration):
            # 计算预测值，基于损失函数计算损失
            y_pre = w * x
            # 计算损失，最小二乘法
            loss = (y_pre - y_true) ** 2
            # 梯度清零+反向传播+更新参数
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        # 更新学习率
        scheduler.step()
    # 13.打印结果
    print(f'lr_list:{lr_list}')
    # 14.可视化
    plt.plot(epoch_list, lr_list)
    plt.xlabel('epoch')
    plt.ylabel('learning rate')
    plt.legend(['ExponentialLR Scheduler'])
    plt.show()

if __name__ == '__main__':
    # lear_rat01()
    # lear_rat02()
    lear_rat03()