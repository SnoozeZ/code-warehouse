# -*- coding: cp936 -*-
import networkx as nx
from networkx.algorithms import *
import matplotlib.pyplot as plt
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
            a += matrix[i][j]
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
print len(graphs)
nx.draw_spring(spanTree)   
#plt.show()

#��ģ��������Ǹ��ߣ�����ɾ��
QSet = []#ÿһ�ε����Qֵ����
edgeSet = []#ÿһ��ɾ���ıߵ�����
for i in range(edgeNum-1):#ɾ��edgeNum��
    print '��'+str(i)+'��ɾ���������еı�...'
    hereQ = -1.0#���ڱ��浱ǰ�����Qֵ
    hereEdge = (-1,-1)#���ڱ���������Qֵ�ı�
    hereGraphs = []
    #������������ÿһ����
    for edge in spanTree.edges():
        id1 = edge[0]
        id2 = edge[1]
        #��ʱɾ����ǰ��
        spanTree.remove_edge(id1,id2)
        #����ɾ�������ߺ������˶��ٲ���ͨ����ͼ
        subGraphs = list(nx.connected_component_subgraphs(spanTree))
        num = len(subGraphs)#��ͼ����
        #��������
        matrix=[[0 for col in range(num)] for row in range(num)]
        #Ϊ����ֵ
        for i in range(num):
            for j in range(num):
                #�����������ţ���ͼ��i��j����������֮�����ӵı���
                count = 0
                for node1 in subGraphs[i].nodes():#i�е�node
                    for node2 in subGraphs[j].nodes():#j�е�node
                        if (node1,node2) in G.edges() or (node2,node1) in G.edges():
                            count +=1
                matrix[i][j] = ((count+0.0)/2)/edgeNum
        #����calModularity������������Qֵ
        #print 'cal Q'
        mod = calModularity(matrix,num)
        #����ǰ���ǲ���ȥ����������Qֵ��
        if mod > hereQ:#����ǣ�����
            hereQ = mod
            hereEdge = (id1,id2)
            hereGraphs = subGraphs
            spanTree.add_edge(id1,id2)
            #print matrix
            #print 'ȥ����('+str(id1)+','+str(id2)+')������ģ���Ϊ'+str(mod)+'�����ģ�'
        else:#������ǣ��������߲���
            #print 'ȥ����('+str(id1)+','+str(id2)+')������ģ���Ϊ'+str(mod)+'��������'
            spanTree.add_edge(id1,id2)
            #print matrix
    #���ֽ���,ɾ�����ߣ���ӡ
    spanTree.remove_edge(hereEdge[0],hereEdge[1])
    print '��'+str(i)+'��ȥ����('+str(hereEdge[0])+','+str(hereEdge[1])+')��ȥ����ģ���QΪ'+str(hereQ)
    QSet.append(hereQ)
    edgeSet.append((hereEdge[0],hereEdge[1]))
ouput = file('output.txt','w')
output.write(str(QSet))
output.write('\n')
output.write(str(edgeSet))
#��ͼ   
#nx.draw_random(spanTree)   
#plt.show()
print 'Complete!'



