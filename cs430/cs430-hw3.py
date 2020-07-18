# !usr/bin/python 
# -*- coding:utf-8 -*-

import time
class Solution1(object):
    def maxValue(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        if not grid:
            return None
        value = [[-1]*(len(grid[0])) for i in range(len(grid))]
        return self.maxCore(grid, len(grid)-1, len(grid[0])-1, value)

    def maxCore(self, grid, i , j, value):
       # print(i,j,value[i][j])
        if value[i][j] != -1:
            return value[i][j]
        if i == 0 and j == 0:
            return grid[0][0]
        elif i == 0:
            return self.maxCore(grid, i, j-1, value) + grid[i][j]
        elif j == 0:
            return self.maxCore(grid, i-1, j, value) + grid[i][j]
        else:
            A = self.maxCore(grid, i-1, j, value) + grid[i][j]
            B = self.maxCore(grid, i, j-1, value) + grid[i][j]
            value[i][j] = max(A, B)
            return max(A, B)

 
class Solution(object):
 

    def __init__(self,grid):

        
        n=[[-1]*(len(grid[0])) for i in range(len(grid))]
        print(self.recursively_withoutmem(grid,i=0,j=0))
        
    def maxValue(self,grid):
        
        for x in range(0,len(grid)):
            
            if len(grid)==1 and len(grid[0])==1:
                return grid[0][0]
            if len(grid)<=1:
                return(grid[0][0]+self.maxValue([grid[x][1:len(grid[x])] for  x in range(0,len(grid))]))
            if len(grid[0])<=1:
            
                return(grid[0][0]+self.maxValue(grid[1:len(grid)]))
            return max(grid[0][0]+self.maxValue(grid[1:len(grid)]),grid[0][0]+self.maxValue([grid[x][1:len(grid[x])] for  x in range(0,len(grid))]))


    def recursively_withoutmem(self,grid,i,j):
        
      
            if i==len(grid)-1 and j==len(grid[0])-1:

                return grid[len(grid)-1][len(grid[0])-1]
            if i>=len(grid)-1: #move right
               
                return grid[i][j]+self.recursively_withoutmem(grid,i,j+1)
            if j>=len(grid[0])-1:# move down
                return grid[i][j]+self.recursively_withoutmem(grid,i+1,j)
            
            return max(grid[i][j]+self.recursively_withoutmem(grid,i,j+1),grid[i][j]+self.recursively_withoutmem(grid,i+1,j))
           

    def maxValue_4(self,grid,i,j,n):
        
      
            print('c',i,j,grid[i][j])
            if n[i][j]>=0:
                #print('s',i,j,n[i][j],n)
                return n[i][j]

            if i==len(grid)-1 and j==len(grid[0])-1:
                #n[i][j]=grid[0][0]
                #return n[i][j]
                return grid[len(grid)-1][len(grid[0])-1]
            if i==len(grid)-1: #move right
                #n[i][j]=grid[i][j]+self.maxValue_4(grid,i,j+1,n)
                #return n[i][j]
                #print(i,j)
                return grid[i][j]+self.maxValue_4(grid,i,j+1,n)
            if j==len(grid[0])-1:# move down
                #n[i][j]=grid[i][j]+self.maxValue_4(grid,i+1,j,n)
                #return n[i][j]
                return grid[i][j]+self.maxValue_4(grid,i+1,j,n)
            
            n[i][j]= max(grid[i][j]+self.maxValue_4(grid,i,j+1,n),grid[i][j]+self.maxValue_4(grid,i+1,j,n))
            #print('a',n[i][j])
            #print('o',n[i][j])
           # print('b',n[i][j])
            #print(i,j,n[i][j],n)
            return n[i][j]
            #return max(grid[i][j]+self.maxValue_3(grid,i,j+1),grid[i][j]+self.maxValue_3(grid,i+1,j))


    def iteratively_withmem(self,grid):
        
      

            for i in range(0,len(grid)):

                for j in range(0,len(grid[0])):

                    if i==0 and j==0:
                        continue
                    if i==0:
                        grid[i][j]+=grid[i][j-1]
                    elif j==0:
                        grid[i][j]+=grid[i-1][j]
                    else:
                        grid[i][j]=max(grid[i][j-1]+grid[i][j],grid[i-1][j]+grid[i][j])

            return grid[len(grid)-1][len(grid[0])-1]





if __name__ == '__main__':
    grid=[[7,1,3,5,8,9,9,2,1,9,0,8,3,1,6,6,9,5],[9,5,9,4,0,4,8,8,9,5,7,3,6,6,6,9,1,6],[8,2,9,1,3,1,9,7,2,5,3,1,2,4,8,2,8,8],[6,7,9,8,4,8,3,0,4,0,9,6,6,0,0,5,1,4],[7,1,3,1,8,8,3,1,2,1,5,0,2,1,9,1,1,4],[9,5,4,3,5,6,1,3,6,4,9,7,0,8,0,3,9,9],[1,4,2,5,8,7,7,0,0,7,1,2,1,2,7,7,7,4],[3,9,7,9,5,8,9,5,6,9,8,8,0,1,4,2,8,2],[1,5,2,2,2,5,6,3,9,3,1,7,9,6,8,6,8,3],[5,7,8,3,8,8,3,9,9,8,1,9,2,5,4,7,7,7],[2,3,2,4,8,5,1,7,2,9,5,2,4,2,9,2,8,7],[0,1,6,1,1,0,0,6,5,4,3,4,3,7,9,6,1,9]]
    #grid=[[1,2,3],[4,5,6]]
#     grid=[
#   [1,3,1],
#   [1,5,1],
#   [4,2,1]
# ]
    a=Solution(grid)
    p=a.iteratively_withmem(grid)
    print(p)
    #b=Solution1()
    #print(b.maxValue(grid))
    #print(a.maxValue_3(grid))