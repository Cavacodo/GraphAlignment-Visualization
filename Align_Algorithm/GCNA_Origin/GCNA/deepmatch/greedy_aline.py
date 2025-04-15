import numpy as np
import scipy.io as sio
import sklearn.metrics.pairwise
from scipy.sparse import csr_matrix, coo_matrix
from sklearn.neighbors import KDTree
import scipy.sparse as sp
from scipy.spatial.distance import cosine
from sklearn.neighbors import KDTree

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


def kd_align(emb1, emb2, normalize=False, distance_metric="euclidean", num_top=50):
    kd_tree = KDTree(emb2, metric=distance_metric)

    row = np.array([])
    col = np.array([])
    data = np.array([])

    dist, ind = kd_tree.query(emb1, k=num_top)
    print("queried alignments")
    row = np.array([])
    for i in range(emb1.shape[0]):
        row = np.concatenate((row, np.ones(num_top) * i))
    col = ind.flatten()
    data = np.exp(-dist).flatten()
    sparse_align_matrix = coo_matrix((data, (row, col)), shape=(emb1.shape[0], emb2.shape[0]))
    return sparse_align_matrix.tocsr()

if __name__ == "__main__":

    emb=np.loadtxt("blo1.emb")


    list1=[]
    list2=[]
    with open('aline_true.txt', 'r') as fin:
        for line in fin:
            u, v = line.split()
            u, v = int(u), int(v)
            list1.append(u)
            list2.append(v)
    emb1=emb[list1]
    emb2=emb[list2]
    print(emb1.shape[0])
    print(emb2.shape[0])

    alignment_matrix = kd_align(emb1, emb2, distance_metric="euclidean", num_top=1)
    topk_scores = [1]  # ,5,10,20,50]
    for k in topk_scores:
        #score, correct_nodes = score_alignment_matrix(alignment_matrix, topk=k, true_alignments=None)
        score =score_alignment_matrix(alignment_matrix,topk=k)
        print("score top%d: %f" % (k, score))
