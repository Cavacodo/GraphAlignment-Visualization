import matplotlib.pyplot as plt
import pandas as pd

from input.dataset import Dataset
from time import time
from algorithms import *
from evaluation.metrics import get_statistics
import numpy as np
import torch
import argparse
import os
import pdb
import seaborn as sns
import graph_utils


def parse_args():
    '''parser = argparse.ArgumentParser(description="Network alignment")
    parser.add_argument('--source_dataset', default="data/flickr_lastfm/flickr/graphsage/")
    parser.add_argument('--target_dataset', default="data/flickr_lastfm/lastfm/graphsage/")
    parser.add_argument('--groundtruth',    default="data/flickr_lastfm/dictionaries/groundtruth")'''

    parser = argparse.ArgumentParser(description="Network alignment")
    parser.add_argument('--source_dataset', default="../graph_data/douban/online/graphsage/")
    parser.add_argument('--target_dataset', default="../graph_data/douban/offline/graphsage/")
    parser.add_argument('--groundtruth',    default="../graph_data/douban/dictionaries/groundtruth")

    # parser.add_argument('--source_dataset2', default="data/ppi/graphsage/")
    # parser.add_argument('--target_dataset2', default="data/ppi/REGAL-d2-seed1/graphsage/")
    # parser.add_argument('--groundtruth2',    default="data/ppi/REGAL-d2-seed1/dictionaries/groundtruth")

    return parser.parse_args()



def line_chart(models, data_matrix, x_label, y_label, title=None, name=None):
    # styles = ['o', '>', 's', 'd', '^', 'x', '*', 'v']
    styles = ['o', 'v', 's', '*']
    line_styles = ['--', '-', '-', '-.', ':']
    # styles = ['o-', '>--', 's-', 'd-.', '^:', 'x-', '*-', 'v-']
    colors = ['#003300', '#009933', '#33cc33', '#66ff66', '#99ff99', '#ffffff']
    fig, ax1 = plt.subplots(figsize=(18, 9))
    num_models = data_matrix.shape[0]
    num_x_levels = data_matrix.shape[1]

    for i in range(num_models):
        line = data_matrix[i]
        x = np.arange(len(line))
        ax1.plot(x, line, line_styles[i], label=models[i])

    ax1.set_xlabel(x_label, labelpad = 10, fontsize=35)
    ax1.set_ylabel(y_label, labelpad = 10, fontsize=35)
    if title is not None:
        plt.title(title, loc='center', color='black', fontsize=35)

    ax1.tick_params(labelsize=35)
    # ax1.set_xticks(np.arange(len(xpoints)))
    # ax1.set_xticklabels(xpoints)
    ax1.set_xlim(-20, data_matrix.shape[1] + 20)
    # ax1.set_ylim(-1, 1)
    # ax1.set_yticks(np.arange(0, maxx + .1, 0.2))
    ax1.legend(fontsize=25)
    ax1.grid(True)
    plt.tight_layout()
    folder = "../chart/"
    if not os.path.exists(folder):
        os.mkdir(folder)
    #plt.show()
    plt.savefig(folder + name)

    plt.close()

def tong_chart(x_label, y_label, title=None, name=None):
    # styles = ['o', '>', 's', 'd', '^', 'x', '*', 'v']
    styles = ['o', 'v', 's', '*']
    line_styles = ['--', '-', '-', '-.', ':']
    # styles = ['o-', '>--', 's-', 'd-.', '^:', 'x-', '*-', 'v-']
    colors = ['#003300', '#009933', '#33cc33', '#66ff66', '#99ff99', '#ffffff']
    data = pd.read_csv('../chart/douban_diff.csv')
    Anchor_nodes = list(data['Anchor nodes'])
    Degree_Difference = list(data['Degree Difference'])
    plt.bar(Anchor_nodes, Degree_Difference)
    x = [i for i in range(0,11)]
    xx = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9','≥10']
    plt.xticks(x, labels=xx)
    plt.xlabel('Local Topology Degree Difference')
    plt.ylabel('Counts')
    #sns.displot(data=data)
    folder = "../chart/"
    if not os.path.exists(folder):
        os.mkdir(folder)
    #plt.show()
    plt.savefig(folder + name)

    plt.close()



def get_degree_array(dataset, idx2id, gt_index):
    degrees = []
    for index in gt_index:
        node = idx2id[int(index)]
        degrees.append(dataset.G.degree()[node])
    return np.array(degrees)

def normalize_data(matrix):
    matrix = matrix - np.mean(matrix)
    matrix /= np.std(matrix)
    return matrix

def get_distance(source_dataset, target_dataset, groundtruth):
    source_gt_index = groundtruth.keys()
    target_gt_index = groundtruth.values()
    source_degree = get_degree_array(source_dataset, source_idx2id, source_gt_index)
    # source_degree = normalize_data(source_degree)
    target_degree = get_degree_array(target_dataset, target_idx2id, target_gt_index)
    # target_degree = normalize_data(target_degree)
    # distance = source_degree - target_degree
    # return np.random.choice(distance, 300)

    diff_degree = [ abs(source_degree[x] - target_degree[x]) for x in range(1118) ]
    dif = {}
    for key in diff_degree:
        dif[key] = dif.get(key, 0) + 1
    dif = sorted(dif.items())
    diff = [[i[0], i[1]] for i in dif]

    return source_degree[:1118], target_degree[:1118], diff
import os
if __name__ == "__main__":
    args = parse_args()
    source_dataset = Dataset(args.source_dataset)
    target_dataset = Dataset(args.target_dataset)

    source_id2idx = source_dataset.id2idx
    target_id2idx = target_dataset.id2idx
    source_idx2id = {v:k for k, v in source_id2idx.items()}
    target_idx2id = {v:k for k, v in target_id2idx.items()}
    groundtruth = graph_utils.load_gt(args.groundtruth, source_id2idx, target_id2idx, "dict")

    source_degree, target_degree, diff_degree = get_distance(source_dataset, target_dataset, groundtruth)
    if not os.path.exists('../chart/douban_diff.csv'):
        import csv
        with open('../chart/douban_diff.csv', 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['Anchor nodes', 'Degree Difference'])
            for i in diff_degree:
                csv_writer.writerow([str(i[0]), str(i[1])])
            print('Writting degree Success')
            f.close()
    data_matrix = np.array([source_degree, target_degree])
    diff_matirx = np.array(diff_degree).T
    models = ["source graph", "target graph"]
    #line_chart(models, data_matrix, "Anchor pairs", "Degree", name="douban.png")
    tong_chart("Anchor pairs", "Degree difference", name="douban_diff.png")
    # exit()
    # source_dataset = Dataset(args.source_dataset2)
    # target_dataset = Dataset(args.target_dataset2)

    # source_id2idx = source_dataset.id2idx
    # target_id2idx = target_dataset.id2idx
    # source_idx2id = {v:k for k, v in source_id2idx.items()}
    # target_idx2id = {v:k for k, v in target_id2idx.items()}
    # groundtruth = graph_utils.load_gt(args.groundtruth2, source_id2idx, target_id2idx, "dict", True)

    # distance2 = get_distance(source_dataset, target_dataset, groundtruth)

    # data_matrix = np.array([distance1, distance2])
    # # print(np.max(source_degree), np.min(source_degree))
    # models = ["real_data", "synthetic_data"]
    # # data_matrix = np.array([source_degree - target_degree])
    
    # # print(data_matrix)
    # line_chart(models, data_matrix, "Anchor pairs", "Degree")

