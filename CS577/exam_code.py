#需要一个函数计算CNN的卷积核
#卷积核的大小为5*5，输入的通道为1，输出的通道为32
#使用torch.nn.Conv2d()函数
import time

import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils as utils
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np


#矩阵计算
def matrix_calculate():
    matrix_a = torch.tensor([[1, -2], [-1, 1]])
    matrix_b = torch.tensor([1, -1])
    matrix_c = torch.tensor([1, 0])
    res=matrix_a.matmul(matrix_b)+matrix_c
    res=sigmoid(res)
    print(res)
#sigmoid函数
def sigmoid(x):
    return 1/(1+np.exp(-x))
#CNN计算卷积核shape等
def clac_conv():
    #定义一个卷积核
    conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=(9,9), stride=1, padding=0)
    #定义一个输入
    input = torch.randn(1, 3, 128, 128)#batch_size,channel,height,width
    #计算卷积核
    output = conv1(input)
    print('卷积核1',output.shape)
    print('参数数量',  sum(p.numel() for p in conv1.parameters()))
    maxpooling = nn.MaxPool2d(kernel_size=(2,2), stride=2, padding=0)
    output = maxpooling(output)
    print('参数数量', sum(p.numel() for p in conv1.parameters()))
    print('maxpooling',output.shape)
    conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=(5,5), stride=1, padding=0)
    output = conv2(output)
    print('卷积核2',output.shape)
    print('参数数量', sum(p.numel() for p in conv2.parameters()))
    output = maxpooling(output)
    print('参数数量', sum(p.numel() for p in conv2.parameters()))
    print('maxpooling', output.shape)
    conv3 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(5,5), stride=1, padding=0)
    output = conv3(output)
    print('卷积核3',output.shape)
    print('参数数量', sum(p.numel() for p in conv3.parameters()))

    output = maxpooling(output)
    print('参数数量', sum(p.numel() for p in conv3.parameters()))
    print('maxpooling',output.shape)
    #按3个neuron进行全连接
    output = output.view(output.size(0), -1)
    fc1 = nn.Linear(64*12*12,3)
    output = fc1(output)
    print('全连接',output.shape)
    print('参数数量', sum(p.numel() for p in fc1.parameters()))

def clac_conv_simpe():
    #计算简单的卷积值
    # 定义 输入 input
    input = torch.tensor([[[[1.0, 2.0,3.0]
                             , [4.0,5.0, 6.0]
                             , [7.0, 8.0, 9.0]]]])
    # 定义 卷积核 kernel
    kernel = torch.tensor([[[[1.0, 1.0],[1.0,1.0]]]])
    # 定义 卷积层 conv
    conv = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=(2,2), stride=1, padding=0)
    # 计算卷积值
    conv.weight.data = kernel
    output = conv(input)
    output = torch.round(output)

    print(output)
if __name__ == '__main__':
    clac_conv_simpe()
