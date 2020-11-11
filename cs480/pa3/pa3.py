# TODO import the necessary classes and methods
import sys
from logic import PropKB,pl_true
from utils import Expr
# input C*D 获得 broad 的宽高
# input 获取已知的语句
# 生成initial KB  累计纳入Kb
# input  接入询问的语句， 给出知识库是否蕴含结果


# 读文件 ， 拆分开 宽高 ，获得的知识，询问等  ok
# 一个命题类，初始化KB ，tell函数，告诉新知识 ，ask 函数 ，获得结果集
# 进来的命题，拆分CNF ，CNF 给KB，调用推导
global broad_X,broad_Y,Additional_info,Query_Sentences
broad_X,broad_Y=0,0
Additional_info=[]
Query_Sentences=[]
def file_read(filename):
	global broad_X,broad_Y
	global Additional_info
	global Query_Sentences

	with open(filename,'r',encoding='utf-8') as f:
		res=f.readlines()
	tag=0
	for r in res:
		if 'Board size' in r:
			tag=1
		if 'Additional Info' in r:
			tag=2
		if 'Query Sentences' in r:
			tag=3
		if r[0]=='#':
			continue
		if tag==1:
			tmp=r.replace('\n', '').lower()
			if 'x' not in tmp:
				print("There is not have x in size,this code can not get the broad's x and y ")
				return
			broad_X=int(tmp.split('x')[0])
			broad_Y=int(tmp.split('x')[1])
		if tag==2:
			Additional_info.append(r.replace('\n', '').upper())
		if tag==3:
			Query_Sentences.append(r.replace('\n', '').upper())
def base_kb():
	init_KB=[]
	for x in range(0,broad_X):
		for y in range(0,broad_Y):
			_M=[]
			_B=[]
			if x > 0:

				_M.append("M" + str(x - 1) + str(y))
				_B.append("B" + str(x - 1) + str(y))
			if x + 1 < broad_X:

				_M.append("M" + str(x + 1) + str(y))
				_B.append("B" + str(x + 1) + str(y))
			if y > 0:

				_M.append("M" + str(x) + str(y-1))
				_B.append("B" + str(x) + str(y-1))

			if y + 1 < broad_Y:

				_M.append("M" + str(x) + str(y + 1))
				_B.append("B" + str(x) + str(y + 1))

			init_KB.append('B'+str(x)+str(y)+'==>'+'|'.join(_M))
			init_KB.append('M' + str(x) + str(y) + '==>' + '&'.join(_B))
	return init_KB




if __name__ == '__main__':

	input_file = sys.argv[1]
	file_read(input_file)
	KB=PropKB()
	init_clauses=base_kb()
	print(init_clauses)
	for S in init_clauses:
		KB.tell(S)
	#KB.tell('M20')
	for S in Additional_info:
		KB.tell(S)
	#KB.tell("B00<=>M10|M01")
	#for S in Query_Sentences:
	#	KB.ask_if_true(Expr(S))
		#print('Yes' if KB.ask_if_true(Expr('B21')) else 'No')
	print('Yes' if KB.ask_if_true(Expr('&',Expr('B11'),Expr('B22'))) else 'No')

