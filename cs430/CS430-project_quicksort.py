#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import random

class quick_sort:

	def __init__(self,n):
		self.n=n
		self.quicksort(self.n,0,len(n)-1)
	

	def partition(self,n,p,r):
		#取随机部分
		random_x=random.randint(p,r-1)
		temp=n[random_x]
		n[random_x]=n[r]
		n[r]=temp
		#取中值部分
		#n[r]=functionxxxx(n)
		x=n[r]
		i=p-1
		for j in range(p,r):
 
			if n[j]<=x:
				i+=1
				temp=n[i]
				n[i]=n[j]
				n[j]=temp

		temp=n[i+1]
		n[i+1]=n[r]
		n[r]=temp
		return i+1

	def quicksort(self,n,p,r):
		if p<r:
			q=self.partition(n,p,r)
			self.quicksort(n,p,q-1)
			self.quicksort(n,q+1,r)
	
	def get_res(self):
		return self.n

if __name__ == '__main__':
	



	num=1000
	n=[]
	for x in range(0,num):
		n.append(random.randint(0,x))

	obj=quick_sort(n)
	print(obj.get_res())

	