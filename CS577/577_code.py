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

def clac_conv():
    # 定义一个5×5的图
    # I = torch.tensor([[0.0, 1.0, 0.0, 0.0, 1.0],
    #                   [1.0, 0.0, 1.0, 0.0, 0.0],
    #                   [0.0, 1.0, 1.0, 0.0, 0.0],
    #                   [0.0, 0.0, 1.0, 1.0, 0.0]])
    #
    # # 定义一个3×3的卷积核
    # K = torch.tensor([[0.0,1.0,0.0],
    #                   [1.0,0.0,1.0],
    #                   [0.0,1.0,0.0]])


    I=torch.tensor([[[[1.0, 0.0, 1.0, 0.0, 1.0],
                    [0.0, 1.0, 0.0, 1.0, 0.0],
                    [1.0, 0.0, 1.0, 0.0, 1.0],
                    [0.0, 1.0, 0.0, 1.0, 0.0],
                    [1.0, 0.0, 1.0, 0.0, 1.0]],

                    [[0.0, 1.0, 2.0, 3.0, 4.0],
                     [5.0, 6.0, 7.0, 8.0, 9.0],
                     [9.0, 8.0, 7.0, 6.0, 5.0],
                     [0.0, 1.0, 2.0, 3.0, 4.0],
                     [5.0, 6.0, 7.0, 8.0, 9.0]],

                    [[3.0, 3.0, 3.0, 3.0, 3.0],
                     [3.0, 2.0, 2.0, 2.0, 3.0],
                     [3.0, 2.0, 1.0, 2.0, 3.0],
                     [3.0, 2.0, 2.0, 2.0, 3.0],
                     [3.0, 3.0, 3.0, 3.0, 3.0]]]]

    )
    K = torch.tensor([[[[-1.0, -1.0, -1.0],
                      [-1.0, -1.0, -1.0],
                      [-1.0, -1.0, -1.0]],
                       [[-1.0, -1.0, -1.0],
                        [-1.0, -1.0, -1.0],
                        [-1.0, -1.0, -1.0]],
                       [[-1.0, -1.0, -1.0],
                        [-1.0, -1.0, -1.0],
                        [-1.0, -1.0, -1.0]]
                       ]]

                        )
    print(I.shape)
    print(K.shape)
    #I = I.unsqueeze(1)
    #K = K.unsqueeze(1)
    # 定义一个卷积层
    conv = nn.Conv2d(in_channels=3,out_channels=3,kernel_size=3,stride=1,padding=0,bias=True)
    #如何设置bias为固定的1
    conv.bias.data = torch.ones(1)

    # 把卷积核赋值给卷积层
    conv.weight.data = K

    # 计算卷积结果
    Z = conv(I)

    # 打印结果
    print(Z)
def clac_padding():
    # 定义输入张量
    x = torch.tensor([[0.0, 1.0, 0.0, 0.0, 1.0],
                      [1.0, 1.0, 0.0, 1.0, 1.0],
                      [1.0, 0.0, 1.0, 0.0, 0.0],
                      [0.0, 1.0, 1.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 1.0, 0.0]])
    # 定义zero padding层
    padding_layer = nn.ZeroPad2d(padding=1)

    # 进行zero padding
    padded_x = padding_layer(x)

    # 输出结果
    print(padded_x)
def clac_pooling():
    #计算池化结果
    # 定义输入张量
    I = torch.tensor([[9.0, 2.0, 6.0, 3.0],
                      [1.0, 5.0, 0.0, 8.0],
                      [5.0, 4.0, 5.0, 2.0],
                      [6.0, 3.0, 1.0, 7.0]])
    #计算pooling结果
    I = I.unsqueeze(0).unsqueeze(0)

    pool = nn.AvgPool2d(kernel_size=2,stride=2)
    Z = pool(I)
    #打印结果
    print(Z)

