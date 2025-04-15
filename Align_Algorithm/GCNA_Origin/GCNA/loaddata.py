# 作者：York
# 时间：2022/6/24 15:52
from tkinter import _flatten

import torch
import networkx as nx
import scipy.sparse as sp

import json
import os
from scipy.io import loadmat
import numpy as np
from networkx.readwrite import json_graph
import utils.graph_utils as graph_utils


class Dataset:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self._load_id2idx()
        self._load_G() #用nx来创建图，并获取里面的节点数和边数
        self._load_features()
        #graph_utils.construct_adjacency(self.G, self.id2idx, sparse=False, file_path=self.data_dir + "/edges.edgelist")
        print("Dataset info:")
        print("- Nodes: ", len(self.G.nodes()))
        print("- Edges: ", len(self.G.edges()))

    def _load_G(self):
        G_data = np.genfromtxt(self.data_dir + 'edge.txt', dtype=np.str_)
        G_feat = np.genfromtxt(self.data_dir + 'feat.txt', dtype=np.str_)
        X = []
        self.G = nx.Graph()
        #self.G.add_nodes_from(str(x) for x in range(len(G_feat)))
        self.G.add_edges_from(G_data) #构建图




    def _load_id2idx(self):
        id2idx_file = self.data_dir + 'id2idx.json'
        self.id2idx = json.load(open(id2idx_file))
        self.idx2id = {v:k for k,v in self.id2idx.items()}


    def _load_features(self):
        self.features = None
        feats_path = self.data_dir + 'feat.txt'
        if os.path.isfile(feats_path):
            self.features = np.loadtxt(feats_path, dtype=np.int32)
        else:
            self.features = None
        '''self.features = np.identity(10312)'''
        return self.features


    def load_edge_features(self):
        self.edge_features= None
        feats_path = os.path.join(self.data_dir, 'edge_feats.mat')
        if os.path.isfile(feats_path):
            edge_feats = loadmat(feats_path)['edge_feats']
            self.edge_features = np.zeros((len(edge_feats[0]),
                                           len(self.G.nodes()),
                                           len(self.G.nodes())))
            for idx, matrix in enumerate(edge_feats[0]):
                self.edge_features[idx] = matrix.toarray()
        else:
            self.edge_features = None
        return self.edge_features

    def normalize(self, mx):
        """Row-normalize sparse matrix"""
        rowsum = np.array(mx.sum(1))
        r_inv = np.power(rowsum, -1).flatten()
        r_inv[np.isinf(r_inv)] = 0.
        r_mat_inv = sp.diags(r_inv)
        mx = r_mat_inv.dot(mx)
        return mx

    def sparse_mx_to_torch_sparse_tensor(self, sparse_mx):
        """Convert a scipy sparse matrix to a torch sparse tensor."""
        sparse_mx = sparse_mx.tocoo().astype(np.float32)
        indices = torch.from_numpy(np.vstack((sparse_mx.row, sparse_mx.col)).astype(np.int64))
        values = torch.from_numpy(sparse_mx.data)
        shape = torch.Size(sparse_mx.shape)
        return torch.sparse.FloatTensor(indices, values, shape)

    def get_adjacency_matrix(self, sparse=False):
        struct_edges = np.genfromtxt(self.data_dir + 'edge.txt', dtype=np.int32)
        sedges = np.array(list(struct_edges), dtype=np.int32).reshape(struct_edges.shape)
        sadj = sp.coo_matrix((np.ones(sedges.shape[0]), (sedges[:, 0], sedges[:, 1])), shape=(self.G.number_of_nodes(), self.G.number_of_nodes()),
                             dtype=np.float32)
        sadj = sadj + sadj.T.multiply(sadj.T > sadj) - sadj.multiply(sadj.T > sadj)
        nsadj = self.normalize(sadj + sp.eye(sadj.shape[0]))

        "最后构建成稀疏矩阵的形式"
        nsadj = self.sparse_mx_to_torch_sparse_tensor(nsadj)

        #return graph_utils.construct_adjacency(self.G, self.id2idx, sparse=False, file_path=self.data_dir + "sssssedges.edgelist")
        return nsadj

    def get_adj_non_spase(self):
        struct_edges = np.genfromtxt(self.data_dir + 'edge.txt', dtype=np.int32)
        sedges = np.array(list(struct_edges), dtype=np.int32).reshape(struct_edges.shape)
        sadj = sp.coo_matrix((np.ones(sedges.shape[0]), (sedges[:, 0], sedges[:, 1])), shape=(self.G.number_of_nodes(), self.G.number_of_nodes()),
                             dtype=np.float32)
        sadj = sadj + sadj.T.multiply(sadj.T > sadj) - sadj.multiply(sadj.T > sadj)
        nsadj = self.normalize(sadj + sp.eye(sadj.shape[0]))
        return nsadj

    def get_nodes_degrees(self):
        return graph_utils.build_degrees(self.G, self.id2idx)

    def get_nodes_clustering(self):
        return graph_utils.build_clustering(self.G, self.id2idx)

    def get_edges(self):

        return np.genfromtxt(self.data_dir + 'edge.txt', dtype=np.int32)



