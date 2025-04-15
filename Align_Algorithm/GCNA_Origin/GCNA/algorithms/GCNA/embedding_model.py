import torch
import torch.nn as nn

import numpy as np
import torch.nn.functional as F
from torch.nn import init

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def init_weight(modules, activation):
    """
    Weight initialization
    :param modules: Iterable of modules
    :param activation: Activation function.
    """
    for m in modules:
        """
            m = GNN(
                    (activate_function): Tanh()
                    (linear): Linear(in_features=538, out_features=128, bias=False)
                )
        """
        if isinstance(m, nn.Linear): #执行到linear的时候 才会执行以下，激活函数不需要。
            if activation is None:
                """
                    一个服从均匀分布的Glorot初始化器
                """
                m.weight.data = init.xavier_uniform_(m.weight.data) #, gain=nn.init.calculate_gain(activation.lower()))
            else:
                """
                    激活函数不为空，所以执行此
                        nn.init.calculate_gain():返回给定的非线性函数的推荐增益值
                        activation.lower():返回将字符串中所有大写字符转换为小写后生成的字符串。
                """
                m.weight.data = init.xavier_uniform_(m.weight.data, gain=nn.init.calculate_gain(activation.lower()))
            if m.bias is not None:
                m.bias.data = init.constant_(m.bias.data, 0.0)


def get_act_function(activate_function):
    """
    Get activation function by name
    :param activation_fuction: Name of activation function 
    """
    if activate_function == 'sigmoid':
        activate_function = nn.Sigmoid()
    elif activate_function == 'relu':
        activate_function = nn.ReLU()
    elif activate_function == 'tanh':
        activate_function = nn.Tanh()
    else:
        return None
    return activate_function


class CombineModel(nn.Module):
    def __init__(self):
        super(CombineModel, self).__init__()
        self.thetas = nn.Parameter(torch.ones(3))

    
    def loss(self, S1, S2, S3, id2idx_augment):
        S = self.forward(S1, S2, S3)
        S_temp = torch.zeros(S.shape)
        for k,v in id2idx_augment.items():
            S_temp[int(k),v] = 1
        
        S = S / torch.sqrt((S**2).sum(dim=1)).view(S.shape[0],1)
        loss = -(S * S_temp).mean()
        return loss


    def forward(self, S1, S2, S3):
        theta_sum = torch.abs(self.thetas[0]) + torch.abs(self.thetas[1]) + torch.abs(self.thetas[2])
        return (torch.abs(self.thetas[0])/theta_sum) * S1 + (torch.abs(self.thetas[1])/theta_sum) * S2 + (torch.abs(self.thetas[2])/theta_sum) * S3


class Combine2Model(nn.Module):
    def __init__(self):
        super(Combine2Model, self).__init__()
        self.thetas = nn.Parameter(torch.ones(2))


    def loss(self, S1, S2, id2idx_augment):
        S = self.forward(S1, S2)
        S_temp = torch.zeros(S.shape)
        for k,v in id2idx_augment.items():
            S_temp[int(k),v] = 1
        
        S = S / torch.max(S, dim=1)[0].view(S.shape[0],1)
        loss = -(S * S_temp).mean()
        # loss = (S - 3 * torch.eye(len(S))).mean()
        return loss

    def forward(self, S1, S2):
        return torch.abs(self.thetas[0]) * S1 + torch.abs(self.thetas[1]) * S2


class GCN(nn.Module):
    """
    The GNN multistates block
    """
    def __init__(self, activate_function, input_dim, output_dim): # 输入维度538,输出维度200
        """
        activate_function: Tanh
        input_dim: input features dimensions
        output_dim: output features dimensions
        """
        super(GCN, self).__init__()
        """
            若激活函数不为空，则获取激活函数
            若激活函数为空，则不设置激活函数
        """
        if activate_function is not None:
            self.activate_function = get_act_function(activate_function)
        else:
            self.activate_function = None
        self.input_dim = input_dim
        self.output_dim = output_dim

        " 设置一个全连接层 "
        self.linear = nn.Linear(input_dim, output_dim, bias=False)

        " 初始化权重 "
        init_weight(self.modules(), activate_function)

    """
        前向传播
    """
    def forward(self, input, A_hat):
        output = self.linear(input) # 全连接层，只不过是单层的，
        output = torch.matmul(A_hat, output)
        if self.activate_function is not None:
            output = self.activate_function(output)
        return output


