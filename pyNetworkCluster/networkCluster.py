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
f = file("karate/karate-g.txt")#��ͼ���ļ�
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
print '������'+str(edgeNum)
print '������'+str(nodeNum)
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

#Ϊÿ���߼������
for edge in G.edges():
    id1 = edge[0]
    id2 = edge[1]
    G.edge[id1][id2]['myWeight'] = 0-calDistance(id1,id2)
#print G.edge
    
#������С������
spanTree = minimum_spanning_tree(G, weight='myWeight')
#print spanTree.edges()
graphs = list(nx.connected_component_subgraphs(spanTree))
print len(graphs)
print "��С�������ı�����"+str(len(spanTree.edges()))
#nx.draw_spring(spanTree)   
#plt.show()
'''
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
'''
#ÿ���߸���Ȩ��1
for edge in spanTree.edges():
    node1 = edge[0]
    node2 = edge[1]
    spanTree.add_edge(node1, node2, weight=1)
    spanTree.add_edge(node1, node2, between=0)
#print spanTree.edges()
    
#����߽���
path=nx.all_pairs_shortest_path(spanTree)
for i in range(1,nodeNum+1):
    for j in range(i+1,nodeNum+1):
        #print ijPath
        ijPath = path[i][j]
        size = len(ijPath)
        for node in range(size-1):
            spanTree[ijPath[node]][ijPath[node+1]]['between'] = spanTree[ijPath[node]][ijPath[node+1]]['between']+1

for i in range(1):
    #���������ı�
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

    #ȥ���ߣ�����ӡ
    spanTree.remove_edge(tNode1,tNode2)



subGraphs = list(nx.connected_component_subgraphs(spanTree))
num = len(subGraphs)#��ͼ����

#����
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
print 'QֵΪ'+str(mod)


output2 = file('karate\cluster.txt','w')
for graph in subGraphs:
    output2.write('���ţ�\n')
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
#����������ȥ���ض��ı�,�����Ϣ
output2 = file('clusters.txt','w')
output2.write('��С������������Щ�ߣ�')
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
num = len(subGraphs)#��ͼ����
print 'ȥ��6���ߣ�������'+str(num)+'������'


for graph in subGraphs:
    output2.write('���ţ�\n')
    for node in graph.nodes():
        output2.write(str(node))
        output2.write(' ')
    output2.write('\n')
output2.close()    
'''
