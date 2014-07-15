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
f = file("karate/karate-g.txt")#打开图的文件
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
print '边数：'+str(edgeNum)
print '点数：'+str(nodeNum)
#print G.edges()
#print edgeNum

output3 = file('karate\matrix.txt','w')
for i in range(nodeNum):
    for j in range (nodeNum):
        if (i,j) in G.edges() or (j,i) in G.edges():
            output3.write("1 ")
        else:
            output3.write("0 ")
    output3.write("\n")
output3.close()

#为每条边计算距离
for edge in G.edges():
    id1 = edge[0]
    id2 = edge[1]
    G.edge[id1][id2]['myWeight'] = 0-calDistance(id1,id2)
#print G.edge
    
#生成最小生成树
spanTree = minimum_spanning_tree(G, weight='myWeight')
#print spanTree.edges()
graphs = list(nx.connected_component_subgraphs(spanTree))
print len(graphs)
print "最小生成树的边数："+str(len(spanTree.edges()))
#nx.draw_spring(spanTree)   
#plt.show()
'''
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
'''
#每条边赋予权重1
for edge in spanTree.edges():
    node1 = edge[0]
    node2 = edge[1]
    spanTree.add_edge(node1, node2, weight=1)
    spanTree.add_edge(node1, node2, between=0)
#print spanTree.edges()
    
#计算边介数
path=nx.all_pairs_shortest_path(spanTree)
for i in range(1,nodeNum+1):
    for j in range(i+1,nodeNum+1):
        #print ijPath
        ijPath = path[i][j]
        size = len(ijPath)
        for node in range(size-1):
            spanTree[ijPath[node]][ijPath[node+1]]['between'] = spanTree[ijPath[node]][ijPath[node+1]]['between']+1

for i in range(1):
    #找最大介数的边
    tBetween = -10
    tNode1 = -1
    tNode2 = -1
    for edge in spanTree.edges():
        node1 = edge[0]
        node2 = edge[1]
        if spanTree[node1][node2]['between']>tBetween:
            tBetween = spanTree[node1][node2]['between']
            tNode1 = node1
            tNode2 = node2

    print 'The max betweenness is '+str(tBetween)+',the edge is '+str(tNode1)+','+str(tNode2)

    #去掉边，并打印
    spanTree.remove_edge(tNode1,tNode2)



subGraphs = list(nx.connected_component_subgraphs(spanTree))
num = len(subGraphs)#子图个数

#计算
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
print 'Q值为'+str(mod)


output2 = file('karate\cluster.txt','w')
for graph in subGraphs:
    output2.write('社团：\n')
    for node in graph.nodes():
        output2.write(str(node))
        output2.write(' ')
    output2.write('\n')
output2.close()  
                
'''
for node1 in spanTree.nodes():
    for node2 in spanTree.nodes():
        a=1
'''

'''
#在生成树中去掉特定的边,输出信息
output2 = file('clusters.txt','w')
output2.write('最小生成树中有这些边：')
for edge in spanTree.edges():
    output2.write(str(edge))
    output2.write('\n')
spanTree.remove_edge(0,3)
spanTree.remove_edge(4,30)
spanTree.remove_edge(30,67)
spanTree.remove_edge(46,102)
spanTree.remove_edge(7,58)
spanTree.remove_edge(8,20)

subGraphs = list(nx.connected_component_subgraphs(spanTree))
num = len(subGraphs)#子图个数
print '去掉6条边，生成了'+str(num)+'个社团'


for graph in subGraphs:
    output2.write('社团：\n')
    for node in graph.nodes():
        output2.write(str(node))
        output2.write(' ')
    output2.write('\n')
output2.close()    
'''