class GCNA(nn.Module):
    """
    Training a multilayer GNN model
    """
    def __init__(self, activate_function, num_GCN_blocks, input_dim, output_dim, \
                num_source_nodes, num_target_nodes, source_feats=None, target_feats=None):
        """
        :params activation_fuction: Name of activation function
        :params num_GCN_blocks: Number of GNN layers of model
        :params input_dim: The number of dimensions of input
        :params output_dim: The number of dimensions of output
        :params num_source_nodes: Number of nodes in source graph
        :params num_target_nodes: Number of nodes in target graph
        :params source_feats: Source Initialized Features
        :params target_feats: Target Initialized Features
        """
        super(GCNA, self).__init__()
        self.num_GCN_blocks = num_GCN_blocks #GCN块数，为2
        self.source_feats = source_feats #源
        self.target_feats = target_feats #目标

        " 本来source_feats为3906 * 538 ;source_feats。shape[1]代表获取列的维度，就是538 "
        input_dim = self.source_feats.shape[1] #538
        self.input_dim = input_dim

        # GNN blocks (emb)
        self.GCNs = []
        """
            一共两层GCN，将两层GCN都加入进去，共有三个参数，激活函数、输入维度、输出维度
            经过两轮循环后，GCNs变成：
                    [GNN(
                        (activate_function): Tanh()
                        (linear): Linear(in_features=538, out_features=128, bias=False)
                        ), 
                        GNN(
                        (activate_function): Tanh()
                        (linear): Linear(in_features=128, out_features=128, bias=False)
                        )]
                
        """
        for i in range(num_GCN_blocks):
            self.GCNs.append(GCN(activate_function, input_dim, output_dim)) #特征信息
            """
                将最后一层的输出维度当做输入维度
            """
            input_dim = self.GCNs[-1].output_dim
        self.GCNs = nn.ModuleList(self.GCNs) #变成ModuleList类型
        init_weight(self.modules(), activate_function)
        " 再上一步完了以后，返回到的是GAlign.py里面的multi_level_embed函数(因为是从那里调的) "

    def forward(self, A_hat, net='s', new_feats=None):
        """
        Do the forward
        :params A_hat: The sparse Normalized Laplacian Matrix 
        :params net: Whether forwarding graph is source or target graph
        """
        if new_feats is not None:
            input = new_feats
        elif net == 's':
            input = self.source_feats
        else:
            input = self.target_feats
        emb_input = input.clone()
        outputs = [emb_input] # 第0层是什么都没有的
        for i in range(self.num_GCN_blocks): # 2
            #TODO
            """
                底下这个就是核心思想，将嵌入融合
                    即后面的共享前面的嵌入，那我们可以直接拿来用啊
                
                
                在这里注意一点，是GAlign嵌套GCN，也就是思想可以借鉴过来，我们在GCN写最简单的forward
                但是在这里要实现论文里面的所有功能，即要做融合操作。
            """
            #sourceTensor.clone().detach()
            GCN_output_i = self.GCNs[i](torch.tensor(emb_input, dtype=torch.float), torch.tensor(A_hat,dtype=torch.float))
            #GCN_output_i=GCN_output_i.to(device)
            #GCN_output_i = self.GCNs[i](emb_input, A_hat)
            outputs.append(GCN_output_i)
            emb_input = GCN_output_i #加入两层
        return outputs



class StableFactor(nn.Module):
    """
    Stable factor following each node
    """
    def __init__(self, num_source_nodes, num_target_nodes, cuda=True):
        """
        :param num_source_nodes: Number of nodes in source graph
        :param num_target_nodes: Number of nodes in target graph
        """
        super(StableFactor, self).__init__()
        # self.alpha_source_trainable = nn.Parameter(torch.ones(num_source_nodes))
        self.alpha_source = torch.ones(num_source_nodes)
        self.alpha_target = torch.ones(num_target_nodes)
        self.score_max = 0
        self.alpha_source_max = None
        self.alpha_target_max = None
        if cuda:
            self.alpha_source = self.alpha_source.cuda()
            self.alpha_target = self.alpha_target.cuda()
        self.use_cuda = cuda
    
        
    def forward(self, A_hat, net='s'):
        """
        Do the forward 
        :param A_hat is the Normalized Laplacian Matrix
        :net: whether graph considering is source or target graph.
        """
        if net=='s':
            self.alpha = self.alpha_source
        else:
            self.alpha = self.alpha_target
        alpha_colum = self.alpha.reshape(len(self.alpha), 1)
        if self.use_cuda:
            alpha_colum = alpha_colum.cuda()
        A_hat_new = (alpha_colum * (A_hat * alpha_colum).t()).t()
        return A_hat_new 


