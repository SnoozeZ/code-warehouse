# -*- coding: utf-8 -*-
import networkx as nx
from random import *
import matplotlib.pyplot as plot
from networkx.algorithms import *

nodeNumber = 1000 #节点个数
averageDegree = 100 #平均度数
probDegree = 0.01 #E-R模型中边有效的概率


def init(G1,G2): #返回一个随机ER网络,G1为现实网络，G2为在线网络
	G1 = nx.fast_gnp_random_graph(nodeNumber, probDegree)
	G2 = nx.fast_gnp_random_graph(nodeNumber, probDegree)
	r = Random()	#随机数生成器
	#现实网络
	Y = []
	for edge in G1.edges():	#边赋予权值
		id1 = edge[0]
		id2 = edge[1]
		weight = r.gauss(0.3,0.1)
		G1.edge[id1][id2]['weight'] = weight
		weight = 1 if weight>1 else weight #边界检查
		weight = 0 if weight<0 else weight
		Y.append(weight)
	plot.hist(Y, bins=50, normed=1, facecolor='green', alpha=0.75)
	plot.title('Real LT network\'s edges\'degree distribution' )
	plot.show()

	Y = []
	for node in G1.nodes(): #点赋予阈值
		threshold = r.gauss(0.3,0.1)
		threshold = 1 if threshold>1 else threshold #边界检查
		threshold = 0 if threshold<0 else threshold
		G1.node['threshold'] = threshold
		Y.append(threshold)	
	plot.hist(Y, bins=50, normed=1, facecolor='green', alpha=0.75)
	plot.title('Real LT network\'s node\'s threshold distribution' )
	plot.show()

	#在线网络
	Y = []	
	for edge in G2.edges():
		id1 = edge[0]
		id2 = edge[1]
		prob = r.gauss(0.5,0.1)
		prob = 1 if prob>1 else prob #边界检查
		prob = 0 if prob<0 else prob
		G2.edge[id1][id2]['actProb'] = prob	#边的激活高斯分布
		Y.append(prob)
	plot.hist(Y, bins=50, normed=1, facecolor='green', alpha=0.75)
	plot.title('Online IC network\'s edge\'s activate probability distribution' )
	plot.show()
	

def performCascade():
	return 1


if __name__ == '__main__':
	G1 = nx.Graph()		#face-to-face 网络
	G2 = nx.Graph()		#online 网络
	init(G1,G2)
	print "蛤蛤"
	a = Random()
	print a.gauss(0,0.5)
	Y = []
	for i in range(10000):
		Y.append(a.gauss(0,0.5))
	#plot.hist(Y, bins=50, normed=1, facecolor='green', alpha=0.75)
	#plot.show()
