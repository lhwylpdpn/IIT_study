#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

# Q9 一个 N*M 的网格，1 代表有障碍物，0 代表没有障碍物。一个机器人，每次可以向下走一格 或者向右走一格。，要从（0,0）位置走到（n-1,m-1）位置，
#请问共有多少种不同的走法。 请给出代码实现，分析时间复杂度 
 
# 提示：请考虑动态规划 


#  输入 一张网 1和0 对应关系
#  向右，or  向下
#  子问题：{n*m}里每个区域的有多少种走法
#  
#  2*2 的格子里的子问题是： 
#  右侧是1，下侧是1 就终止
#  右侧是1，下侧是0 就向下
#  右侧是0，下侧是1 就向右
#  右和下都是0，向右是一种，向下是一种

# 子问题是：到达每个点，有几种路径过来的 ，重叠子问题是：到达最右下的点，总共有多少种走法
# 左侧1 ，上测1  始终到不了，返回0
# 左侧0, 上侧 1 retrun1 + 到达上个点的总可能数
# 左侧1 上册0 return1 + 到达上个点的总可能数
# 左0 上0 return 2 + 到达上个点的总可能数

# 每个递归 返回当前规模下最右点的到达总数
# 如果是最后一个点




class Q9():


    def __init__(self,cell):

        self.cell=cell
        for r in self.cell:
            r.insert(0,1)#每行首加阻碍
            r.append(1)#每行尾巴加阻碍
        self.cell.insert(0,[1]*len(cell[0]))
        self.cell.append([1]*len(cell[0]))

        #print(cell)
        
        self.value = [[-1]*(len(cell[0])) for i in range(len(cell))]
    def recursively_withoutmem(self,i,j):# 得到到达这个点的可能之和
        



        #print(i,j)
        if self.cell[i][j]==0:
            #print('all',i,j)
            if self.value[i][j]>0:
               # print('alreay',i,j)
                return self.value[i][j]

            if self.cell[i-1][j]==1 and self.cell[i][j-1]==1: #left 1 up 1 over
                   # print('a',i,j)
                    self.value[i][j]=0
                    return 0

            elif self.cell[i-1][j]==0 and self.cell[i][j-1]==0:#left 0 up 0  两种过来的可能之和
                   # print('b',i,j)
                    self.value[i][j]=self.recursively_withoutmem(i-1,j)+ self.recursively_withoutmem(i,j-1)
                    return  self.recursively_withoutmem(i-1,j)+ self.recursively_withoutmem(i,j-1)
            elif self.cell[i-1][j]==0 and self.cell[i][j-1]==1: #left 0 
                   # print('c',i,j)
                    self.value[i][j]=1+self.recursively_withoutmem(i-1,j)
                    return 1+self.recursively_withoutmem(i-1,j)
            elif self.cell[i-1][j]==1 and self.cell[i][j-1]==0: # up 0
                   # print('d',i,j)
                    self.value[i][j]=1+self.recursively_withoutmem(i,j-1)
                    return 1+self.recursively_withoutmem(i,j-1)


      

if __name__ == '__main__':
    # n=30
    # a=time.time()
    # res=Solution(n)
    # t=res.numTrees(n)
    
    # print(t)
    # print(time.time()-a)
    # b=time.time()
    # x=res.numTrees_no_recursion(n)
    # print(x)
    # print(time.time()-b)

    cell=[
  [0,0,0],
  [0,1,0],
  [0,0,0]
]
    m=len(cell[0])
    n=len(cell)
    obj=Q9(cell)
    print(cell)
    print(obj.recursively_withoutmem(i=m,j=n))