#准备一个CNN网络
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = torch.nn.Conv2d(3, 64, 6)
        # 定义第一个池化层
        #print(self.conv1.weight.shape)
        self.pool1 = torch.nn.MaxPool2d(2, 2)
        # 定义第二个卷积层，输入通道为64，输出通道为32，卷积核大小为16*16
        self.conv2 = torch.nn.Conv2d(64, 64, 4)
        # 定义第二个池化层
        self.pool2 = torch.nn.MaxPool2d(2, 2)
        # 定义第一个全连接层
        self.fc1 = torch.nn.Linear(64 * 5 * 5, 32)
        # 定义第二个全连接层
        self.fc2 = torch.nn.Linear(32, 10)

    def forward(self, x):
        # 输入x经过第一个卷积层和池化层后得到x
        #print(1,x.shape)
        x=self.conv1(x)
        #print(2,x.shape)
        x=torch.nn.functional.relu(x)
        #print(3,x.shape)
        x =self.pool1(x)
        #print(4,x.shape)
        # 输入x经过第二个卷积层和池化层后得到x
        x=self.conv2(x)
        #print(5,x.shape)
        x=torch.nn.functional.relu(x)
        #print(6,x.shape)
        x = self.pool2(x)
        #print(7,x.shape)
        # 将x展平为一维向量
        x = x.view(-1, 64 * 5 * 5)
        # 输入x经过第一个全连接层后得到x
        x = torch.nn.functional.relu(self.fc1(x))
        # 输入x经过第二个全连接层后得到x
        x = self.fc2(x)
        return x

def tranning_process(epochs,train_loader,valid_loader,optimizer,net,criterion):
    return_loss={}
    return_loss['traning_loss']=[]
    return_loss['validate_loss']=[]
    return_accuracy={}
    return_accuracy['traning_accuracy']=[]
    return_accuracy['validate_accuracy']=[]
    device = torch.device('mps')
    for epoch in range(epochs):  # 遍历多个轮次
        a=time.time()
        running_loss=[]
        for i, data in enumerate(train_loader, 0):
            inputs, labels = data
            inputs = inputs.to(device)  # move your inputs to device
            labels = labels.to(device)  # move your labels to device
            optimizer.zero_grad()
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss.append(loss.item())

        return_loss['traning_loss'].append(sum(running_loss)/len(running_loss))
        valid_loss = validate(net, valid_loader,criterion)
        return_loss['validate_loss'].append(valid_loss)
        train_acc=perdict_process(train_loader,net)
        return_accuracy['traning_accuracy'].append(train_acc)
        valid_acc=perdict_process(valid_loader,net)
        return_accuracy['validate_accuracy'].append(valid_acc)


        print('epoch',epoch)
        print('traning_loss',sum(running_loss)/len(running_loss))
        print('valid_loss',valid_loss)
        print('traning_accuracy',train_acc)
        print('valid_accuracy',valid_acc)
        print('time',time.time()-a)
        print('------------------')

    print('traning process is over')
    return return_loss,return_accuracy
def validate(net, valid_loader,criterion):
    # 初始化验证损失为0
    valid_loss =[]
    device = torch.device('mps')
    with torch.no_grad():
        for data in valid_loader:
            inputs, labels = data
            inputs = inputs.to(device)  # move your inputs to device
            labels = labels.to(device)  # move your labels to device
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            valid_loss.append(loss.item())
    return sum(valid_loss)/len(valid_loss)
def perdict_process(test_loarder,net):
    total=0
    correct=0
    device = torch.device('mps')
    with torch.no_grad():
        for data in test_loarder:
            images,labels=data
            images = images.to(device)  # move your inputs to device
            labels = labels.to(device)  # move your labels to device
            outputs=net(images)
            _,predicted=torch.max(outputs.data,1)
            total+=labels.size(0)
            correct+=(predicted==labels).sum().item()
    return correct/total

def nn_main():
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    training_data = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    testing_data = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)
    #将training_data切分成train_set和val_set
    train_set, val_set = utils.data.random_split(training_data, [50000, 10000])
    #定义训练集的dataloader
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=64, shuffle=True,num_workers=2)
    #定义验证集的dataloader
    val_loader = torch.utils.data.DataLoader(val_set, batch_size=64, shuffle=True,num_workers=2)
    #定义测试集的dataloader
    test_loader = torch.utils.data.DataLoader(testing_data, batch_size=64, shuffle=True,num_workers=2)
    model=CNN()
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    res_loss,res_acc=tranning_process(epochs=3,train_loader=train_loader,valid_loader=val_loader,optimizer=optimizer,net=model,criterion=criterion)
    acc= perdict_process(test_loader, model)
    print('accuracy of testdata:'+ str(acc))
    #针对res_loss里的训练损失和验证损失，绘制出训练损失和验证损失随epoch变化的曲线
    plt.plot(res_loss['traning_loss'],label='traning_loss')
    plt.plot(res_loss['validate_loss'],label='validate_loss')
    plt.legend()
    plt.show()
    plt.plot(res_acc['traning_accuracy'],label='traning_accuracy')
    plt.plot(res_acc['validate_accuracy'],label='validate_accuracy')
    plt.legend()
    plt.show()


