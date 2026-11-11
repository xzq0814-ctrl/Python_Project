"""
图像分类:
二值图：1通道，每个像素点由0，1组成
灰度图：1通道，每个像素点的范围：[0，255]
索引图：1通道，每个像素点的范围：[0，255]，像素点表示颜色表的索引
RGB真彩图：3通道，Red，Green，Blue，红绿蓝。
"""
import numpy as np
import matplotlib.pyplot as plt
import torch

def pic01():
    # 1.定义全黑图片：像素点越接近0越黑，越接近255越白。
    # HWC: 高度 宽度 通道
    img1 = np.zeros((200,200,3))
    # 绘图
    plt.imshow(img1)
    plt.axis('off')
    plt.show()
    # 全白图片
    img2 = torch.full(size=(200,200,3),fill_value=255)
    plt.imshow(img2)
    plt.show()
def pic02():
    pass

if __name__ == '__main__':
    pic02()

