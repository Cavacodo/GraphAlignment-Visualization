# 作者：York
# 时间：2022/4/28 17:00
import math

import torch

from torch.nn.parameter import Parameter
from torch.nn.modules.module import Module


class GraphConvolution(Module):
    """
    Simple GNN layer, similar to https://arxiv.org/abs/1609.02907
    """

    def __init__(self, in_features, out_features, bias=True):
        super(GraphConvolution, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = Parameter(torch.FloatTensor(in_features, out_features))
        if bias:
            self.bias = Parameter(torch.FloatTensor(out_features))
        else:
            self.register_parameter('bias', None)
            #Parameter()与register_parameter()都是将一个不可训练的类型Tensor转换成可以训练的类型parameter，并将这个parameter绑定到这个module里面，相当于变成了模型的一部分，成为了模型中可以根据训练进行变化的参数。
        self.reset_parameters()
    #构建好特征之后对特征进行随机初始化的过程
    def reset_parameters(self):
        stdv = 1. / math.sqrt(self.weight.size(1))
        self.weight.data.uniform_(-stdv, stdv)
        if self.bias is not None:
            self.bias.data.uniform_(-stdv, stdv)

    def forward(self, input, adj):
        support = torch.mm(input, self.weight)#将input函数和weight函数做了一个乘积；torch.mm(a, b)是矩阵a和b矩阵相乘
        output = torch.spmm(adj, support)#稀疏矩阵的相乘，是之前归一化之后的结果和上一步相乘
        if self.bias is not None:
            return output + self.bias
        else:
            return output

    def __repr__(self):
        return self.__class__.__name__ + ' (' \
               + str(self.in_features) + ' -> ' \
               + str(self.out_features) + ')'

