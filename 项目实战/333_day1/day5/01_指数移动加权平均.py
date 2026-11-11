"""
演示30天的天气分布情况
针对于β（调节权重系数）来讲，其值越大说明：越依赖指数加权平均，越不依赖本次的梯度值，数据就越：平缓。
"""
import torch
import matplotlib.pyplot as plt


ElEMENT_number = 30
def dm_wea01():
    torch.manual_seed(0)
    temperature = torch.randn(size=[ElEMENT_number,]) * 10
    print(temperature)
    # 绘制平均温度
    days = torch.arange(1, ElEMENT_number + 1, 1)
    plt.plot(days, temperature,color='r')
    plt.scatter(days, temperature)
    plt.show()

def dm_wea02(beta=0.9):
    torch.manual_seed(0)
    temperature = torch.randn(size=[ElEMENT_number,]) * 10
    print(temperature)

    exp_weight_avg=[]
    for idx, temp in enumerate(temperature,1):
        if idx ==1:
            exp_weight_avg.append(temp)
            continue
        new_temp = exp_weight_avg[idx-2] * beta +(1 - beta) * temp

        exp_weight_avg.append(new_temp)
    days = torch.arange(1, ElEMENT_number + 1, 1)
    plt.plot(days, exp_weight_avg,color='r')
    plt.scatter(days, temperature)
    plt.show()

if __name__ == '__main__':
    dm_wea01()
    dm_wea02(0.5)
    dm_wea02(0.9)