#from Algorithm.comparison_model.WAlign.graphmodel import CloAlign
import loaddata
from algorithms.BigAlign import BigAlign
from algorithms.CENALP import CENALP
from algorithms.DeepLink import DeepLink
from algorithms.FINAL import FINAL
from algorithms.GCNA import GCNA
from algorithms.IONE import IONE
from algorithms.IsoRank import IsoRank
from algorithms.NAWAL import NAWAL
from algorithms.PALE import pale as PALE
from algorithms.REGAL import REGAL
from algorithms.Walign.Walign import Walign
from input.dataset import Dataset
from time import time
import sys
sys.path.append("..")
from evaluation.metrics import get_statistics
import utils.graph_utils as graph_utils
import random
import numpy as np
import torch
import argparse
import os
import pdb
from utils.graph_utils import load_gt
import torch.nn.functional as F
# import timesd
from deepmatch.aline import run_new
def parse_args():
    parser = argparse.ArgumentParser(description="Network alignment")
    parser.add_argument('--source_dataset', default="graph_data/douban/online/graphsage/")
    parser.add_argument('--target_dataset', default="graph_data/douban/offline/graphsage/")
    parser.add_argument('--groundtruth',    default="graph_data/douban/dictionaries/groundtruth")
    parser.add_argument('--data',    default="douban")
    parser.add_argument('--seed',           default=123,    type=int)
    subparsers = parser.add_subparsers(dest="algorithm", help='Choose 1 of the algorithm from: IsoRank, FINAL, UniAlign, NAWAL, DeepLink, REGAL, IONE, PALE, CloAlign')
    

    #CloAlign_ours
    parser_cloalign = subparsers.add_parser('CloAlign', help = 'our algorithm')
    parser_cloalign.add_argument('--sample', type=list, default=[0.95])
    parser_cloalign.add_argument('--repeat', type=int, default=1)
    #parser_cloalign.add_argument('--input_graph',type=str,default='graph_data/Email-Enron/Email-Enron.txt')
    #parser_cloalign.add_argument('--input_graph',type=str,default='graph_data/flickr/flickr.edge')
    parser_cloalign.add_argument('--input_graph', type=str, default='graph_data/douban/online/edgelist/online.edgelist')
    #parser_cloalign.add_argument('--input_graph',type=str,default='graph_data/test/test.txt')
    #parser_cloalign.add_argument('--output_graph',type=str,default='graph_data/Email-Enron/combin_Email-Enron.txt')
    #parser_cloalign.add_argument('--output_graph',type=str,default='graph_data/flickr/combin_flickr.edge')
    #parser_cloalign.add_argument('--output_graph',type=str,default='graph_data/test/combin_test.txt')
    parser_cloalign.add_argument('--output_graph',type=str,default='graph_data/douban/offline/edgelist/offline.edgelist')

    # NAWAL
    parser_nawal = subparsers.add_parser('NAWAL', help='NAWAL algorithm')
    parser_nawal.add_argument('--load_emb', action='store_true')
    parser_nawal.add_argument('--embedding_name', type=str, help='to save or load emb from file')
    parser_nawal.add_argument('--save_emb', type=str, help='weather to save emb')
    parser_nawal.add_argument('--nawal_mapping_batch_size', type=int, default=1000)
    parser_nawal.add_argument('--dis_smooth', type=float, default=0.1)
    parser_nawal.add_argument('--min_lr', type=float, default=1e-6)
    parser_nawal.add_argument('--lr_decay', type=float, default=0.98)
    parser_nawal.add_argument('--lr_shrink', type=float, default=0.5)
    parser_nawal.add_argument('--embedding_dim', type=int, default=2048)
    parser_nawal.add_argument('--dis_hid_dim', type=int, default=2048)
    parser_nawal.add_argument('--dis_layers', type=int, default=2)
    parser_nawal.add_argument('--dis_dropout', type=float, default=0.)
    parser_nawal.add_argument('--dis_input_dropout', type=float, default=0.1)
    parser_nawal.add_argument('--emb_lr', type=float, default=0.01)
    parser_nawal.add_argument('--map_optimizer', type=str, default="sgd,lr=0.1")
    parser_nawal.add_argument('--dis_optimizer', type=str, default="sgd,lr=0.1")
    parser_nawal.add_argument('--nawal_mapping_epochs', type=int, default=1) # 5
    parser_nawal.add_argument('--nawal_mapping_epoch_size', type=int, default=1000000)
    parser_nawal.add_argument('--test_dict',default="graph_data/data/ppi/ppi_ground_True.txt", type=str)
    parser_nawal.add_argument('--train_dict', default="graph_data/data/ppi/test.txt",type=str)
    parser_nawal.add_argument('--map_beta', type=float, default=0.001)
    parser_nawal.add_argument('--pale_map_batchsize', type=int, default=512)
    parser_nawal.add_argument('--pale_map_epochs', type=int, default=500)
    parser_nawal.add_argument('--pale_map_lr', type=float, default=0.01)
    parser_nawal.add_argument('--dis_steps', type=int, default=5)
    parser_nawal.add_argument('--neg_sample_size', type=int, default=10)
    parser_nawal.add_argument('--batch_size_embedding', type=int, default=1024)
    parser_nawal.add_argument('--embedding_epochs', type=int, default=10) # 500
    parser_nawal.add_argument('--UAGA_mode', action='store_true')
    parser_nawal.add_argument('--cuda', action='store_true')
    parser_nawal.add_argument('--hidden_dim1',         default=1200, type=int)
    parser_nawal.add_argument('--hidden_dim2',         default=1600, type=int)
    parser_nawal.add_argument('--mapper', type=str, default="nawal", help="Choose the mapper which is one of ('nawal', 'mlp', 'linear', 'deeplink'")
    parser_nawal.add_argument('--unsupervised_lr',     default=0.007, type=float)
    parser_nawal.add_argument('--supervised_lr',       default=0.007, type=float)
    parser_nawal.add_argument('--batch_size_mapping', default=200)
    parser_nawal.add_argument('--unsupervised_epochs', default=500, type=int)
    parser_nawal.add_argument('--supervised_epochs',   default=500,         type=int)
    parser_nawal.add_argument('--alpha',               default=0.8, type=float)
    parser_nawal.add_argument('--top_k',               default=5, type=int)



    # IsoRank
    parser_isorank = subparsers.add_parser('IsoRank', help='IsoRank algorithm')
    parser_isorank.add_argument('--H',                   default=None, help="Priority matrix")
    parser_isorank.add_argument('--max_iter',            default=50, type=int, help="Max iteration")
    parser_isorank.add_argument('--alpha',               default=0.82, type=float)
    parser_isorank.add_argument('--tol',                 default=1e-8, type=float)
    parser_isorank.add_argument('--train_dict', default="", type=str)


    # FINAL
    parser_final = subparsers.add_parser('FINAL', help='FINAL algorithm')
    parser_final.add_argument('--H',                   default=None, help="Priority matrix")
    parser_final.add_argument('--max_iter',            default=50, type=int, help="Max iteration")
    parser_final.add_argument('--alpha',               default=0.6, type=float)
    parser_final.add_argument('--tol',                 default=1e-2, type=float)
    parser_final.add_argument('--train_dict', default='', type=str)


    # BigAlign
    parser_bigalign = subparsers.add_parser('BigAlign', help='BigAlign algorithm')
    parser_bigalign.add_argument('--lamb', default=0.01, help="Lambda", type=float)


    # IONE
    parser_ione = subparsers.add_parser('IONE', help='IONE algorithm')
    parser_ione.add_argument('--train_dict', default="graph_data/douban/dictionaries/node,split=0.2.test.dict", help="Groundtruth use to train.")
    parser_ione.add_argument('--epochs', default=1, help="Total iterations.", type=int) #默认是60 这里改了
    parser_ione.add_argument('--dim', default=100, help="Embedding dimension.")
    parser_ione.add_argument('--cuda', action='store_true')
    parser_ione.add_argument('--lr', type=float, default=0.08)


    # REGAL
    parser_regal = subparsers.add_parser('REGAL', help='REGAL algorithm')
    parser_regal.add_argument('--attrvals', type=int, default=2,
                        help='Number of attribute values. Only used if synthetic attributes are generated')
    parser_regal.add_argument('--dimensions', type=int, default=128,
                        help='Number of dimensions. Default is 128.')
    parser_regal.add_argument('--k', type=int, default=10,
                        help='Controls of landmarks to sample. Default is 10.')
    parser_regal.add_argument('--max_layer', type=int, default=2,
                        help='Calculation until the layer for xNetMF.')
    parser_regal.add_argument('--alpha', type=float, default=0.01, help="Discount factor for further layers")
    parser_regal.add_argument('--gammastruc', type=float, default=1, help="Weight on structural similarity")
    parser_regal.add_argument('--gammaattr', type=float, default=1, help="Weight on attribute similarity")
    parser_regal.add_argument('--num_top', type=int, default=10,
                        help="Number of top similarities to compute with kd-tree.  If 0, computes all pairwise similarities.")
    parser_regal.add_argument('--buckets', default=2, type=float, help="base of log for degree (node feature) binning")


    # DeepLink
    parser_deeplink = subparsers.add_parser("DeepLink", help="DeepLink algorithm")
    parser_deeplink.add_argument('--cuda',                action="store_true")

    parser_deeplink.add_argument('--embedding_dim',       default=300,         type=int)
    parser_deeplink.add_argument('--embedding_epochs',    default=5,        type=int)

    parser_deeplink.add_argument('--unsupervised_lr',     default=0.007, type=float)
    parser_deeplink.add_argument('--supervised_lr',       default=0.007, type=float)
    parser_deeplink.add_argument('--batch_size_mapping',  default=200,         type=int)
    parser_deeplink.add_argument('--unsupervised_epochs', default=50, type=int)
    parser_deeplink.add_argument('--supervised_epochs',   default=50,         type=int)

    parser_deeplink.add_argument('--train_dict',          default="graph_data/acm_dblp/dictionaries/node,split=0.1.train.dict")
    parser_deeplink.add_argument('--hidden_dim1',         default=1200, type=int)
    parser_deeplink.add_argument('--hidden_dim2',         default=1600, type=int)

    parser_deeplink.add_argument('--number_walks',        default=100, type=int)
    parser_deeplink.add_argument('--format',              default="edgelist")
    parser_deeplink.add_argument('--walk_length',         default=5, type=int)
    parser_deeplink.add_argument('--window_size',         default=2, type=int)
    parser_deeplink.add_argument('--top_k',               default=5, type=int)
    parser_deeplink.add_argument('--alpha',               default=0.8, type=float)
    parser_deeplink.add_argument('--num_cores',           default=8, type=int)


    # PALE
    parser_PALE = subparsers.add_parser('PALE', help="PALE algorithm")
    parser_PALE.add_argument('--cuda',                action='store_true')

    parser_PALE.add_argument('--learning_rate1',      default=0.01,        type=float)
    parser_PALE.add_argument('--embedding_dim',       default=300,         type=int)
    parser_PALE.add_argument('--batch_size_embedding',default=512,         type=int)
    parser_PALE.add_argument('--embedding_epochs',    default=500,        type=int)
    parser_PALE.add_argument('--neg_sample_size',     default=10,          type=int)
    parser_PALE.add_argument('--num_walks',     default=10,          type=int)
    parser_PALE.add_argument('--walk_len',     default=10,          type=int)
    parser_PALE.add_argument('--cur_weight',     default=1,          type=float)


    parser_PALE.add_argument('--learning_rate2',      default=0.01,       type=float)
    parser_PALE.add_argument('--batch_size_mapping',  default=32,         type=int)
    parser_PALE.add_argument('--mapping_epochs',      default=100,         type=int)
    parser_PALE.add_argument('--mapping_model',       default='linear')
    parser_PALE.add_argument('--activate_function',   default='sigmoid')
    parser_PALE.add_argument('--toy',   action="store_true")
    parser_PALE.add_argument('--train_dict',          default='graph_data/douban/dictionaries/node,split=0.01.train.dict')
    parser_PALE.add_argument('--embedding_name',          default='')
    


    # CENALP
    parser_CENALP = subparsers.add_parser('CENALP', help="CENALP algorithm")
    parser_CENALP.add_argument('--cuda',                action='store_true')

    parser_CENALP.add_argument('--embedding_dim',       default=64,         type=int)
    parser_CENALP.add_argument('--num_walks',       default=20,         type=int)
    parser_CENALP.add_argument('--neg_sample_size',       default=10,         type=int)
    parser_CENALP.add_argument('--walk_len',       default=5,         type=int)
    parser_CENALP.add_argument('--alpha', default=5, type=float)
    parser_CENALP.add_argument('--switch_prob', default=0.3, type=float)
    parser_CENALP.add_argument('--batch_size', default=512, type=int)
    parser_CENALP.add_argument('--walk_every', default=8, type=int)
    parser_CENALP.add_argument('--learning_rate', default=0.01, type=float)
    parser_CENALP.add_argument('--threshold', default=0.5, type=float)
    parser_CENALP.add_argument('--train_dict', default="graph_data/douban/dictionaries/node,split=0.01.train.dict", type=str)
    parser_CENALP.add_argument('--num_sample',     default=300,          type=int, help="Number of samples for linkprediction")
    parser_CENALP.add_argument('--linkpred_epochs',     default=10,          type=int, help="Number of linkprediction epochs")
    parser_CENALP.add_argument('--num_iteration_epochs',     default=15,          type=int, help="Number of pair to add each epoch")

    #Walign
    parser_Walign = subparsers.add_parser("Walign", help= "walign algorithm")
    parser_Walign.add_argument('--noise',type = float, default=0.0)
    parser_Walign.add_argument('--epochs',type = int, default=1)
    parser_Walign.add_argument('--user_config', type = bool, default=True)
    parser_Walign.add_argument('--prior_rate', type = int, default=0.02)
    parser_Walign.add_argument('lr', type=float,default=0.001)
    parser_Walign.add_argument('lr_wd', type=float,default=0.01)
    parser_Walign.add_argument('lr_recon', type=float,default=0.01)
    parser_Walign.add_argument('--alpha', type=float,default=0.01)
    parser_Walign.add_argument('--hidden_size', type=int,default=512)


    # GCNA
    parser_GCNA = subparsers.add_parser("GCNA", help="GCNA algorithm")
    parser_GCNA.add_argument('--cuda',                action="store_true")
    parser_GCNA.add_argument('--embedding_dim',       default=128,         type=int)
    parser_GCNA.add_argument('--GCNA_epochs',    default=100,        type=int)
    parser_GCNA.add_argument('--lr', default=0.005, type=float)
    parser_GCNA.add_argument('--num_GCN_blocks', type=int, default=2)
    parser_GCNA.add_argument('--act', type=str, default='tanh')
    parser_GCNA.add_argument('--log', action="store_true", help="Just to print loss")
    parser_GCNA.add_argument('--invest', action="store_true", help="To do some statistics")
    parser_GCNA.add_argument('--input_dim', default=100, help="Just ignore it")
    parser_GCNA.add_argument('--alpha0', type=float, default=1)
    parser_GCNA.add_argument('--alpha1', type=float, default=1)
    parser_GCNA.add_argument('--alpha2', type=float, default=1)
    parser_GCNA.add_argument('--noise_level', type=float, default=0)

    # refinement
    parser_GCNA.add_argument('--refinement_epochs', default=80, type=int)
    parser_GCNA.add_argument('--threshold_refine', type=float, default=0.94, help="The threshold value to get stable candidates")

    # loss
    parser_GCNA.add_argument('--beta', type=float, default=1, help='balancing source-target and source-augment')
    parser_GCNA.add_argument('--threshold', type=float, default=0.01, help='confidence threshold for adaptivity loss')
    parser_GCNA.add_argument('--coe_consistency', type=float, default=0.8, help='balancing consistency and adaptivity loss')

    return parser.parse_args()


