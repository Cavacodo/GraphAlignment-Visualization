# 作者：York
# 时间：2022/4/28 11:57
import torch.nn as nn
import torch
import torch.nn.functional as F

import torch.nn as nn
import torch.nn.functional as F
from algorithms.CloAlign.convolution import GraphConvolution


class GCN(nn.Module):
    def __init__(self, nfeat, nhid, nclass, dropout):
        super(GCN, self).__init__()
        #构建第一层GCN，第一个参数是初始特征，第二个参数是隐藏层特征
        self.gc1 = GraphConvolution(nfeat, nhid)
        #构建第二层GCN，传入的nhid维度是16维，输出的nclass与最后要判定的类别数是一致的，是7个类别
        self.gc2 = GraphConvolution(nhid, nclass)
        self.dropout = dropout

    def forward(self, x, adj):
        adj = torch.Tensor(adj)
        x = F.relu(self.gc1(x, adj))
        x = F.dropout(x, self.dropout, training=self.training)
        #完成第一层GCN训练之后，x.shape是2708*16维的。16是hidden layer的维度，16是传参传进去的
        x = self.gc2(x, adj)
        return F.log_softmax(x, dim=1)


def main():
    a = torch.randn(2015,128)
    x = GCN(2015,128)
    y = x(a)
    print(y)
    print(y.shape)

if __name__ == '__main__':
    main()