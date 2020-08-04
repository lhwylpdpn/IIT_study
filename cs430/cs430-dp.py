#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
class Solution():#q6

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




 


if __name__ == '__main__':

    n=[2,3,1,2,4,3]

    #res=Q7()
    #n=[1,2,2,3]
    #print(res.delete_element(n))
    res=Q8()
    print(res.return_sum_limit(n,7))

    




    