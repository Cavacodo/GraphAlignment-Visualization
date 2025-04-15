# 作者：York
# 时间：2022/4/26 13:25
import math
import random
import os
import torch

from deepmatch.initialMatching import *
from algorithms.network_alignment_model import NetworkAlignmentModel
from deepmatch.initialMatching import map_prob_maxtrix, munkres
from utils.graph_utils import load_gt
import networkx as nx
import matplotlib.pyplot as plt
import torch.nn.functional as F
from algorithms.CloAlign.embedding import GCN

class CloAlign():

    def __init__(self,args):
        super(CloAlign, self).__init__()
        self.args = args
        self.input_graph = self.load_G(self.args.input_graph)
        self.output_graph = self.args.output_graph
    def align(self):
        print(f'G is {self.input_graph}')
        sample = self.args.sample
        print(sample)
        repeat = self.args.repeat
        for i in sample:
            score_count = 0.0
            for j in range(repeat):
                G = self.input_graph
                nodes = self.combin_graph_final(i, 8 * int(math.sqrt(G.number_of_nodes())), "./aline_true.txt", self.output_graph, False)
                print(nodes,type(nodes))
                new_G = self.load_G(self.args.output_graph)
                emb = self.embd(new_G)
        return emb


    def embd(self,G):
        node_number = G.number_of_nodes()
        edge_number = G.number_of_edges()
        adj = nx.adjacency_matrix(G).todense()

        print(f'new_G is {G}')
        print(f'新图的节点数为：{node_number},新图的边数为：{edge_number}')
        print(f'新图的邻接矩阵为：{adj}')
        print(f'{adj.shape}')
        I = self.const_I(node_number)
        model = GCN(I.shape[1],
                    nhid=512,
                    nclass=128,
                    dropout=0.5)
        optimizer = torch.optim.Adam(model.parameters(),lr=0.01, weight_decay=5e-4)

        embd0 = model(I, adj)
        print(f'emb is {embd0}')
        print(embd0.shape)
        return embd0

    def const_I(self,size):
        I = torch.eye(size)
        return I
    def tag(self,list1, num):  # list1采样列表，num当前节点编号，sample，采样数量，n原图节点
        return list1.index(num)

    def combin_graph_final(self,ratio,sample_nodes,aline_file,out_graph,isdirected):
        # True代表无向图
        G = self.input_graph
        print("原图节点数：" + str(G.number_of_nodes()))
        # 去除一定的边
        G1_sample = sample_graph(G, ratio)
        print("破坏后图中节点：" + str(G1_sample.number_of_nodes()))
        G2 = get_subgraph(G1_sample, sample_nodes)
        GC2 = max((G2.subgraph(c1) for c1 in nx.connected_components(G2)), key=len)
        G1 = get_subgraph(G, sample_nodes)
        GC1 = max((G1.subgraph(c1) for c1 in nx.connected_components(G1)), key=len)

        # 匹配的点
        nodes_match = []
        # 不匹配的点
        nodes_no_match = {}

        nodes_G2 = list(G1_sample.nodes())
        # nodes_G2.sort()
        seed_time1 = time.time()
        matches_ms = bipartite_matching(GC1, GC2)
        seed_time2 = time.time()
        seed_time = seed_time2 - seed_time1
        # print("seed time is %f" % seed_time)
        nodes_g2 = []
        # print("before %f" % len(nodes_G2))
        for match in matches_ms:
            nodes_G2.remove(match[1])
            nodes_g2.append(match[1])
            if match[0] == match[1]:
                nodes_match.append(match[1])
                nodes_match.sort()
            else:
                nodes_no_match[match[1]] = match[0]
        # print("after %f" % len(nodes_G2))
        print("不匹配的点")
        print(nodes_no_match)
        # 图1中不匹配的点
        match_g1 = list(nodes_no_match.keys())
        # 图2中不匹配的点
        match_g2 = list(nodes_no_match.values())

        out_graph_begin = time.time()
        dict1 = {}
        s = G.order()
        for i in nodes_G2:
            dict1[i] = s
            s = s + 1
        # 结合图
        # f = open(out_graph,'w')
        dict1.update(nodes_no_match)
        G1_sample = nx.relabel_nodes(G1_sample, dict1)

        compose_graph = nx.compose(G, G1_sample)

        nx.write_edgelist(compose_graph, out_graph, data=False) #每次都写在服务器上面了
        out_graph_after = time.time()
        print("write out graph time is %f" % (out_graph_after - out_graph_begin))
        # 写原图
        # print("writing source graph")
        # for i in edges_g1:
        #     f.writelines(str(i[0])+" "+str(i[1])+"\n")
        # print("writing source graph done")
        # #写目标图
        # print("writing taget graph")
        # for i in edges_g2:
        #     u=i[0]
        #     v=i[1]
        #     if u in nodes_match and v in nodes_match:
        #         continue
        #     if u not in nodes_match:
        #         if u in match_g2:
        #             u = match_g1[match_g2.index(u)]
        #         else:
        #             # 采样列表，当前节点编号，采样数量，原图节点
        #             # u = tag(nodes_G2, u)+G.order()
        #             u=dict1[u]+G.order()
        #     if v not in nodes_match:
        #         if v in match_g2:
        #             v = match_g1[match_g2.index(v)]
        #         else:
        #             # v = tag(nodes_G2, v)+G.order()
        #             v = dict1[v] + G.order()
        #     f.writelines(str(u) + " " + str(v)+"\n")
        # f.close()
        # print("writing taget graph done")
        # out_graph_after = time.time()
        # print("write out graph time is %f" % (out_graph_after-out_graph_begin))
        # G_new = load_file(out_graph)
        # 有节点丢失
        # print("新图节点总数："+str(G.number_of_nodes()*2-len(nodes_g2)))
        # print(dict1)
        # 在新图上实际对应节点
        #aline_file ='/home/pjjiang/PaperCode/Clo_Align/GCNA-master(zhu)/aline_true.txt'
        fb = open(aline_file, 'w')
        print("aline path:", aline_file)
        print(fb)
        for i in nodes_G2:
            fb.writelines(str(i) + " " + str(dict1[i]) + "\n")
        fb.close()
        self.const(G.order() + len(nodes_G2), isdirected, out_graph)
        # edgelist = nx.read_edgelist(out_graph)
        self.write_ini(G.order()+len(nodes_G2), compose_graph, nodes_match, dict1)
        return G.order() + len(nodes_G2)


        """G = self.input_graph
        self.draw_G(G)
        print("原图节点数：" + str(G.number_of_nodes()))
        G1_sample = self.sample_graph(G,ratio)
        print("破坏后图中节点：" + str(G1_sample.number_of_nodes()))
        G2 = self.get_subgraph(G1_sample, sample_nodes)
        GC2 = max((G2.subgraph(c1) for c1 in nx.connected_components(G2)), key=len)
        G1 = self.get_subgraph(G, sample_nodes)
        GC1 = max((G1.subgraph(c1) for c1 in nx.connected_components(G1)), key=len)
        print(f'GC2 is {GC2},GC1 is {GC1}')

        # 匹配的点
        nodes_match = []
        # 不匹配的点
        nodes_no_match = {}

        nodes_G2 = list(G1_sample.nodes())
        nodes_G2.sort()
        matches_ms = self.bipartite_matching(GC1, GC2)
        nodes_g2 = []
        for match in matches_ms:
            nodes_G2.remove(match[1])
            nodes_g2.append(match[1])
            if match[0] == match[1]:
                nodes_match.append(match[1])
                nodes_match.sort()
            else:
                nodes_no_match[match[0]] = match[1]

        print("不匹配的点")
        print(nodes_no_match)
        # 图1中不匹配的点
        match_g1 = list(nodes_no_match.keys())
        # 图2中不匹配的点
        match_g2 = list(nodes_no_match.values())
        print(match_g1)
        print(match_g2)

        # 结合图
        f = open(out_graph, 'w')
        edges_g1 = G.edges()
        edges_g2 = G1_sample.edges()
        # 写原图
        for i in edges_g1:
            f.writelines(str(i[0]) + " " + str(i[1]) + "\n")
        # 写目标图
        for i in edges_g2:
            u = i[0]
            v = i[1]
            if u in nodes_match and v in nodes_match:
                continue
            if u not in nodes_match:
                if u in match_g2:
                    u = match_g1[match_g2.index(u)]
                else:
                    # 采样列表，当前节点编号，采样数量，原图节点
                    u = self.tag(nodes_G2, u) + G.order()
            if v not in nodes_match:
                if v in match_g2:
                    v = match_g1[match_g2.index(v)]
                else:
                    v = self.tag(nodes_G2, v) + G.order()
            f.writelines(str(u) + " " + str(v) + "\n")

        f.close()
        # G_new = load_file(out_graph)
        # 有节点丢失
        print("新图节点总数：" + str(G.number_of_nodes() * 2 - len(nodes_g2)))

        # 在新图上实际对应节点
        fb = open(aline_file, 'w')
        for i in G1_sample.nodes():
            if i in nodes_match:
                continue
            if i in match_g1:
                continue
            if i in match_g2:
                continue
            fb.writelines(str(i) + " " + str(self.tag(nodes_G2, i) + G.order()) + "\n")
        fb.close()
        self.const(G.order() + len(nodes_G2), isdirected, out_graph)
        return G.order() + len(nodes_G2)"""
    def write_ini(self, nums_nodes, G, node_match, dict):
        print(f'node_match is {node_match}')
        print(f'dict is {dict}')
        #将dict写入到txt文件中
        with open('dict.txt','w') as f:
            for key, value in dict.items():
                f.write(str(key))
                f.write(' ')
                f.write(str(value))
                f.write('\n')
        #将匹配节点写入到文件中
        with open('node_match.txt', 'w') as f:
            for i in node_match:
                f.write(str(i))
                f.write('\n')

    def const(self,n, isdirected, input_graph):
        edges = {i: [] for i in range(n)}
        with open(input_graph, 'r') as fin:
            for line in fin:
                u, v = line.split()
                u, v = int(u), int(v)
                edges[u].append(v)
                if isdirected == False:
                    edges[v].append(u)
        print("writing " + 'outdegreelist.txt')
        with open('outdegreelist.txt', 'w') as fout:
            for i in range(n):
                for j in edges[i]:
                    deginv = 1.0 / (len(edges[i]))
                    fout.write(str(i) + " " + str(j) + " " + str(deginv) + "\n")
        print("writing " + 'outdegree.txt')
        with open('outdegree.txt', 'w') as fout:
            for i in range(n):
                fout.write(str(i) + " " + str((len(edges[i]))) + "\n")


    def draw_G(self,G):
        nx.draw(G, with_labels= True)
        plt.show()

    def sample_graph(self, G, s):
        newG = nx.Graph()
        newG.add_edges_from(random.sample(G.edges(),int(len(G.edges()))))
        for edge in newG.edges():
            newG[edge[0]][edge[1]]['weight'] = 1.0
        return newG

    def get_subgraph(self,real_G, nodes = 500):
        graph = real_G
        sub_nodes = []
        print(graph.degree())
        print(f'type(graph.degree()) is {type(graph.degree())}')

        nodes_sort = sorted(graph.degree(), key = lambda x:x[1], reverse=True)

        sub_degree = nodes_sort[:nodes]

        for item in sub_degree:
            sub_nodes.append(item[0])

        G = graph.subgraph(sub_nodes)
        return G

    def load_G(self,file_path, undirected = True):
        G = nx.Graph()
        txt_reader = open(file_path,'r')
        for item in txt_reader:
            item = item.split()
            G.add_edge(int(item[0]), int(item[1]))
            if undirected:
                G.add_edge(int(item[1]), int(item[0]))
        txt_reader.close()
        return G

    def bipartite_matching(self,G1, G2, p=1, q=1, dimensions=128, embedding='DeepWalk'):
        node1, node2, proM = map_prob_maxtrix(G1, G2, p=p, q=q, dimensions=dimensions, embedding=embedding)
        M, N = proM.shape

        # numpy_array = np.array(node1)
        # np.save('node1.txt',numpy_array )
        # numpy_array2 = np.array(node2)
        # np.save('node2.txt',numpy_array2 )

        values = [(i, j, 1 - proM[i][j])
                  for i in range(M)
                  for j in range(N) if proM[i][j] > 1e-2]
        # print("长度："+str(len(values)))
        values_dict = dict(((i, j), v) for i, j, v in values)

        munkres_match = munkres(values)

        matches = []
        for p1, p2 in munkres_match:
            if p1 > len(node1) or p2 > len(node2):
                continue
            else:
                matches.append((int(node1[p1]), int(node2[p2]), 1 - values_dict[(p1, p2)]))
        return matches
        pass

def load_G(file_path, undirected = True):
    G = nx.Graph()
    txt_reader = open(file_path,'r')
    for item in txt_reader:
        item = item.split()
        G.add_edge(int(item[0]), int(item[1]))
        if undirected:
            G.add_edge(int(item[1]), int(item[0]))
    txt_reader.close()
    return G

def main():
    print('this is main')
    file = '../../graph_data/douban/offline/edgelist/combin_offline.edgelist'
    newG = load_G(file)
    print(type(newG))


if __name__ == '__main__':
    main()