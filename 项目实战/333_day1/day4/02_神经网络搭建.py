"""
深度学习案例的4个步骤：
    1.准备数据。
    2.搭建神经网络
    3.模型训练
    4.模型测试
神经网络搭建流程：
    1.定义一个类，继承：nn.Module
    2.在__init__()方法中，搭建神经网络。
    3.在forward()方法中，完成：前向传播。
"""
import torch
import torch.nn as nn
from torchsummary import summary # 计算模型参数，查看模型结构

# todo:1.搭建神经网络，自定义继承 nn.Module
class ModelDemo(nn.Module):
    # 在init魔法方法中完成初始化：父类成员 和 神经网络搭建
    def __init__(self):
        super().__init__()
        # 隐藏层
        self.linear1 = nn.Linear(in_features=3, out_features=3)
        self.linear2 = nn.Linear(in_features=3, out_features=2)
        # 输出层
        self.output = nn.Linear(in_features=2, out_features=2)
        # 隐藏层参数初始化
        nn.init.xavier_normal_(self.linear1.weight)
        nn.init.zeros_(self.linear1.bias)
        nn.init.kaiming_normal_(self.linear2.weight)
        nn.init.zeros_(self.linear2.bias)
    # 前向传播 输入层（矩阵x）->隐藏层->输出层
    def forward(self, x):
        # 隐藏层一计算：加权求和 + 激活函数
        # x = self.linear1(x)
        # x = torch.sigmoid(x)
        x = torch.sigmoid(self.linear1(x))
        x = torch.relu(self.linear2(x))
        # dim=-1 按行计算
        x = torch.softmax(self.output(x), dim=-1)
        # 返回预测值
        return x


# todo:2.模型训练测试
def train():
    # 创建模型对象
    my_model = ModelDemo()
    # 创建数据集样本，随机生成
    data = torch.randn(size=(5, 3))
    # 调用神经网络模型->进行模型训练
    output = my_model(data)   # 底层自动调用forward方法，进行前向传播
    print(f'output: {output}')
    print(f'output.shape: {output.shape}')
    print(f'output.requires_grad: {output.requires_grad}')
    # 计算和查看模型参数
    print('============计算模型参数=============')
    summary(my_model, (5, 3))
    print('=============查看模型参数============')
    for name, param in my_model.named_parameters():
        print(f'name: {name}')
        print(f'param: {param}')
if __name__ == '__main__':
    train()
