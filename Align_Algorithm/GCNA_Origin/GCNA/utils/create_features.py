import argparse
import numpy as np
import utils.graph_utils as graph_utils

from input.dataset import Dataset



def parse_args():
    parser = argparse.ArgumentParser(description="Create synthetic feature for graph")
    parser.add_argument('--input_data1', default="../graph_data/fq-tw/twitter/graphsage/")
    parser.add_argument('--input_data2', default="../graph_data/fq-tw/foursquare/graphsage/")
    parser.add_argument('--feature_dim', default=128, type=int)
    parser.add_argument('--ground_truth', default="../graph_data/fq-tw/dictionaries/groundtruth")
    return parser.parse_args()




def create_features(data1, data2, dim, ground_truth):
    feature1 = create_feature(data1, dim)
    feature2 = create_feature(data2, dim)
    
    inverted_groundtruth = {v:k for k, v in ground_truth.items()}
    for i in range(len(feature2)):
        try:
            feature2[i] = feature1[inverted_groundtruth[i]]
        except:
            continue

    return feature1, feature2

def create_featurex(data, dim):
    deg = data.get_nodes_degrees()
    deg = np.array(deg)
    binn = int(max(deg) / dim)
    feature = np.zeros((len(data.G.nodes()), dim))
    for i in range(len(deg)):
        deg_i = deg[i]
        node_i = data.G.nodes()[i]
        node_i_idx = data.id2idx[node_i]
        feature[node_i_idx, int(deg_i/(binn+ 1))] = 1
    return feature

def create_feature(data, dim):
    shape = (len(data.G.nodes()), int(dim))
    features = np.random.uniform(size=shape)
    for i, feat in enumerate(features):
        mask = np.ones(feat.shape, dtype=bool)
        mask[feat.argmax()] = False
        feat[~mask] = 1
        feat[mask] = 0
    return features


from txdpy import get_num


def test():
    args = parse_args()
    data1 = Dataset(args.input_data2)
    l = list(data1.G.nodes())
    l = [get_num(i) for i in l]
    print(l)


def trans(gt, data1, data2):
    X = np.genfromtxt(gt)
    print(X)



def load_gt(path, id2idx_src=None, id2idx_trg=None, format='matrix'):
    if id2idx_src:
        conversion_src = type(list(id2idx_src.keys())[0]) #str
        conversion_trg = type(list(id2idx_trg.keys())[0]) #str
    if format == 'matrix':
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
    return gt


if __name__ == "__main__":
    #test()
    args = parse_args()

    data1 = Dataset(args.input_data1)
    data2 = Dataset(args.input_data2)
    trans(args.ground_truth, data2, data1)
    ground_truth = load_gt(args.ground_truth, None, None, 'dict')
    feature1, feature2 = create_features(data1, data2, args.feature_dim, ground_truth)
    np.save(args.input_data1 + '/feats.npy', feature1)
    np.save(args.input_data2 + '/feats.npy', feature2)
