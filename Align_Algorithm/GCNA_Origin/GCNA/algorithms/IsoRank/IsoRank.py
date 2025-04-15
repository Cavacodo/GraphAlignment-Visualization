import numpy as np
from numpy import inf, nan
from copy import deepcopy
import argparse
import sys

from evaluation.metrics import get_statistics
from utils import graph_utils

sys.path.append("..")
from algorithms.network_alignment_model import NetworkAlignmentModel
from input.dataset import Dataset
import pdb
from utils.graph_utils import get_H

class IsoRank(NetworkAlignmentModel):

    """
    Description:
      The algorithm computes the alignment/similarity matrix by a random walk
      based method. This algorithm is for non-attributed networks.
    Input:
      - A1, A2: adjacency matrices of two networks
      - H: the prior node similarity matrix, e.g., degree similarity matrix
      - alpha: decay factor, i.e., how important the global topology
               consistency is
      - maxiter: maximum number of iterations
    Output:
      - S: an n2*n1 alignment matrix, entry (x,y) represents to what extend node-
       x in A2 is aligned to node-y in A1
    Reference:
      Singh, Rohit, Jinbo Xu, and Bonnie Berger.
      Global alignment of multiple protein interaction networks with application to functional orthology detection.
      Proceedings of the National Academy of Sciences 105.35 (2008): 12763-12768.
    """

    def __init__(self, source_dataset, target_dataset, H=None, alpha=0.82, maxiter=30, tol=1e-4, train_dict=None):
        self.source_dataset = source_dataset
        self.target_dataset = target_dataset
        self.alignment_matrix = None
        #self.A1 = source_dataset.get_adjacency_matrix()
        self.A1 = source_dataset.get_adj_non_spase()
        #self.A2 = target_dataset.get_adjacency_matrix()
        self.A2 = target_dataset.get_adj_non_spase()

        self.alpha = alpha
        self.maxiter = maxiter
        if train_dict is not None:
            print("This is supervised IsoRank")
        self.H = get_H(H, source_dataset, target_dataset, train_dict)
        self.tol = tol

    def align(self):

        n1 = self.A1.shape[0]
        n2 = self.A2.shape[0]

        # normalize the adjacency matrices
        d1 = 1 / self.A1.sum(axis=1)
        d2 = 1 / self.A2.sum(axis=1)

        d1 = d1.A
        d2 = d2.A
        self.A1 = self.A1.A
        self.A2 = self.A2.A

        d1[d1 == inf] = 0
        d2[d2 == inf] = 0
        d1 = d1.reshape(-1,1)
        d2 = d2.reshape(-1,1)

        W1 = d1*self.A1
        W2 = d2*self.A2
        S = np.ones((n2,n1)) / (n1 * n2) # Map target to source
        # IsoRank Algorithm in matrix form
        for iter in range(1, self.maxiter + 1):
            prev = S.flatten()
            if self.H is not None:
                S = (self.alpha*W2.T).dot(S).dot(W1) + (1-self.alpha) * self.H
            else:
                S = W2.T.dot(S).dot(W1)
            delta = np.linalg.norm(S.flatten()-prev, 2)
            print("Iteration: ", iter, " with delta = ", delta)
            if delta < self.tol:
                break

        self.alignment_matrix = S.T
        return self.alignment_matrix

    def get_alignment_matrix(self):
        if self.alignment_matrix is None:
            raise Exception("Must calculate alignment matrix by calling 'align()' method first")
        return self.alignment_matrix


def parse_args():

    parser = argparse.ArgumentParser(description="IsoRank")
    parser.add_argument('--prefix1',             default="../../graph_data/douban/online/graphsage/")
    parser.add_argument('--prefix2',             default="../../graph_data/douban/offline/graphsage/")
    parser.add_argument('--groundtruth',         default="../../graph_data/douban/dictionaries/groundtruth")
    parser.add_argument('--H',                   default="../../graph_data/douban/H.mat")
    parser.add_argument('--base_log_dir',        default='../../graph_data/IJCAI16_results')
    parser.add_argument('--log_name',            default='pale_facebook')
    parser.add_argument('--max_iter',            default=50, type=int)
    parser.add_argument('--alpha',               default=0.82, type=float)
    parser.add_argument('--tol',                 default=1e-4, type=float)
    parser.add_argument('--k',                   default=1, type=int)

    return parser.parse_args()

"""    for key, value in gt.items():
        ele_key = alignment_matrix[key].argsort()[::-1]
        for i in range(len(ele_key)):
            if ele_key[i] == value:
                if i > k: break
                ra = i + 1 # r1
                MAP += 1/ra
                Hit += 1
                AUC += (alignment_matrix.shape[1] - ra) / (alignment_matrix.shape[1] - 1)
                break
    n_nodes = len(gt)"""
"""    MAP /= n_nodes
    AUC /= n_nodes
    Hit /= n_nodes
    return Hit"""


if __name__ == "__main__":
    args = parse_args()
    print(args)
    source_dataset = Dataset(args.prefix1)
    target_dataset = Dataset(args.prefix2)
    groundtruth = graph_utils.load_gt(args.groundtruth, source_dataset.id2idx, target_dataset.id2idx, 'dict')

    model = IsoRank(source_dataset, target_dataset, args.H, args.alpha, args.max_iter, args.tol)
    S = model.align()

    print("-"*100)
    acc, MAP, top5, top10 = get_statistics(S, groundtruth, use_greedy_match=False, get_all_metric=True)
    print("Accuracy: {:.4f}".format(acc))
    print("MAP: {:.4f}".format(MAP))
    print("Precision_5: {:.4f}".format(top5))
    print("Precision_10: {:.4f}".format(top10))
    print("-"*100)




