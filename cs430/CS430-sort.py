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

sys.setrecursionlimit(10000000)

class insertion_sort:

	def insertionsort(self,n):
		for x in range(1,len(n)):
			key=n[x]  
			i=x-1
			while i>=0 and key<n[i]:
				n[i+1]=n[i]
				i=i-1
			n[i+1]=key 
			

class heap_sort:


	def min_heapify(self,A,i):
		l=2*i+1
		r=2*i+2
		#print('68',A,i,l,r)

		if l<len(A):
			if A[l]>A[i]:
				smallest=i
			else:
				smallest=l
		else:
			smallest=i
		if r<len(A):
			if A[r]<A[smallest]:
				smallest=r
		#print(smallest)
		if smallest!=i:
			temp=A[i]
			A[i]=A[smallest]
			A[smallest]=temp
			self.min_heapify(A,smallest)
		else:
			pass

	def bulid_min_heap(self,A):
		#print(int(len(A)/2))
		i=int(len(A)/2)-1
		while i>=0:
			self.min_heapify(A,i)
			i=i-1

	def heapsort(self,A):
		self.bulid_min_heap(A)
		i=len(A)-1
		#print('TTT')
		b=[]
		while i>=0:
			#print(A[0])
			temp=A[0]
			A[0]=A[i]
			A[i]=temp
			#print('4',A[0],A)
			b.append(A[len(A)-1])
			A.pop()
			self.min_heapify(A,0)
			i=i-1
		
		return b



class quick_sort:

	def partition(self,n,p,r):

		random_x=random.randint(p,r-1)
		temp=n[random_x]
		n[random_x]=n[r]
		n[r]=temp

		x=n[r]
		i=p-1
		for j in range(p,r):
			#print(j,n[j]<=x)
			if n[j]<=x:
				i+=1
				temp=n[i]
				n[i]=n[j]
				n[j]=temp
		#print(n)
		temp=n[i+1]
		n[i+1]=n[r]
		n[r]=temp
		#print(n)
		return i+1

	def quicksort(self,n,p,r):
		if p<r:
			q=self.partition(n,p,r)
			#print(q)
			#time.sleep(1)
			self.quicksort(n,p,q-1)
			self.quicksort(n,q+1,r)


class merge_sort: 

	def merge(self,n,p,q,r):
		L=[]
		R=[]
		#print('connect',(p,q),(q,r)," as ",p,q,r)
		for i in range(0,q-p+1):
			L.append(n[p+i])
			#print(p,i,p+i-1)
		for j in range(0,r-q):
			R.append(n[q+j+1])
			#print(q+j)
		i=0
		j=0
		
		
		L.append(float("inf"))
		R.append(float("inf"))
		#print(L)
		#print(R)
		for k in range(p,r+1):
			
			if L[i]<=R[j]:
				n[k]=L[i]
				i+=1
			else:
				n[k]=R[j]
				j+=1
			#print(n[k])
		#print('connect after', n[p:r+1])
		
	def mergresort(self,n,p,r):
		if p<r:
			q=int((p+r)/2)
			#print((p,q),(q+1,r))
			#time.sleep(1)
			self.mergresort(n,p,q)
			self.mergresort(n,q+1,r)
			self.merge(n,p,q,r)


class bubble_sort:

	def bubblesort(A):
		for x in range(0,len(A)):
			for y in range(x,len(A)):
				if A[x]>A[y]:
					temp=A[x]
					A[x]=A[y]
					A[y]=temp

		return A






if __name__ == '__main__':

	num=100
	n=[]
	for x in range(0,num):
		n.append(random.randint(0,x))	

	print(n)
	test(n,0)
	print(n)
	# start=time.time()
	# clac=heap_sort()
	# res=clac.heapsort(n)
	# #print(res)
	# print(time.time()-start)
	


	# n=[]
	# for x in range(0,num):
	# 	n.append(random.randint(0,x))	
	# start=time.time()
	# clac=quick_sort()
	# clac.quicksort(n,0,len(n)-1)
	# #print(n)
	# print(time.time()-start)
	
	# n=[]
	# for x in range(0,num):
	# 	n.append(random.randint(0,x))	
	# #n=[1,2,3,4]
	# start=time.time()
	# clac=insertion_sort()
	# clac.insertionsort(n)
	# #print(n)
	# print(time.time()-start)
	




	# n=[]
	# for x in range(0,num):
	# 	n.append(random.randint(0,x))	

	# start=time.time()
	# clac=merge_sort()
	# clac.mergresort(n,0,len(n)-1)
	# #print(n)
	# print(time.time()-start)

	# n=[]
	# for x in range(0,num):
	# 	n.append(random.randint(0,x))	
	# start=time.time()
	# t=sorted(n)
	# #print(t)
	# print(time.time()-start)


