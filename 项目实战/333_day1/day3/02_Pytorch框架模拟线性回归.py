"""
numpy对象 ->张量Tensor ->数据集对象TensorDataset->数据加载器DataLoader
人工智能 = 数据+算法+算力
数据决定模型的上限
"""
#导入相关模块
import torch
from torch.utils.data import TensorDataset, dataloader  # 构造数据集对象
from torch.utils.data import DataLoader      # 数据加载器
from torch import nn     # nn模块中有平方损失函数和假设函数
from torch import optim  # optim模块中有优化器函数
from sklearn.datasets import make_regression # 创建线性回归模型数据集
import matplotlib.pyplot as plt              # 可视化
plt.rcParams['font.sans-serif']=['SimHei']  #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False    #用来正常显示负号
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# 1. 创建线性回归样本数据
def create_dataset():
    # 创建数据集对象
    x,y,coef = make_regression(
        n_samples=100,         # 100个样本
        n_features=1,          # 1个特征
        noise=10,              # 噪声，越大，样本点越散
        coef=True,             # 是否返回系数 默认False，返回None
        bias = 14.5,           # 偏置
        random_state=3,        # 随机种子  种子相同输出数据相同
    )
    # 封装成张量对象
    x = torch.tensor(x,dtype=torch.float)
    y = torch.tensor(y,dtype=torch.float)
    return x,y,coef
# 表示模型训练
def train(x,y,coef):
    # 1.创建数据集对象,Tensor -> 数据集对象 -> 数据加载器
    dataset = TensorDataset(x,y)
    # 2.创建数据加载器对象
    # 参数： 数据集对象， 批次大小， 是否打乱数据   (训练集打乱，测试集不打乱)
    data_loader = DataLoader(dataset,batch_size=16,shuffle=True)
    # 3.创建初始的线性回归模型 , 参数：输入特征维度，输出特征维度
    model = nn.Linear(1,1).to(device)
    # 4.创建损失函数对象
    criterion = nn.MSELoss()
    # 5.创建优化器对象
    optimizer = optim.SGD(model.parameters(),lr = 0.01)
    # 6.具体的训练过程
    # 定义变量：训练轮数，每轮平均损失值，训练总损失值，训练样本数
    epochs, loss_list, total_loss, total_sample = 100,[],0.0,0
    for epoch in range(epochs):
        # 每轮分批次训练，从加载器中获取批次数据
        for train_x, train_y in data_loader:  # 7批（16，16，16，16，16，16，4）
            # 模型预测
            y_pre = model(train_x)
            # 计算每批的平均损失
            loss = criterion(y_pre, train_y.reshape(-1,1))  # -1，1  n行1列
            # 计算总损失和样本批次数
            total_loss += loss.item()
            total_sample += 1
            # 梯度清零+反向传播(算梯度)+梯度更新
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        # 把本轮平均损失添加到列表中
        loss_list.append(total_loss/total_sample)
        print(f'轮数：{epoch+1},平均损失值：{total_loss/total_sample}')
    # 打印最终的训练结果
    print(f'{epochs}轮的平均损失分别为{loss_list}')
    print(f'模型参数，权重{model.weight},偏置{model.bias}')
    # 绘制损失曲线         100轮，  每轮平均损失
    plt.figure(1)
    plt.plot(range(epochs),loss_list)
    plt.title('损失曲线变化图')
    plt.grid()
    plt.show(block=False)
    # 预测值与真实值的关系
    # 绘制样本点分布情况
    plt.figure(2)
    plt.scatter(x,y)
    # 绘制训练模型的预测值
    y_pre = torch.tensor(data = [v*model.weight.detach()+model.bias.detach() for v in x])
    # 计算真实值
    y_true = torch.tensor(data=[v*coef+14.5 for v in x])
    # 绘制预测值和真实值折线图
    plt.plot(x,y_pre,color='red',label='预测值')
    plt.plot(x,y_true,color='green',label='真实值')
    # 图例，网格
    plt.legend()
    plt.grid()
    plt.show()
if __name__ == '__main__':
    # 创建数据集
    x,y,coef = create_dataset()
    # print(f'x:{x},y:{y},coef:{coef}')
    # 模型训练
    train(x,y,coef)