def testnn():

    # 创建输入张量
    input_tensor = torch.randn(1, 3, 5, 5)  # 输入图像，大小为3x5x5

    # 创建卷积层
    conv = nn.Conv2d(in_channels=3, out_channels=1, kernel_size=3, stride=1, padding=0, bias=False)
    print(input_tensor)
    # 打印卷积层的权重
    print("卷积层的权重:")
    print(conv.weight)

    # 进行卷积操作
    output_tensor = conv(input_tensor)

    # 打印卷积结果的形状
    print("卷积结果的形状:")
    print(output_tensor.shape)
    print(output_tensor)



def classfication_cifar():
    transform = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.RandomCrop(32, padding=4),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    training_data = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
    test_data = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
    #打印训练集和测试集的大小
    print('训练集大小：',len(training_data))
    print('测试集大小：',len(test_data))
    # 将training_data切分成train_set和val_set
    train_set, val_set = utils.data.random_split(training_data, [40000, 10000])
    print('训练集大小：', len(train_set))
    print('验证集大小：', len(val_set))
    # 定义训练集的dataloader
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=64, shuffle=True, num_workers=2)

    # 定义验证集的dataloader
    val_loader = torch.utils.data.DataLoader(val_set, batch_size=64, shuffle=True, num_workers=2)

    # 定义测试集的dataloader
    test_loader = torch.utils.data.DataLoader(test_data, batch_size=64, shuffle=True, num_workers=2)
    model = CNN()
    #this is for mac
    device=torch.device('mps')
    model.to(device)

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.7)
    #optimizer = optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.99))
    res_loss, res_acc = tranning_process(epochs=150, train_loader=train_loader, valid_loader=val_loader,optimizer=optimizer, net=model, criterion=criterion)
    acc = perdict_process(test_loader, model)
    print('accuracy of testdata:' + str(acc))
 #针对res_loss里的训练损失和验证损失，绘制出训练损失和验证损失随epoch变化的曲线
    plt.plot(res_loss['traning_loss'],label='traning_loss')
    plt.plot(res_loss['validate_loss'],label='validate_loss')
    plt.legend()
    plt.show()
    plt.plot(res_acc['traning_accuracy'],label='traning_accuracy')
    plt.plot(res_acc['validate_accuracy'],label='validate_accuracy')
    plt.legend()
    plt.show()


def checkGPU():

    print(f"Is MPS (Metal Performance Shader) built? {torch.backends.mps.is_built()}")
    print(f"Is MPS available? {torch.backends.mps.is_available()}")
    device = torch.device('mps')
    print(device)


class cnn_clac_num(nn.Module):
    def __init__(self):
        super(cnn_clac_num, self).__init__()
        self.conv1 = torch.nn.Conv2d(in_channels=3, out_channels=4, kernel_size=3)
        self.pool1 = torch.nn.MaxPool2d(2, 2)
        self.conv2 = torch.nn.Conv2d(5, 5, 3)
        self.pool2 = torch.nn.MaxPool2d(2, 2)
        self.fc1 = torch.nn.Linear(64 * 5 * 5, 32)
        self.fc2 = torch.nn.Linear(32, 10)

    def forward(self, x):
        x =self.conv1(x)
        print('after conv1',x.shape)
        #计算此时总共有多少个参数
        print('conv1',self.conv1.weight.shape)
        x = self.pool1(torch.relu(x))
        x = self.conv2(x)
        x = self.pool2(torch.relu(x))

        x = x.view(-1, 64 * 5 * 5)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

#需要一个函数，返回两个字符串的Edit Distance
def edit_distance(str1,str2):
    len1=len(str1)
    len2=len(str2)
    dp=[[0 for i in range(len2+1)] for j in range(len1+1)]
    for i in range(len1+1):
        dp[i][0]=i
    for j in range(len2+1):
        dp[0][j]=j
    for i in range(1,len1+1):
        for j in range(1,len2+1):
            if str1[i-1]==str2[j-1]:
                dp[i][j]=dp[i-1][j-1]
            else:
                #dp[i-1][j]表示删除，dp[i][j-1]表示插入，dp[i-1][j-1]表示替换
                dp[i][j]=min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1])+1
    return dp[len1][len2]
if __name__ == '__main__':

    s=['CompName','StockPrice','NumExpl','ModelNumber','Color']
    s1=['BrandName','Headquarter','StockValue','Color','ModelSerial']

    for start in s:
        for end in s1:
            print(start,end,edit_distance(start,end))
