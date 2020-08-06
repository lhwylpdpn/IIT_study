#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time





class Q9(): 


    def __init__(self,cell):

        self.cell=cell
        for r in self.cell:
            r.insert(0,1)#每行首加阻碍
            r.append(1)#每行尾巴加阻碍
        self.cell.insert(0,[1]*len(cell[0]))
        self.cell.append([1]*len(cell[0]))

        print(cell)
        
        self.value = [[-1]*(len(cell[0])) for i in range(len(cell))]
    def recursively_withoutmem(self,i,j):# 得到到达这个点的可能之和
        

        

        if self.cell[i][j]==0:
            if i==1 and j==1:
                return 1


            if self.value[i][j]>0:
               # print('alreay',i,j)
                return self.value[i][j]

            if self.cell[i-1][j]==1 and self.cell[i][j-1]==1: #up 1 left 1 over
                   # print('a',i,j)
                    self.value[i][j]=0
                    return 0

            elif self.cell[i-1][j]==0 and self.cell[i][j-1]==0:#up 0 left 0  两种过来的可能之和
                   # print('b',i,j)
                    self.value[i][j]=self.recursively_withoutmem(i-1,j)+ self.recursively_withoutmem(i,j-1)
                    return  self.value[i][j]
            elif self.cell[i-1][j]==1 and self.cell[i][j-1]==0: #up1 left 0
                    self.value[i][j]=self.recursively_withoutmem(i,j-1)
                    return self.value[i][j]
            else:
                self.value[i][j]=self.recursively_withoutmem(i-1,j)
                return self.value[i][j]
        else:
            return 0


