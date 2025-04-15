import os
import sys
sys.path.append("..")
import numpy as np
import networkx as nx
import random
import pdb
import numpy as np
from scipy.io import loadmat
from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix

def print_graph_stats(G):
    print('# of nodes: %d, # of edges: %d' % (G.number_of_nodes(),
                                              G.number_of_edges()))


"""
    构建邻接矩阵，传过来的一共有俩参数，一个是G（包括图的节点啊等等），另外一个是Id2idx
"""
def construct_adjacency(G, id2idx, sparse=False, file_path=None):
    idx2id = {v:k for k,v in id2idx.items()} #将idx2idx倒过来，本来是'728':1,现在是1:'728'
    nodes_list = [idx2id[i] for i in range(len(id2idx))] #将节点全部取出来，构成了nodes列表，即V
    edges_list = list(G.edges()) #取G中的边，构成边list，即E
    """
        构建边
            edge：{tuple:2}
        最后的形式是N * 2的形式，即我们看到的：
            0,1
            0,2
            1,1272
            1,451
            1,1357
            1,1880
            2,243
            2,241
            2,896
            2,932
            2,2327
            2,561
            ...
    """
    edges = np.array([[id2idx[edge[0]], id2idx[edge[1]]] for edge in edges_list])
    """
        存储下来
    """
    if file_path:
        np.save(file_path, edges)

    """
        如果是sparse=true，以稀疏矩阵的形式存储，并返回的是scipy
        如果是sparse=false，将图转换为矩阵,矩阵的数值为边的权重;
                    也可以用nx.to_numpy_array(G)，二者等价
    """
    if sparse:
        adj = nx.to_scipy_sparse_matrix(G, nodes_list).tolil() #以稀疏矩阵来代替
    else:
        adj = nx.to_numpy_matrix(G, nodes_list) #不以稀疏矩阵来代替
    """
        此文件是构建邻接矩阵
    """
    return adj


def build_degrees(G, id2idx):
    degrees = np.zeros(len(G.nodes()))
    for node in G.nodes():
        deg = G.degree(node)
        degrees[id2idx[node]] = deg
    return degrees


def build_clustering(G, id2idx):
    cluster = nx.clustering(G)
    # convert clustering from dict with keys are ids to array index-based
    clustering = [0] * len(G.nodes())
    for id, val in cluster.items():
        clustering[id2idx[id]] = val
    return clustering


def get_H(path, source_dataset, target_dataset, train_dict=""):
    if train_dict:
        H = np.zeros((len(target_dataset.G.nodes()), len(source_dataset.G.nodes())))
        #H = np.zeros((1767,1767))
        for k, v in train_dict.items():
            H[v, k] = 0.98
        return H
    if path is None: 
        #H = np.ones((len(target_dataset.G.nodes()), len(source_dataset.G.nodes())))
        H = np.random.rand(len(target_dataset.G.nodes()), len(source_dataset.G.nodes()))
        "随机生成矩阵"
        #H = np.ones((1767,1767))
        H = H*(1/len(source_dataset.G.nodes()))
        #H = H*(1/1767)
        return H
    else:    
        if not os.path.exists(path):
            raise Exception("Path '{}' is not exist".format(path))
        dict_H = loadmat(path)
        H = dict_H['H']
        return H


def get_edges(G, id2idx):
    edges1 = [(id2idx[n1], id2idx[n2]) for n1, n2 in G.edges()]
    edges2 = [(id2idx[n2], id2idx[n1]) for n1, n2 in G.edges()]
    
    edges = edges1 + edges2
    edges = np.array(edges)
    return edges


def load_gt(path, id2idx_src=None, id2idx_trg=None, format='matrix'):    
    if id2idx_src:
        """
            id2idx_src代表的是源id索引号，一共有3906个节点
            id2idx_trg代表的是目标id索引号，一共有1118个节点
        """
        conversion_src = type(list(id2idx_src.keys())[0]) #str
        conversion_trg = type(list(id2idx_trg.keys())[0]) #str
    if format == 'matrix':
        """
            如果是矩阵形式，则代表是SpareTensor的形式，需要给其进行处理
        """
        # Dense
        """
        gt = np.zeros((len(id2idx_src.keys()), len(id2idx_trg.keys())))
        with open(path) as file:
            for line in file:
                src, trg = line.strip().split()                
                gt[id2idx_src[conversion_src(src)], id2idx_trg[conversion_trg(trg)]] = 1
        return gt
        """
        # Sparse
        row = []
        col = []
        val = []
        with open(path) as file:
            for line in file:
                src, trg = line.strip().split()
                row.append(id2idx_src[conversion_src(src)])
                col.append(id2idx_trg[conversion_trg(trg)])
                val.append(1)
        gt = csr_matrix((val, (row, col)), shape=(len(id2idx_src), len(id2idx_trg)))
    else:
        gt = {} #真实Ground_truth的一个列表
        with open(path) as file: #打开文件
            for line in file: #按行读，并处理
                src, trg = line.strip().split()
                # print(src, trg)
                if id2idx_src:
                    gt[id2idx_src[conversion_src(src)]] = id2idx_trg[conversion_trg(trg)] #将对应的索引号进行对应
                else:
                    gt[str(src)] = str(trg)


    '''with open(r'F:\Clo_Align\GCNA-master(zhu)\allmovie_tmdb.txt', 'w') as f:
        for key, value in gt.items():
            f.write(str(key))
            f.write(' ')
            f.write(str(value))
            f.write('\n')'''

    """
        ground_truth存储的是两个图当中的节点索引号
    """
    return gt

