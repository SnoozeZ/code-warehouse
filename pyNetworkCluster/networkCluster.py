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

#����������֮��weight�ĺ���
def calDistance(i,j):
    #�ҵ���ͬ����
    sameNeighbor = []
    for ni in G.neighbors(i):
        for nj in G.neighbors(j):
            if ni == nj:
                sameNeighbor.append(ni)
    #����Щ��ͬ�����е�������
    count = 0
    for i in sameNeighbor:
        for j in sameNeighbor:
            if j in G.neighbors(i):
                count += 1
    count /= 2.0
    global edgeNum
    return count/edgeNum


#��������ģ���ֵ
def calModularity(matrix,size):
    Q = 0.0
    for i in range(size):
        a=0.0
        for j in range(size):
            a = matrix[i][j]
        Q += matrix[i][i]-a*a
    return Q

#��ʼ��ͼ

f = file("Book.txt")#��ͼ���ļ�
while True:
    line = f.readline()
    if len(line)==0:
        break
    line = line.strip('\n')
    line = line.split(';')
    id1 = int(line[0])
    id2 = int(line[1])
    #��ȡ���±�����id
    '''
    itemTitle = 'Hehe'
    itemID = i
    
    #����ͼ
    G.add_node(itemID,title = 'itemTitle')
    #��ȡ���¹��������²������
    itemSet = [1,2,3]
    edgeNum += len(itemSet)#�����ܱ���
    for item in itemSet:
        G.add_edge(itemID,item)
    '''
    #����ͼ
    G.add_edge(id1,id2)
    
edgeNum = len(G.edges())
nodeNum = len(G.nodes())
#print G.edges()
#print edgeNum

#Ϊÿ���߼������
for edge in G.edges():
    id1 = edge[0]
    id2 = edge[1]
    G.edge[id1][id2]['weight'] = 0-calDistance(id1,id2)

#print G.edge

#������С������
spanTree = minimum_spanning_tree(G, weight='weight')
print spanTree.edges()
graphs = list(nx.connected_component_subgraphs(spanTree))
spanTree.remove_edge(0,2)
graphs = list(nx.connected_component_subgraphs(spanTree))
print len(graphs)

#��ģ��������Ǹ��ߣ�����ɾ��
for i in range(edgeNum):#ɾ��edgeNum��
    hereQ = -1.0
    hereEdge = (-1,-1)
    for edge in G.edges():#������������ÿһ����
        id1 = edge[0]
        id2 = edge[1]
        #��ʱɾ����ǰ��
        spanTree.remove_edge(id1,id2)
        #����ɾ�������ߺ������˶��ٲ���ͨ����ͼ
        subGraphs = list(nx.connected_component_subgraphs(spanTree))
        num = len(subGraphs)
        #��������
        matrix=[[0 for col in range(num)] for row in range(num)]
        #Ϊ����ֵ
        for i in range(num):
            for j in range(num):
                #������������i��j����������֮�����ӵı���
                count = 0
                for node1 in subGraph[i].nodes():#i�е�node
                    for node2 in subGraph[j].nodes:#j�е�node
                        if (node1,nod2) in G.edges() or (node2,node1) in G.edges:
                            count +=1
                matrix[i][j] = (count+0.0)/2/edgeNum
        #������������Qֵ
        mod = calModularity(matrix,num)
        #����ǰ���ǲ���ȥ����������Qֵ��
        if mod >hereQ:#����ǣ�����
            hereQ = mod
            hereEdge = (id1,id2)
        else:#������ǣ��������߲���
            spanTree.add_edge(id1,id2)
    #���ֽ�������ӡ
    print '��'+str(i)+'��ȥ���ߣ�ȥ����ģ���QΪ'+str(hereQ)
        
nx.draw_random(spanTree)
plt.show()
print 'hhe'