if __name__ == '__main__':
    """
        1、算法IsoRank已经跑通：（无监督、有监督均可，跑的是Douban）
            ---------------------------------------------------------------------------------------------------
            Accuracy: 0.0009
            MAP: 0.0070
            Precision_1: 0.0009
            Precision_5: 0.0045
            ---------------------------------------------------------------------------------------------------
        
        2、算法PALE尚未跑通（无监督），batchsize太大？
        
        3、算法BigAlign已经跑通：
            ---------------------------------------------------------------------------------------------------
            Accuracy: 0.0072
            MAP: 0.0404
            Precision_5: 0.0358
            Precision_10: 0.0769
            ---------------------------------------------------------------------------------------------------
        
        4、算法IONE已经跑通（有监督）：
            ----------------------------------------------------------------------------------------------------
            Accuracy: 0.0009
            MAP: 0.0073
            Precision_5: 0.0063
            Precision_10: 0.0125
            ----------------------------------------------------------------------------------------------------
        
        5、算法FINAL已经跑通（可以有监督，也可以无监督）【成功达到论文的复现结果】：
            ----------------------------------------------------------------------------------------------------
            Accuracy: 0.4383
            MAP: 0.5539
            Precision_5: 0.6896
            Precision_10: 0.7710
            ----------------------------------------------------------------------------------------------------
            Running time: 92.40768384933472

        
        6、算法CENALP没跑起来。
        
        7、算法DeepLink(无监督)已经跑通:
            ----------------------------------------------------------------------------------------------------
            Accuracy: 0.1082
            MAP: 0.1973
            Precision_5: 0.2952
            Precision_10: 0.3792
            ----------------------------------------------------------------------------------------------------
        
        8、算法REGAL已经跑通：
            ----------------------------------------------------------------------------------------------------
            Accuracy: 0.0259
            MAP: 0.0728
            Precision_5: 0.0957
            Precision_10: 0.1503
            ----------------------------------------------------------------------------------------------------
        
        9、算法NAWAL已经跑通
            ----------------------------------------------------------------------------------------------------
            Accuracy: 0.0000
            MAP: 0.0067
            Precision_5: 0.0063
            Precision_10: 0.0116
            ----------------------------------------------------------------------------------------------------
        
                        
    """
    args = parse_args()
    print(args)
    start_time = time()
    # random.seed(args.seed)
    # np.random.seed(args.seed)
    # torch.manual_seed(args.seed)

    if args.data in ['ppi', 'douban' ,'dblp', 'flickr', 'citeseer', 'blocat','acm_dblp','nell', 'citeseer2','uai']:
        source_dataset = loaddata.loaddata(args.data, 's', '0.1')
        target_dataset = loaddata.loaddata(args.data, 't', '0.1')
        groundtruth = loaddata.loadgroundtruth(args.data, '0.1')
        if args.data in ['douban']:
            groundtruth = dict([val, key] for key, val in groundtruth.items())
    else :
        source_dataset = Dataset(args.source_dataset)
        target_dataset = Dataset(args.target_dataset)
        groundtruth = graph_utils.load_gt(args.groundtruth, source_dataset.id2idx, target_dataset.id2idx, 'dict')

    algorithm = args.algorithm
    print(f'algorithm is {algorithm}')
    if algorithm == "IsoRank":
        train_dict = None
        if args.train_dict != "":
            train_dict = graph_utils.load_gt(args.train_dict, source_dataset.id2idx, target_dataset.id2idx, 'dict')
        model = IsoRank(source_dataset, target_dataset, args.H, args.alpha, args.max_iter, args.tol, train_dict=train_dict)
    elif algorithm == "FINAL":
        train_dict = None
        if args.train_dict != "":
            train_dict = graph_utils.load_gt(args.train_dict, source_dataset.id2idx, target_dataset.id2idx, 'dict')
        model = FINAL(source_dataset, target_dataset, H=args.H, alpha=args.alpha, maxiter=args.max_iter, tol=args.tol, train_dict=train_dict)
    elif algorithm == "REGAL":
        model = REGAL(source_dataset, target_dataset, max_layer=args.max_layer, alpha=args.alpha, k=args.k, num_buckets=args.buckets,
                      gammastruc = args.gammastruc, gammaattr = args.gammaattr, normalize=True, num_top=args.num_top)
    elif algorithm == "BigAlign":
        model = BigAlign(source_dataset, target_dataset, lamb=args.lamb)
    elif algorithm == "IONE":
        model = IONE(source_dataset, target_dataset, gt_train=args.train_dict, epochs=args.epochs, dim=args.dim, seed=args.seed, learning_rate=args.lr)
    elif algorithm == "DeepLink":
        model = DeepLink(source_dataset, target_dataset, args, groundtruth)
    elif algorithm == "GCNA":
        model = GCNA(source_dataset, target_dataset, args, groundtruth)
    elif algorithm == "PALE":
        model = PALE(source_dataset, target_dataset, args, groundtruth)
    elif algorithm == "CENALP":
        model = CENALP(source_dataset, target_dataset, args)
    elif algorithm == "NAWAL":
        model = NAWAL(source_dataset, target_dataset, args)
    elif algorithm =="Walign":
        model = Walign(source_dataset,target_dataset, args)
    # elif algorithm == "CloAlign":
    #      model = CloAlign(args)
    else:
        raise Exception("Unsupported algorithm")

    #model = CloAlign(args)
    S = model.align()

    # 此处的S就是对齐矩阵
    # if algorithm != 'CloAlign':
    print("-"*100)
    acc, MAP, top5, top10, AUC = get_statistics(S, groundtruth, use_greedy_match=True, get_all_metric=True)
    print("Accuracy: {:.4f}".format(acc))
    print("MAP: {:.4f}".format(MAP))
    print("Precision_5: {:.4f}".format(top5))
    print("Precision_10: {:.4f}".format(top10))
    print("AUC: {:.4f}".format(AUC))
    print("-"*100)
    print('Running time: {}'.format(time()-start_time))

    # else :
    #     secore = run_new(S.detach().numpy(), 'aline_true.txt')
    #     print(secore)