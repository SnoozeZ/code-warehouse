# -*- coding: utf-8 -*-
import networkx as nx
from random import *
import random
import matplotlib.pyplot as plot
from networkx.algorithms import *

nodeNumber = 1000 		#节点个数
averageDegree = 100 	#平均度数
probDegree = 0.01 		#E-R模型中边有效的概率
activeNumG1 = 50 		#现实网络中的初始激活数量
activeNumG2 = 10 		#在线网络中的初始激活数量 
disFig = False 			#是否显示图片
crossAlpha = 0.01		#Self reinforcement 因子
crossBeta = 0.01		#Neighborhood reinforcement 因子

def displayFigure(Y,title):
	if disFig:
		plot.hist(Y, bins=50, normed=1, facecolor='green', alpha=0.75)
		plot.title(title)
		plot.show()

def probTrue(prob):# 以prob的概率返回一个真值
	if prob<0 or prob>1:
		print "Ilegal probability when call \'probTrue\' function" 
	if random.random()<prob:
		return True
	else:
		return False

def construct(G1,G2): #返回一个随机ER网络,G1为现实网络，G2为在线网络
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
	displayFigure(Y,'Real LT network\'s edges\'weight distribution')

	Y = []
	for node in G1.nodes(): #点赋予阈值
		threshold = r.gauss(0.3,0.1)
		threshold = 1 if threshold>1 else threshold #边界检查
		threshold = 0 if threshold<0 else threshold
		G1.node[node]['threshold'] = threshold
		Y.append(threshold)	
		G1.node[node]['active'] = False	#点初始为不激活
	displayFigure(Y,'Real LT network\'s node\'s threshold distribution')

	#在线网络
	Y = []	
	for edge in G2.edges():#每条边赋予激活概率
		id1 = edge[0]
		id2 = edge[1]
		prob = r.gauss(0.5,0.1)
		prob = 1 if prob>1 else prob #边界检查
		prob = 0 if prob<0 else prob
		G2.edge[id1][id2]['actProb'] = prob	#边的激活高斯分布
		Y.append(prob)

		G2[id1][id2]['unuse'] = True 	#初始化为未使用过 

	for node in G2.nodes():	
		G2.node[node]['active'] = False #点初始化为不激活
		G2.node[node]['selfProb'] = 1
	displayFigure(Y,'Online IC network\'s edge\'s activate probability distribution')

	return (G1,G2)

def init(G1,G2):	#为两个网络赋予初始的激活点
	
	#为G1 LT现实网络挑选初始激活点
	actList = range(0,nodeNumber)
	actList = random.sample(actList, activeNumG1)
	for node in actList:
		G1.node[node]['active'] = True

	#为G2 LC现实网络挑选初始激活点
	actList = range(0,nodeNumber)
	actList = random.sample(actList, activeNumG2)
	for node in actList:
		G2.node[node]['active'] = True

	return (G1,G2)

def performCascade(G1,G2):
	#现实LT网络层内扩散
	totalWeight = 0
	actList = [] 	#本次扩散中，被激活的点
	for node in G1.nodes():
		if not G1.node[node]['active']:	#当前点未被激活
			totalWeight = 0
			for edge in nx.edges(G1,node):
				print edge
				id1 = edge[0]
				id2 = edge[1]
				if G1.node[id2]['active']:
					totalWeight += G1.edge[id1][id2]['weight']
			if totalWeight >= G1.node[node]['threshold']:	#如果影响力大于阈值
				G1.node[node]['active'] = True
				actList.append(node)
	#现实网络向在线网络扩散
	for node in actList:
		if not G2.node[node]['active']:	#Self reinforcement
			G2.node[node]['selfProb'] *= 1+crossAlpha
		else:	#neighborhood reinforcement
			for edge in nx.edges(G2,node):
				id1 = edge[0]
				id2 = edge[1]
				temp = G2.edge[id1][id2]['actProb']
				temp *= 1+crossBeta
				temp = 0 if temp<0 else temp
				temp = 1 if temp>1 else temp
				G2.edge[id1][id2]['actProb'] = temp

	#在线IC网络的层内扩散
	actList = []
	for node in G2.nodes():
		if not G2.node[node]['active']:
			totalProb = 1
			for edge in nx.edges(G2,node):
				id1 = edge[0]
				id2 = edge[1]
				if G2.node[id2]['active'] and G2.node[id2]['unuse']:
					totalProb *= 1 - G2.edge[id1][id2]
			totalProb = (1 - totalProb)*G2.node[node]['selfProb']
			if probTrue(totalProb):
				G2.node[node]['active'] = True
				actList.append(node)

	#IC网络向LT网络的扩散
	for node in actList:
		if not G1.node[node]['active']:	#Self reinforcement
			temp = G1.node[node]['threshold']
			temp *= 1- crossAlpha
			temp = 0 if temp<0 else temp
			temp = 1 if temp>1 else temp
			G1.node[node]['threshold'] = temp
		else:	#Neighborhood reinforcement



		






	print len(G1.edges())
	return (G1,G2)


if __name__ == '__main__':
	G1 = nx.Graph()		#face-to-face 网络
	G2 = nx.Graph()		#online 网络
	(G1,G2) = construct(G1,G2)
	(G1,G2) = init(G1,G2)
	#(G1,G2) = performCascade(G1,G2)
	print "蛤蛤"
	a = Random()
	Y = []
	for i in range(10000):
		Y.append(a.gauss(0,0.5))
	#plot.hist(Y, bins=50, normed=1, facecolor='green', alpha=0.75)
	#plot.show()
