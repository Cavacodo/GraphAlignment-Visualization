# 作者：York
# 时间：2022/4/13 14:13

import sys
sys.path.append("..")
from algorithms.network_alignment_model import NetworkAlignmentModel

import torch.nn.functional as F
import torch.nn as nn

class Walign(NetworkAlignmentModel):
    def __init__(self, source_dataset, target_dataset, args):
        super(Walign, self).__init__(source_dataset, target_dataset)
        self.source_dataset = source_dataset
        self.target_dataset = target_dataset
        self.args = args









