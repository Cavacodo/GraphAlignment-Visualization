from algorithms.network_alignment_model import NetworkAlignmentModel
from evaluation.metrics import get_statistics
from algorithms.GCNA.embedding_model import GCNA as Multi_Order, StableFactor
from input.dataset import Dataset
from utils.graph_utils import load_gt
import torch.nn.functional as F
import torch.nn as nn
from algorithms.GCNA.utils import *
from algorithms.GCNA.losses import *

import torch
import numpy as np
import networkx as nx
import random 
import numpy as np

import argparse
import os
import time
import sys

from torch.autograd import Variable
from tqdm import tqdm


"""
    与之前最大的不同是将Source graph与target graph嵌入到同一个GCN中
"""
class GCNA(NetworkAlignmentModel):
    """
    GCNA model for networks alignment task
    """
    def __init__(self, source_dataset, target_dataset, args, groundtruth):
        """
        :params source_dataset: source graph
        :params target_dataset: target graph
        :params args: more config params
        """
        super(GCNA, self).__init__(source_dataset, target_dataset)
        self.source_dataset = source_dataset  #对于豆瓣而言，source有3906个node，8164个edge
        self.target_dataset = target_dataset  #对于豆瓣而言，target有1118个node，1511个edges
        self.alphas = [args.alpha0, args.alpha1, args.alpha2] #三个超参数，都为1
        self.args = args
        #self.full_dict = load_gt(args.groundtruth, source_dataset.id2idx, target_dataset.id2idx, 'dict') #装在ground_truth
        self.full_dict = groundtruth #装在ground_truth


    """
        图增强，即论文里面写的数据增强功能。
            在原始图上面增加一点噪声，这类形式移除边，也可以增加边，里面都有
    """
    def graph_augmentation(self, dataset, type_aug='remove_edges'):
        """
        Generate small noisy graph from original graph
        :params dataset: original graph
        :params type_aug: type of noise added for generating new graph
        """
        edges = dataset.get_edges() #获取边，形式是n * 2的格式
        #adj = dataset.get_adjacency_matrix() #获取邻接矩阵 matrix:(3906,3906)
        adj = dataset.get_adj_non_spase() #获取邻接矩阵 matrix:(3906,3906)
        adj = adj.todense()
        if type_aug == "remove_edges":
            num_edges = len(edges) # num_edges = 16328
            num_remove = int(len(edges) * self.args.noise_level)
            index_to_remove = np.random.choice(np.arange(num_edges), num_remove, replace=False)
            edges_to_remove = edges[index_to_remove]
            for i in range(len(edges_to_remove)):
                adj[edges_to_remove[i, 0], edges_to_remove[i, 1]] = 0
                adj[edges_to_remove[i, 1], edges_to_remove[i, 0]] = 0
        elif type_aug == "add_edges":
            num_edges = len(edges)
            num_add = int(len(edges) * self.args.noise_level)
            count_add = 0
            while count_add < num_add:
                random_index = np.random.randint(0, adj.shape[1], 2)
                if adj[random_index[0], random_index[1]] == 0:
                    adj[random_index[0], random_index[1]] = 1
                    adj[random_index[1], random_index[0]] = 1
                    count_add += 1
        elif type_aug == "change_feats":
            feats = np.copy(dataset.features)
            num_nodes = adj.shape[0]
            num_nodes_change_feats = int(num_nodes * self.args.noise_level)
            node_to_change_feats = np.random.choice(np.arange(0, adj.shape[0]), num_nodes_change_feats, replace=False)
            for node in node_to_change_feats:
                feat_node = feats[node]
                feat_node[feat_node == 1] = 0
                feat_node[np.random.randint(0, feats.shape[1], 1)[0]] = 1
            feats = torch.FloatTensor(feats)
            if self.args.cuda:
                feats = feats.cuda()
            return feats
        new_adj_H, _ = Laplacian_graph(adj)
        if self.args.cuda:
            new_adj_H = new_adj_H.cuda()
        return new_adj_H




    def align(self):
        """
        The main function of GCNA
        """
        """
            把A_hat、特征都获取到
        """
        source_A_hat, target_A_hat, source_feats, target_feats = self.get_elements()
        print("Running Multi-level embedding") #底下是进行多层embedding
        GCNA = self.multi_level_embed(source_A_hat, target_A_hat, source_feats, target_feats) #输入的是归一化的邻接矩阵
        print("Running Refinement Alignment")
        S_GAlign = self.refinement_alignment(GCNA, source_A_hat, target_A_hat)
        return S_GAlign


    def multi_level_embed(self, source_A_hat, target_A_hat, source_feats, target_feats):
        """
        Input: SourceGraph and TargetGraph
        Output: Embedding of those graphs using Multi_order_embedding model
        """

        """
            初始化完了以后就返回，得到GAlign为：
            GCNA(
                (GCNs): ModuleList(
                    (0): GNN(
                      (activate_function): Tanh()
                      (linear): Linear(in_features=538, out_features=128, bias=False)
                        )
                    (1): GNN(
                      (activate_function): Tanh()
                      (linear): Linear(in_features=128, out_features=128, bias=False)
                        )
                    )
                )
        """
        GCNA = Multi_Order( # 这个是Embedding_model里面的 GCNA 只不过是换了一个名字
            activate_function = self.args.act, # tanh
            num_GCN_blocks = self.args.num_GCN_blocks, #层数2
            input_dim = self.args.input_dim, #输入维度100
            output_dim = self.args.embedding_dim, #嵌入维度128
            num_source_nodes = len(source_A_hat), #3906
            num_target_nodes = len(target_A_hat), #1118
            source_feats = source_feats, #source 特征
            target_feats = target_feats # target 特征
        )

        if self.args.cuda:
            GCNA = GCNA.cuda()

        "构建优化器"
        """
            构建方法使用的是lambda与filter结合的形式，目的是从GCNA参数列表中构建出可以进行梯度更新的tensor
        """
        structural_optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, GCNA.parameters()), lr=self.args.lr)

        blank = ' '
        print('-----------------------------------------------')
        print('|   weight name   |        weight shape       |')
        print('-----------------------------------------------')

        for index, (key, w_variable) in enumerate(GCNA.named_parameters()):
            if len(key) <= 15: key = key + (15 - len(key)) * blank
            w_variable_blank = ''
            if len(w_variable.shape) == 1:
                if w_variable.shape[0] >= 100:
                    w_variable_blank = 8 * blank
                else:
                    w_variable_blank = 9 * blank
            elif len(w_variable.shape) == 2:
                if w_variable.shape[0] >= 100:
                    w_variable_blank = 2 * blank
                else:
                    w_variable_blank = 3 * blank

            print('| {} | {}{} |'.format(key, w_variable.shape, w_variable_blank))
            key = 0
        print('-----------------------------------------------')


        new_source_A_hats = []
        new_target_A_hats = []
        new_source_A_hats.append(self.graph_augmentation(self.source_dataset, 'remove_edges'))
        new_source_A_hats.append(self.graph_augmentation(self.source_dataset, 'add_edges'))
        new_source_A_hats.append(source_A_hat)
        new_source_feats = self.graph_augmentation(self.source_dataset, 'change_feats')

        new_target_A_hats.append(self.graph_augmentation(self.target_dataset, 'remove_edges'))
        new_target_A_hats.append(self.graph_augmentation(self.target_dataset, 'add_edges'))
        new_target_A_hats.append(target_A_hat)
        new_target_feats = self.graph_augmentation(self.target_dataset, 'change_feats')


        """
            真正开始迭代运行的
        """
        for epoch in range(self.args.GCNA_epochs):
            if self.args.log:
                print("Structure learning epoch: {}".format(epoch))
            for i in range(2): #代表原图和目标图
                for j in range(len(new_source_A_hats)): #代表添加进去的三个图，分别进行循环
                    structural_optimizer.zero_grad()
                    """
                        如果i=0，代表的是源图（3906），否则是目标图（1118）
                    """
                    if i == 0:
                        A_hat = source_A_hat
                        augment_A_hat = new_source_A_hats[j]
                        " outputs对应三层，分别是论文中的theta0 theta1 theta2 "

                        outputs = GCNA(torch.tensor(source_A_hat, dtype=torch.float), 's') #s代表source ；这才是真正的运行，之前都是初始化，这个是直接执行forward函数
                        if j < 3: #这代表的是三个噪声图训练
                            """
                                在这里要注意逻辑，训练完后返回到的是consistency_loss那一行！！！
                                而不是等三行都运行完了再到底下去，循环别看错了
                            """
                            augment_outputs = GCNA(augment_A_hat, 's')
                        else:
                            #augment_outputs = GCNA(augment_A_hat, 's', new_source_feats)
                            pass
                    else:
                        A_hat = target_A_hat
                        augment_A_hat = new_target_A_hats[j]
                        outputs = GCNA(target_A_hat, 't')
                        if j < 3:
                            augment_outputs = GCNA(augment_A_hat, 't')
                        else:
                            #augment_outputs = GCNA(augment_A_hat, 't', new_target_feats)
                            pass
                    """
                        计算损失
                    """
                    " 这个计算的是原图的嵌入和真实之间的损失 "
                    consistency_loss = self.linkpred_loss(outputs[-1], A_hat) #计算损失，输出跟真实的之间的误差
                    " 这个计算的是增强图的嵌入和真实之间的损失 "
                    augment_consistency_loss = self.linkpred_loss(augment_outputs[-1], augment_A_hat)
                    " consistency_loss构成 "
                    consistency_loss = self.args.beta * consistency_loss + (1-self.args.beta) * augment_consistency_loss


                    diff = torch.abs(outputs[-1] - augment_outputs[-1]) #转成绝对值
                    """
                        直观来说。源网络应该与目标网络及其扰动版本对齐，反之也是，
                        这有助于对齐对consistency violations具有鲁棒性（R2）。
                        为此设计了一种噪声自适应损失函数，使网络节点在扰动前后的多阶特征差异最小。
                        
                        这是pytorch里面tensor的一个操作,diff[diff < self.args.threshold] ** 2) 就是选择
                            diff里面小于阈值（在这里一开始设置为0.01）的项取出来。
                    """
                    noise_adaptivity_loss = (diff[diff < self.args.threshold] ** 2).sum() / len(outputs)

                    " 最终将两个损失结合 "
                    loss = self.args.coe_consistency * consistency_loss + (1 - self.args.coe_consistency) * noise_adaptivity_loss
                    if self.args.log:
                        print("Loss: {:.4f}".format(loss.data))
                    loss.backward()
                    structural_optimizer.step()
        GCNA.eval()
        return GCNA


    """
        论文中的Alignment Refinement部分
    """
    def refinement_alignment(self, GCNA, source_A_hat, target_A_hat):
        source_A_hat = source_A_hat.to_dense() #将稀疏矩阵换做稠密矩阵
        target_A_hat = target_A_hat.to_dense()
        #source_A_hat = torch.tensor(source_A_hat)
        #target_A_hat = torch.tensor(target_A_hat)
        GCNA_S = self.refine(GCNA, source_A_hat, target_A_hat, 0.94)
        return GCNA_S


    def get_elements(self):
        """
        Compute Normalized Laplacian matrix
        Preprocessing nodes attribute
        """
        """
            构建source和target的A_hat。
                首先调用source_dataset.get_adjacency_matrix()构建邻接矩阵
                然后再构建拉普拉斯矩阵
        """
        #source_A_hat, _ = Laplacian_graph(self.source_dataset.get_adjacency_matrix())
        #source_A_hat = self.source_dataset.get_adjacency_matrix()
        source_A_hat = self.source_dataset.get_adj_non_spase()
        source_A_hat = source_A_hat.todense()
        #target_A_hat, _ = Laplacian_graph(self.target_dataset.get_adjacency_matrix())
        #target_A_hat = self.target_dataset.get_adjacency_matrix()
        target_A_hat = self.target_dataset.get_adj_non_spase()
        target_A_hat = target_A_hat.todense()
        """
            如果是GPU
        """
        if self.args.cuda:
            source_A_hat = np.asarray(source_A_hat)
            target_A_hat = np.asarray(target_A_hat)
            source_A_hat = torch.from_numpy(source_A_hat).cuda()
            target_A_hat = torch.from_numpy(target_A_hat).cuda()

            # source_A_hat = source_A_hat.cuda()
            # target_A_hat = target_A_hat.cuda()
        """
            属性特征
        """
        source_feats = self.source_dataset.features #大小为3906 * 538
        target_feats = self.target_dataset.features #大小为1118 * 538

        if source_feats is None:
            source_feats = np.zeros((len(self.source_dataset.G.nodes()), 1))
            target_feats = np.zeros((len(self.target_dataset.G.nodes()), 1))

        """
            底下这个是什么操作？！
        """
        for i in range(len(source_feats)): #3906
            if source_feats[i].sum() == 0:
                source_feats[i, -1] = 1
        for i in range(len(target_feats)):
            if target_feats[i].sum() == 0:
                target_feats[i, -1] = 1


        if source_feats is not None:
            source_feats = torch.FloatTensor(source_feats) #转成float
            target_feats = torch.FloatTensor(target_feats)
            if self.args.cuda:
                source_feats = source_feats.cuda()
                target_feats = target_feats.cuda()
        """
        torch.nn.functional.normalize(input, p=2, dim=1, eps=1e-12, out=None)
            对指定维度进行L2_norm的计算，即P范数计算（不指定默认为2），对输入数据进行标准化使得输入数据满足正态分布
        """
        source_feats = F.normalize(source_feats)
        target_feats = F.normalize(target_feats)
        return source_A_hat, target_A_hat, source_feats, target_feats


    """
        计算损失
    """
    def linkpred_loss(self, embedding, A):
        """
        :param embedding: H^(l)
        :param A: A_hat
        :return:
        """
        " 计算公式中的   H^(l) * H^(l)^T "
        pred_adj = torch.matmul(F.normalize(embedding), F.normalize(embedding).t())
        if self.args.cuda:
            pred_adj = F.normalize((torch.min(pred_adj, torch.Tensor([1]).cuda())), dim = 1)
        else:
            """
                torch.min(pred_adj, torch.Tensor([1])) 找到其中的最小值 
                例子：
                        a = torch.Tensor([1,2,3,4,5,6])
                        b= torch.Tensor([1])
                        torch.min(a,b)
                    输出：tensor([1., 1., 1., 1., 1., 1.])
            """
            pred_adj = F.normalize((torch.min(pred_adj, torch.Tensor([1]))), dim = 1) #按照行来进行归一化
        #linkpred_losss = (pred_adj - A[index]) ** 2
        " 范数计算 "
        linkpred_losss = (pred_adj.detach() - A) ** 2
        linkpred_losss = linkpred_losss.sum() / A.shape[1]
        return linkpred_losss


    """
        下面是迭代优化对齐矩阵的算法过程
    
    """
    def refine(self, GCNA, source_A_hat, target_A_hat, threshold):
        refinement_model = StableFactor(len(source_A_hat), len(target_A_hat), self.args.cuda)
        if self.args.cuda: 
            refinement_model = refinement_model.cuda()
        S_max = None
        source_outputs = GCNA(refinement_model(source_A_hat, 's'), 's')
        target_outputs = GCNA(refinement_model(target_A_hat, 't'), 't')
        acc, S = get_acc(source_outputs, target_outputs, self.full_dict, self.alphas, just_S=True)#初始化对齐矩阵
        score = np.max(S, axis=1).mean()#初始化得分
        acc_max = 0
        alpha_source_max = None
        alpha_target_max = None
        if 1:
        #if score > refinement_model.score_max:
            refinement_model.score_max = score
            alpha_source_max = refinement_model.alpha_source
            alpha_target_max = refinement_model.alpha_target
            acc_max = acc
            S_max = S
        print("Acc: {}, score: {:.4f}".format(acc, score))
        source_candidates, target_candidates = [], []            
        alpha_source_max = refinement_model.alpha_source + 0
        alpha_target_max = refinement_model.alpha_target + 0

        """
            初始化完了，下面是迭代过程
        """
        for epoch in range(self.args.refinement_epochs):
            if self.args.log:
                print("Refinement epoch: {}".format(epoch))
            source_candidates, target_candidates, len_source_candidates, count_true_candidates = self.get_candidate(source_outputs, target_outputs, threshold)

            refinement_model.alpha_source[source_candidates] *= 1.1##乘以影响因子1.1
            refinement_model.alpha_target[target_candidates] *= 1.1
            source_outputs = GCNA(refinement_model(source_A_hat, 's'), 's')##重新获得节点的嵌入表示，这是源图的，下面是目标图的
            target_outputs = GCNA(refinement_model(target_A_hat, 't'), 't')
            acc, S = get_acc(source_outputs, target_outputs, self.full_dict, self.alphas, just_S=True)
            score = np.max(S, axis=1).mean()
            if score > refinement_model.score_max:##迭代
                refinement_model.score_max = score
                alpha_source_max = refinement_model.alpha_source + 0
                alpha_target_max = refinement_model.alpha_target + 0
                acc_max = acc
                S_max = S
            if self.args.log:
                print("Acc: {}, score: {:.4f}, score_max {:.4f}".format(acc, score, refinement_model.score_max))
            if epoch == self.args.refinement_epochs - 1:
                print("Numcandidate: {}, num_true_candidate: {}".format(len_source_candidates, count_true_candidates))
        print("refinement done!")
        print("Acc with best score: {:.4f} is : {}".format(refinement_model.score_max, acc_max))
        refinement_model.alpha_source = alpha_source_max
        refinement_model.alpha_target = alpha_target_max
        self.GCNA_S = S_max
        # self.log_and_evaluate(GCNA, refinement_model, source_A_hat, target_A_hat)
        return self.GCNA_S


    def get_similarity_matrices(self, source_outputs, target_outputs):
        """
        Construct Similarity matrix in each layer
        :params source_outputs: List of embedding at each layer of source graph
        :params target_outputs: List of embedding at each layer of target graph
        """
        list_S = []
        for i in range(len(source_outputs)):
            source_output_i = source_outputs[i]
            target_output_i = target_outputs[i]
            S = torch.mm(F.normalize(source_output_i), F.normalize(target_output_i).t())
            list_S.append(S)
        return list_S


    def log_and_evaluate(self, embedding_model, refinement_model, source_A_hat, target_A_hat):
        embedding_model.eval()
        source_outputs = embedding_model(refinement_model(source_A_hat, 's'), 's')
        target_outputs = embedding_model(refinement_model(target_A_hat, 't'), 't')
        print("-"* 100)
        log, self.S = get_acc(source_outputs, target_outputs, self.full_dict, self.alphas)
        print(self.alphas)
        print(log)
        return source_outputs, target_outputs
    

    def get_candidate(self, source_outputs, target_outputs, threshold):
        List_S = self.get_similarity_matrices(source_outputs, target_outputs)[1:]
        source_candidates = []
        target_candidates = []
        count_true_candidates = 0
        if len(List_S) < 2:
            print("The current model doesn't support refinement for number of GNN layer smaller than 2")
            return torch.LongTensor(source_candidates), torch.LongTensor(target_candidates)

        num_source_nodes = len(self.source_dataset.G.nodes())
        num_target_nodes = len(self.target_dataset.G.nodes())
        for i in range(min(num_source_nodes, num_target_nodes)):
            node_i_is_stable = True
            for j in range(len(List_S)):
                if List_S[j][i].argmax() != List_S[j-1][i].argmax() or List_S[j][i].max() < threshold:
                    node_i_is_stable = False 
                    break
            if node_i_is_stable:
                tg_candi = List_S[-1][i].argmax()
                source_candidates.append(i)
                target_candidates.append(tg_candi)
                try:
                    if self.full_dict[i] == tg_candi:
                        count_true_candidates += 1
                except:
                    continue
        return torch.LongTensor(source_candidates), torch.LongTensor(target_candidates), len(source_candidates), count_true_candidates
