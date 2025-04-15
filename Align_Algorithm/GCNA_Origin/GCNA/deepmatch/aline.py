import numpy as np
import scipy.io as sio
import sklearn.metrics.pairwise
import torch
from scipy.sparse import csr_matrix, coo_matrix
from sklearn.neighbors import KDTree
import scipy.sparse as sp
from scipy.spatial.distance import cosine
from sklearn.neighbors import KDTree
from sklearn.neighbors import BallTree
from sklearn.metrics.pairwise import pairwise_distances_argmin_min

import time

def get_embedding_similarities(embed, embed2=None, sim_measure="euclidean", num_top=None):
    n_nodes, dim = embed.shape
    if embed2 is None:
        embed2 = embed

    if num_top is not None:  # KD tree with only top similarities computed

        kd_sim = kd_align(embed, embed2, distance_metric=sim_measure, num_top=num_top)
        return kd_sim

    # All pairwise distance computation
    if sim_measure == "cosine":
        similarity_matrix = sklearn.metrics.pairwise.cosine_similarity(embed, embed2)
    else:  # 走这里

        similarity_matrix = sklearn.metrics.pairwise.euclidean_distances(embed, embed2)
        similarity_matrix = np.exp(-similarity_matrix)

    return similarity_matrix

def score_alignment_matrix3(alignment_matrix):


    sorted_indices = np.argsort(alignment_matrix)
    alignment_score=0
    for node_index in range(500):
        node1 = np.load("data/wiki_new/node1.txt.npy")
        node2 = np.load("data/wiki_new/node2.txt.npy")
        node_sorted_indices = sorted_indices[node_index]


        # if(node1[node_index]==node2[node_sorted_indices[-1]] or node1[node_index]==node2[node_sorted_indices[-2]] or node1[node_index]==node2[node_sorted_indices[-3]]):
        #     alignment_score += 1
        if (node1[node_index] == node2[node_sorted_indices[-1]] or node1[node_index] == node2[node_sorted_indices[-2]] or node1[node_index] == node2[node_sorted_indices[-3]]):
            alignment_score += 1
    alignment_score /= float(500)
    return alignment_score
def score_alignment_matrix2(alignment_matrix):



    sorted_indices = np.argsort(alignment_matrix)
    alignment_score=0
    for node_index in range(4277):
        node_sorted_indices = sorted_indices[node_index]
        if(aline[node_index]==node_sorted_indices[-1] or aline[node_index]==node_sorted_indices[-2] or aline[node_index]==node_sorted_indices[-3]):
            alignment_score += 1

    alignment_score /= float(500)
    return alignment_score


def score_alignment_matrix(alignment_matrix, topk=None, topk_score_weighted=False, true_alignments=None):
    n_nodes = alignment_matrix.shape[0]
    correct_nodes = []

    if topk is None:
        row_sums = alignment_matrix.sum(axis=1)
        row_sums[row_sums == 0] = 1e-6  # shouldn't affect much since dividing 0 by anything is 0
        alignment_matrix = alignment_matrix / row_sums[:, np.newaxis]  # normalize

        alignment_score = score(alignment_matrix, true_alignments=true_alignments)
    else:
        alignment_score = 0
        if not sp.issparse(alignment_matrix):  # 走这里
            sorted_indices = np.argsort(alignment_matrix)  # 根据值从小到大输出索引
            #print(sorted_indices)
        for node_index in range(n_nodes):

            target_alignment = node_index  # default: assume identity mapping, and the node should be aligned to itself

            #target_alignment = int(true_alignments[node_index])
            target_alignment = int(node_index)
            if sp.issparse(alignment_matrix):
                row, possible_alignments, possible_values = sp.find(alignment_matrix[node_index])
                node_sorted_indices = possible_alignments[possible_values.argsort()]
            else:
                node_sorted_indices = sorted_indices[node_index]
            if target_alignment in node_sorted_indices[-topk:]:
                if topk_score_weighted:
                    alignment_score += 1.0 / (n_nodes - np.argwhere(sorted_indices[node_index] == target_alignment)[0])
                else:
                    alignment_score += 1
                correct_nodes.append(node_index)
        alignment_score /= float(n_nodes)

    return alignment_score

def score_alignment_matrix1(alignment_matrix, topk=None, topk_score_weighted=False, true_alignments=None):
    n_nodes = alignment_matrix.shape[0]
    alignment_score = 0
    for node_index in range(n_nodes):

        a=alignment_matrix[node_index][node_index]

        print(a)
        print(type(a))
        if a!=0:
            alignment_score += 1

    alignment_score /= float(n_nodes)


    return alignment_score

