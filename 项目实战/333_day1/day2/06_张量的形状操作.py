"""
reshape()函数
reshape函数可以在保证张量数据不变的前提下改变数据的维度，将其转换成指定的形状。
squeeze()和 unsqueeze()函数
Squeeze函数删除形状为1的维度(降维)，unsqueeze函数 在指定轴上添加形状为1的维度(升维)
transpose()    一次只能交换两个维度  不改变原始数据
permute()      一次可以同时交换多个维度
view()
    只能修改连续的张量的形状，连续张量=内存中存储顺序 和 在张量中显示的顺序相同
contiguous()
    把不连续的张量 -> 连续的张量，即:基于张量中显示的顺序，修改内存中的存储顺序。
is_contiguous()  判断张量是否是连续的.
"""
import torch
torch.manual_seed(24)
# 1.演示 reshape()函数
def dem01():
    t1 = torch.randint(1,10,size=(2,3))
    print(f"t1 = {t1}, shape: {t1.shape},row:{t1.shape[0]},col:{t1.shape[1]},{t1.shape[-1]}")
    # t1转换维度，3行两列，1行6列
    # t2 = t1.reshape(3,2)
    t2 = t1.reshape(1,6)
    print(f"t2 = {t2}, shape: {t2.shape},row:{t2.shape[0]},col:{t2.shape[1]},{t2.shape[-1]}")
    # t3 = t1.reshape(2,5)  # 报错 2*3=6  2*5=10,不一致
# 2.演示 unsqueeze函数,squeeze()函数
def dem02():
    t1 = torch.randint(1,10,size=(2,3))
    print(f't1={t1},shape={t1.shape}')
    # 0轴上添加1个维度
    t2 = t1.unsqueeze(0)
    print(f't2={t2},shape={t2.shape}')
    # 1轴上添加1个维度
    t3 = t1.unsqueeze(1)
    print(f't3={t3},shape={t3.shape}')
    # 2轴上添加1个维度
    t4 = t1.unsqueeze(2)
    print(f't4={t4},shape={t4.shape}')
    # 在3轴上（不存在）添加1个维度,报错 （2，3，??,1）
    # t5 =t1.unsqueeze(3)

    # 删除所有为1的维度
    t6 = torch.randint(1,10,size=(2,3,1,4,1,1))
    print(f't6={t6},shape={t6.shape}')
    t7 = t6.squeeze()
    print(f't7={t7},shape={t7.shape}')
# 3.演示 transpose()函数，permute()函数
def dem03():
    t1 = torch.randint(1,10,size=(2,3,4))
    print(f't1={t1},shape={t1.shape}')
    print('-'*30)
    # 改变维度-> (3,2,4)
    t2 = t1.transpose(0, 1)
    print(f't2={t2},shape={t2.shape}')
    t3 = t1.transpose(0,2)
    # t3 = t1.transpose(0,-1)  # 效果同上
    print(f't3={t3},shape={t3.shape}')

    # 改变维度 -> (4,2,3)
    t4 = t1.permute(2,0,1)
    print(f't4={t4},shape={t4.shape}')
# 4.演示 view()函数 ,contiguous()函数,is_contiguous()函数
def dem04():
    t1 = torch.randint(1,10,size=(2,3))
    print(f't1={t1},shape={t1.shape}')
    # 判断张量是否连续
    print(t1.is_contiguous())
    # 修改形状
    t2 = t1.view(3,2)
    print(f't2={t2},shape={t2.shape}')
    print(t2.is_contiguous())
    # 通过transpose() 交换维度
    t3 = t1.transpose(0,1)
    print(f't3={t3},shape={t3.shape}')
    print(t3.is_contiguous())
    # 把 t3张量从（3，2），通过view 转成（2，3）
    t4 = t3.contiguous().view(2,3)  # 把t3变成连续张量
    print(f't4={t4},shape={t4.shape}')
# 5. 测试
if __name__ == '__main__':
    # dem01()
    # dem02()
    # dem03()
    dem04()