def chuli_id2idx(dataset_names, st, samping):
    dataset_name = ''.join([x for x in dataset_names if x.isalpha()])
    print(fr'dataset is {dataset_name}')
    #address = './graph_data/data/' + dataset_name + '/' + dataset_name + '_' + st + '_edge.txt'
    #address = '/home/pjjiang/PaperCode/Clo_Align/Algorithm/Next/data_syn/attribute_noise/' + dataset_name + '/' + dataset_name + samping + '/' + dataset_name + '_' + st + '_edge.txt'
    #address = '/home/pjjiang/PaperCode/Clo_Align/Algorithm/GCNA-master(zhu)/graph_data/data/' + dataset_names + '/' + dataset_name + '_' + st + '_edge.txt'
    #address = './graph_data/data/' + dataset_name + '_' + st + '_edge.txt'
    address = './graph_data/ppi_dynamic/'+str(samping)+'/' + dataset_name + '_' + st + '_edge.txt'
    print(address)
    if st in ['s']:
        x = np.loadtxt(address, dtype=np.int32)
        x_list = list(x.flatten())
        x = []
        for i in x_list:
            if i not in x:
                x.append(i)

        d = {}
        for i,k in enumerate(x):
            if k not in d.keys():
                d[str(k)] = i

    elif st in ['t']:
        G = nx.Graph()
        x = np.loadtxt(address, dtype=int)
        G.add_edges_from(x)
        '''node_list = list(G.nodes)
        node_list = [int(x) for x in node_list]
        node_list = list(set(node_list))
        n = sorted(list(set(range(node_list[0], node_list[-1] + 1)) - set(node_list)))
        for i in range(node_list[::-1][0] + 1, 1741):
            n.append(i)

        for i in n:
            G.add_edge(i, i)'''
        # print(x_list)
        x_list = list(G.edges)
        x_list = list(_flatten(x_list))
        x = []
        for i in x_list:
            if i not in x:
                x.append(i)

        d = {}
        for i, k in enumerate(x):
            if k not in d.keys():
                d[str(k)] = i

    #with open('./graph_data/data/' + dataset_name + '/' + dataset_name + '_' + st + '_id2idx.json', 'w') as f:
    with open('D:/下载/论文/源码/GCNA-master(zhu)/' + str(samping) + '/' + dataset_name + '_' + st + '_id2idx.json', 'w') as f:
    #with open('./graph_data/data/' + dataset_name + '_' + st + '_id2idx.json', 'w') as f:
        f.write(json.dumps(d))

def loaddata(dataset_name, st, samping):
    #address = './graph_data/data/' + dataset_name + '/' + dataset_name + '_' + st + '_' 豆瓣数据集
    #address = './graph_data/data/' + dataset_name + '_' + st + '_' ppi数据集
    #address = '/home/pjjiang/PaperCode/Clo_Align/Algorithm/Next/data_syn/attribute_noise/' + dataset_name + '/' + dataset_name + samping +'/' + dataset_name + '_' + st + '_'
    dataset_name = ''.join([x for x in dataset_name if x.isalpha()])
    print(fr'dataset is {dataset_name}')
    if dataset_name == 'ppi':
        address = './graph_data/data/' + dataset_name + '_' + st + '_'
    elif dataset_name == 'douban':
        address = './graph_data/data/' + dataset_name + '/' + dataset_name + '_' + st + '_'
    if st in ['s']:
        _dataset = Dataset(address)
    elif st in ['t']:
        _dataset = Dataset(address)

    return _dataset



def loadgroundtruth(dataset_names, samping):
    dataset_name = ''.join([x for x in dataset_names if x.isalpha()])
    #ground_truth = np.genfromtxt('./graph_data/data/' + dataset_name + '/' + dataset_name + '_ground_True.txt', dtype=np.int32) 豆瓣用
    #ground_truth = np.genfromtxt('/home/pjjiang/PaperCode/Clo_Align/Algorithm/Next/data_syn/attribute_noise/' + dataset_name + '/' + dataset_name + samping +'/' + dataset_name + '_ground_True.txt', dtype=np.int32)
    #ground_truth = np.genfromtxt('graph_data/data/' + '/' + dataset_name + '_ground_True.txt', dtype=np.int32) ppi数据集
    if dataset_names == 'ppi':
        ground_truth = np.genfromtxt('graph_data/data/' + '/' + dataset_name + '_ground_True.txt', dtype=np.int32)
    elif dataset_names == 'douban':
        ground_truth = np.genfromtxt('./graph_data/data/' + dataset_name + '/' + dataset_name + '_ground_True.txt', dtype=np.int32)
    ground_truth = list(ground_truth)
    full_di = dict(ground_truth)
    return full_di

def chuli(dataset_name, st):
    address = './graph_data/data/' + dataset_name + '_' + st + '_'
    G_data = np.genfromtxt(address + 'edge.txt', dtype=np.int)
    G = nx.Graph()
    G.add_edges_from(G_data)
    nodes = sorted(list(G.nodes))
    non = [i for i in range(1767)]
    diff = np.setdiff1d(non, nodes)
    print(diff)


if __name__ == '__main__':
    chuli_id2idx('ppi','t', '0.9')
    print("id2idx done")