def kd_align(emb1, emb2, normalize=False, distance_metric="euclidean", num_top=1):
    before_rep = time.time()


    # kd_tree = KDTree(emb2, metric=distance_metric)
    kd_tree=KDTree(emb2, metric=distance_metric)
    # row = np.array([])
    # col = np.array([])
    # data = np.array([])
    alignment_score = 0
    dist, ind = kd_tree.query(emb1, k=num_top)
    after_rep = time.time()
    print("kd_tree匹配时间 %f seconds" % (after_rep - before_rep))
    for i in range(ind.shape[0]):
        if ind[i][0]==i:
            alignment_score += 1
    alignment_score /= float(ind.shape[0])
    return alignment_score
    # print(ind[1])
    # print(ind[0])
    # print("queried alignments")
    # row = np.array([])
    # for i in range(emb1.shape[0]):
    #     row = np.concatenate((row, np.ones(num_top) * i))
    # col = ind.flatten()
    # data = np.exp(-dist).flatten()
    # sparse_align_matrix = coo_matrix((data, (row, col)), shape=(emb1.shape[0], emb2.shape[0]))
    # return sparse_align_matrix.tocsr()


def run(emb,aline_true):
    emb = np.loadtxt(emb)
    list1 = []
    list2 = []
    with open(aline_true, 'r') as fin:
        for line in fin:
            u, v = line.split()
            u, v = int(u), int(v)
            list1.append(u)
            list2.append(v)
    emb1 = emb[list1]
    emb2 = emb[list2]
    print(emb1.shape[0])
    print(emb2.shape[0])
    # node = np.load("data/wiki_2/list.npy")
    # emb=np.delete(emb,node,0)
    # split_idx = int(emb.shape[0] / 2)
    # emb1 = emb[:split_idx]
    # emb2 = emb[split_idx:]
    # alignment_matrix = get_embedding_similarities(emb1, emb2, num_top=None)
    alignment_matrix = kd_align(emb1, emb2, distance_metric="euclidean", num_top=1)
    topk_scores = [1]  # ,5,10,20,50]
    for k in topk_scores:
        # score, correct_nodes = score_alignment_matrix(alignment_matrix, topk=k, true_alignments=None)
        score = score_alignment_matrix1(alignment_matrix, topk=k)
        # print("score top%d: %f" % (k, score))
    return score

def run_new(emb,aline_true):
    begin=time.time()
    list1 = []
    list2 = []
    ground_truth = [ [] for i in range(2) ]
    with open(aline_true, 'r') as fin:
        for line in fin:
            u, v = line.split()
            u, v = int(u), int(v)
            list1.append(u)
            list2.append(v)
            ground_truth[0].append(u)
            ground_truth[1].append(v)

    ground_truth = np.array(ground_truth)
    ground_truth = torch.from_numpy(ground_truth)
    print(ground_truth)
    emb1 = emb[list1]
    emb2 = emb[list2]
    alignment_score=0
    index,value = pairwise_distances_argmin_min(emb1, emb2,axis=1,metric='euclidean')
    index=list(index)
    for i, element in enumerate(index):
        if i==element:
            alignment_score=alignment_score+1
    # for i in range(len(index)):
    #     if i==index[i]:
    #         alignment_score=alignment_score+1

    after=time.time()
    print("match time is %f" % (after-begin))
    return alignment_score/len(index)
def run_final(emb,aline_true):

    list1 = []
    list2 = []
    with open(aline_true, 'r') as fin:
        for line in fin:
            u, v = line.split()
            u, v = int(u), int(v)
            list1.append(u)
            list2.append(v)
    emb1 = emb[list1]
    emb2 = emb[list2]
    print(emb1.shape[0])
    print(emb2.shape[0])
    # node = np.load("data/wiki_2/list.npy")
    # emb=np.delete(emb,node,0)
    # split_idx = int(emb.shape[0] / 2)
    # emb1 = emb[:split_idx]
    # emb2 = emb[split_idx:]
    # alignment_matrix = get_embedding_similarities(emb1, emb2, num_top=None)
    alignment_score = kd_align(emb1, emb2, distance_metric="euclidean", num_top=1)
    # print(alignment_matrix)
    # topk_scores = [1]  # ,5,10,20,50]
    # for k in topk_scores:
    #     # score, correct_nodes = score_alignment_matrix(alignment_matrix, topk=k, true_alignments=None)
    #     score = score_alignment_matrix1(alignment_matrix, topk=k)
    #     # print("score top%d: %f" % (k, score))

    return alignment_score