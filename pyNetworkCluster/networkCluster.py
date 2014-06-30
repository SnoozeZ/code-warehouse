# -*- coding: cp936 -*-
import networkx as nx
from networkx.algorithms import *
import matplotlib.pyplot as plt
'''
G1=nx.Graph()
G1.add_node(12345)
G1.add_edge(12345,44444)
G1.add_node(44444)


print G1.number_of_nodes()
print G1.edge()
print G1.edges()'''
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
            a = matrix[i][j]
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
    #获取文章标题与id
    '''
    itemTitle = 'Hehe'
    itemID = i
    
    #插入图
    G.add_node(itemID,title = 'itemTitle')
    #获取文章关联的文章并插入边
    itemSet = [1,2,3]
    edgeNum += len(itemSet)#计算总边数
    for item in itemSet:
        G.add_edge(itemID,item)
    '''
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
spanTree.remove_edge(0,2)
graphs = list(nx.connected_component_subgraphs(spanTree))
print len(graphs)

#找模块度最大的那个边，并且删除
for i in range(edgeNum):#删除edgeNum次
    hereQ = -1.0
    hereEdge = (-1,-1)
    for edge in G.edges():#遍历生成树中每一条边
        id1 = edge[0]
        id2 = edge[1]
        #暂时删除当前边
        spanTree.remove_edge(id1,id2)
        #看看删了这条边后生成了多少不联通的子图
        subGraphs = list(nx.connected_component_subgraphs(spanTree))
        num = len(subGraphs)
        #建立矩阵
        matrix=[[0 for col in range(num)] for row in range(num)]
        #为矩阵赋值
        for i in range(num):
            for j in range(num):
                #对于两个社团i和j，计算它们之间连接的边数
                count = 0
                for node1 in subGraph[i].nodes():#i中的node
                    for node2 in subGraph[j].nodes:#j中的node
                        if (node1,nod2) in G.edges() or (node2,node1) in G.edges:
                            count +=1
                matrix[i][j] = (count+0.0)/2/edgeNum
        #计算这个矩阵的Q值
        mod = calModularity(matrix,num)
        #看当前边是不是去掉后产生最大Q值的
        if mod >hereQ:#如果是，保存
            hereQ = mod
            hereEdge = (id1,id2)
        else:#如果不是，把这条边补上
            spanTree.add_edge(id1,id2)
    #该轮结束，打印
    print '第'+str(i)+'次去掉边，去掉后模块度Q为'+str(hereQ)
        
nx.draw_random(spanTree)
plt.show()
print 'hhe'



