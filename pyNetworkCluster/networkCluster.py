# -*- coding: cp936 -*-
import networkx as nx
from networkx.algorithms import *
import matplotlib.pyplot as plt
G=nx.Graph()
nodeNum = 104
edgeNum = 0

#计算两个点之间weight的函数
def calDistance(i,j):
    #找到共同好友
    sameNeighbor = []
    for ni in G.neighbors(i):
        for nj in G.neighbors(j):
            if ni == nj:
                sameNeighbor.append(ni)
    #看这些共同好友中的连接数
    count = 0
    for i in sameNeighbor:
        for j in sameNeighbor:
            if j in G.neighbors(i):
                count += 1
    count /= 2.0
    global edgeNum
    return count/edgeNum

#计算矩阵的模块度值
def calModularity(matrix,size):
    Q = 0.0
    for i in range(size):
        a=0.0
        for j in range(size):
            a += matrix[i][j]
        Q += matrix[i][i]-a*a
    return Q

#初始化图
f = file("Book.txt")#打开图的文件
while True:
    line = f.readline()
    if len(line)==0:
        break
    line = line.strip('\n')
    line = line.split(';')
    id1 = int(line[0])
    id2 = int(line[1])
    #插入图
    G.add_edge(id1,id2)
edgeNum = len(G.edges())
nodeNum = len(G.nodes())
#print G.edges()
#print edgeNum

#为每条边计算距离
for edge in G.edges():
    id1 = edge[0]
    id2 = edge[1]
    G.edge[id1][id2]['weight'] = 0-calDistance(id1,id2)
#print G.edge
    
#生成最小生成树
spanTree = minimum_spanning_tree(G, weight='weight')
print spanTree.edges()
graphs = list(nx.connected_component_subgraphs(spanTree))
print len(graphs)
nx.draw_spring(spanTree)   
#plt.show()

#找模块度最大的那个边，并且删除
QSet = []#每一次的最大Q值序列
edgeSet = []#每一次删除的边的序列
for i in range(edgeNum-1):#删除edgeNum次
    print '第'+str(i)+'次删除生成树中的边...'
    hereQ = -1.0#用于保存当前轮最大Q值
    hereEdge = (-1,-1)#用于保存产生最大Q值的边
    hereGraphs = []
    #遍历生成树中每一条边
    for edge in spanTree.edges():
        id1 = edge[0]
        id2 = edge[1]
        #暂时删除当前边
        spanTree.remove_edge(id1,id2)
        #看看删了这条边后生成了多少不联通的子图
        subGraphs = list(nx.connected_component_subgraphs(spanTree))
        num = len(subGraphs)#子图个数
        #建立矩阵
        matrix=[[0 for col in range(num)] for row in range(num)]
        #为矩阵赋值
        for i in range(num):
            for j in range(num):
                #对于两个社团（子图）i和j，计算它们之间连接的边数
                count = 0
                for node1 in subGraphs[i].nodes():#i中的node
                    for node2 in subGraphs[j].nodes():#j中的node
                        if (node1,node2) in G.edges() or (node2,node1) in G.edges():
                            count +=1
                matrix[i][j] = ((count+0.0)/2)/edgeNum
        #调用calModularity计算这个矩阵的Q值
        #print 'cal Q'
        mod = calModularity(matrix,num)
        #看当前边是不是去掉后产生最大Q值的
        if mod > hereQ:#如果是，保存
            hereQ = mod
            hereEdge = (id1,id2)
            hereGraphs = subGraphs
            spanTree.add_edge(id1,id2)
            #print matrix
            #print '去掉边('+str(id1)+','+str(id2)+')产生的模块度为'+str(mod)+'是最大的！'
        else:#如果不是，把这条边补上
            #print '去掉边('+str(id1)+','+str(id2)+')产生的模块度为'+str(mod)+'不是最大的'
            spanTree.add_edge(id1,id2)
            #print matrix
    #该轮结束,删除最大边，打印
    spanTree.remove_edge(hereEdge[0],hereEdge[1])
    print '第'+str(i)+'次去掉边('+str(hereEdge[0])+','+str(hereEdge[1])+')，去掉后模块度Q为'+str(hereQ)
    QSet.append(hereQ)
    edgeSet.append((hereEdge[0],hereEdge[1]))
ouput = file('output.txt','w')
output.write(str(QSet))
output.write('\n')
output.write(str(edgeSet))
#画图   
#nx.draw_random(spanTree)   
#plt.show()
print 'Complete!'



