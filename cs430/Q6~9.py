#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
class Q6():#q6

    def __init__(self,n):
        self.dp=[0]*(n+1)
        

    def numTrees(self,n):
        if self.dp[n]!=0:
            return self.dp[n]


        if n<=1:
            return 1
        res=0
        for m in range(1,n+1):
            res+=self.numTrees(m-1)*self.numTrees(n-m)
            self.dp[n]=res
        return self.dp[n]

    def numTrees_no_recursion(self,n):
        dp=[0]*(n+1)
        dp[0]=1
        dp[1]=1


        for m in range(2,n+1):
            for i in range(1,m+1):
                dp[m]+=dp[i-1]*dp[m-i]
        return dp[n]

class Q7:

    def delete_element(self,nums):

        i=0#kuai
        j=0#man

        for i in range(1,len(nums)):
            
            if nums[i]!=nums[j]:
                j+=1
                nums[j]=nums[i]
        print(nums[0:j+1])
        return j+1
                
class Q8:

    def return_sum_limit(self,nums,s):

        start=0
        end=0
        sum_=0
        min_=len(nums)+1
        for x in range(0,len(nums)):
            sum_+=nums[x]
            
            
            while sum_>=s:
                if end-start+1<=min_:
                    min_=end-start+1
                sum_=sum_-nums[start]
                start+=1
            end+=1
        return 0 if min_==len(nums)+1 else min_





class Q9(): 


    def __init__(self,cell):

        self.cell=cell
        for r in self.cell:
            r.insert(0,1)#每行首加阻碍
            r.append(1)#每行尾巴加阻碍
        self.cell.insert(0,[1]*len(cell[0]))
        self.cell.append([1]*len(cell[0]))
        
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


# Q11  难度正常 初始给出两个正整数，x 与 y，对 x 可以有两种操作，一种是 x = x * 2，另一种是 x = x – 1。 请设计一个算法，
# 求出最少需要多少次操作，可以把 x 变成 y。 
 
# 提示：该题最好使用贪心算法进行解答，暴力求解不可取。 
 
 
# 例   x = 3  y = 7   共需要 4 次  （3-1） * 2 * 2 – 1 = 7  这也是最少的步骤 



class Q11():

    def __init__(self):
        self.i=0

    def clac(self,x,y):

        while x!=y:
            self.i+=1
            if x<y:
                x=x*2
            else:
                x=x-1
        return self.i

class Q12():

    int smallestRangeII(vector<int>& A, int K) {
        sort(A.begin(),A.end());
        int n=A.size();
        int res=A[n-1]-A[0];
        for(int i=1;i<n;i++){
            int minB=min(A[0]+K,A[i]-K);
            int maxB=max(A[n-1]-K,A[i-1]+K);
            res=min(res,maxB-minB);



if __name__ == '__main__':

    #n=[2,3,1,2,4,3]

    #res=Q7()
    #n=[1,2,2,3]
    #print(res.delete_element(n))
    #res=Q8()
    #print(res.return_sum_limit(n,7))

    # x=3
    # y=7
    # res=Q11()
    # print(res.clac(x,y))
    n=[0,10]
    k=2
    res=Q12()
    res.smallestRangeII(n,k)
   


    