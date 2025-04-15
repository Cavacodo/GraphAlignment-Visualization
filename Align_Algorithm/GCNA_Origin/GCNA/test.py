# 作者：York
# 时间：2022/4/25 11:16
from algorithms import GCNA
from input.dataset import Dataset
from network_alignment import parse_args
import torch
import time
import sys
sys.path.append("algorithms")
import utils.graph_utils as graph_utils
args = parse_args()
print(args)
# random.seed(args.seed)
# np.random.seed(args.seed)
# torch.manual_seed(args.seed)

source_dataset = Dataset(args.source_dataset)
target_dataset = Dataset(args.target_dataset)
groundtruth = graph_utils.load_gt(args.groundtruth, source_dataset.id2idx, target_dataset.id2idx, 'dict')

model = GCNA(source_dataset, target_dataset, args)


source_A_hat, target_A_hat, source_feats, target_feats = model.get_elements()
g = model.multi_level_embed(source_A_hat, target_A_hat, source_feats, target_feats)


print(g)

