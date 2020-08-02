#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
class Solution(object):
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


if __name__ == '__main__':
    n=30
    a=time.time()
    res=Solution(n)
    t=res.numTrees(n)
    
    print(t)
    print(time.time()-a)
    b=time.time()
    x=res.numTrees_no_recursion(n)
    print(x)
    print(time.time()-b)