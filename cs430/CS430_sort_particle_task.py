#-*- coding: utf-8 -*-
       
import random

def reverseString(self, s): #task1 反转字符串
    
    for x in range(0,int(len(s)/2)):
        temp=s[x]
        s[x]=s[len(s)-1-x]
        s[len(s)-1-x]=temp
    

# 时间复杂度 T(n)=O(n/2)=O(n)


 
def intersection(self, nums1, nums2): #task2 取交集 、去重
    dict_A={}

    res=[]
    for x in range(0,len(nums1)):

        if nums1[x] in dict_A:
            dict_A[nums1[x]]=dict_A[nums1[x]]+1
        else:
            dict_A[nums1[x]]=0

    for x in dict_A.keys():

        if x in nums2:
            res.append(x)

    return res

# 时间复杂度 假设数组1的长度为n，数组2的长度为m T(n)=O(n+m)






class merge_sort: 
	
	def __init__(self):
		self.res=0

	def merge(self,n,p,q,r):
		L=[]
		R=[]
		for i in range(0,q-p+1):
			L.append(n[p+i])
		for j in range(0,r-q):
			R.append(n[q+j+1])
		i=0
		j=0
		
		
		L.append(float("inf"))
		R.append(float("inf"))

		for k in range(p,r+1):
			
			if L[i]<=R[j]:
				n[k]=L[i]
				i+=1
			else:
				print(R[j],q-i+1)
				self.res+=q-i
				n[k]=R[j]
				j+=1
		print('merge',p,q,r)
		




	def mergresort(self,n,p,r):
		
		if p<r:
			q=int((p+r)/2)
			#print((p,q),(q+1,r))
			#time.sleep(1)
			self.mergresort(n,p,q)
			self.mergresort(n,q+1,r)
			self.merge(n,p,q,r)




class minik(object):# task - 返回数组的最小的k个值
   
    def partition(self,n,p,r):

        random_x=random.randint(p,r-1)
        temp=n[random_x]
        n[random_x]=n[r]
        n[r]=temp

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
        if p<self.end:
            q=self.partition(n,p,r)
            self.quicksort(n,p,q-1)
            self.quicksort(n,q+1,r)
        
    def smallestK(self, n, k):
        if len(n)==0 or k<=0:
            return []

        self.end=k
        self.quicksort(n,0,len(n)-1)
        return n[0:self.end]

# 时间复杂度 应该是 O(n),但是证明过程还在梳理，有点没能理解透彻





if __name__ == '__main__':
	n=[]
	for x in range(0,10):
		n.append(random.randint(0,x))
	k=3
	clac=minik()
	print(n)
	print(clac.smallestK(n,k))



