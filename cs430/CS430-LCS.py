#!/usr/bin/python
# -*- coding: UTF-8 -*- 



import os
import sys
import time
import csv
import sys
import datetime
import os
import shutil
import random



class Solution(object):
    def longestCommonSubsequence(self, text1, text2):
        text1.insert(0,0)
        text2.insert(0,0)
        m=len(text1) # have m rows
        n=len(text2) # have n columns
        c= [ [0] * (n) for _ in range(m)]
        
        b= [ [0] * (n) for _ in range(m)]
        for i in range(0,m):
        	c[i][0]=0
        for j in range(0,n):
        	c[0][j]=0

        for i in range(1,m):
        	for j in range(1,n):

        		if text1[i]==text2[j]:
        			c[i][j]=c[i-1][j-1]+1
        			b[i][j]=0
        		elif c[i-1][j]>=c[i][j-1]:
        			c[i][j]=c[i-1][j]
        			b[i][j]=1
        		else:
        			c[i][j]=c[i][j-1]
        			b[i][j]=2
       	#for r in range(0,len(c)):
       	#	print(c[r])
        self.PRINT_LCS(b,text1,m-1,n-1)
    def PRINT_LCS(self,b,X,i,j):
    	#print(i,j,b[i][j])
    	if i==0 or j==0:
    		return
    	if b[i][j]==0:
    		
    		self.PRINT_LCS(b,X,i-1,j-1)
    		print(X[i])
    	elif b[i][j]==1:
    		self.PRINT_LCS(b,X,i-1,j)
        else:
        	self.PRINT_LCS(b,X,i,j-1)



if __name__ == '__main__':
	text1=['A','B','C','B','D','A','B']
	text2=['B','D','C','A','B','A']
	text1=[1,0,0,1,0,1,0,1]
	text2=[0,1,0,1,1,0,1,1,0]
	obj_=Solution()
	obj_.longestCommonSubsequence(text1,text2)