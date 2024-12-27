'''
This file is adapted from https://github.com/lydiawunan/LOSTIN/blob/main/GNN-LSTM/read_graph_pyg.py, with added node levels
'''
import pandas as pd
import torch
from torch_geometric.data import Data
import os.path as osp
import numpy as np
from read_graph_raw import read_csv_graph_raw
from tqdm import tqdm


import torch
import numpy


# see https://github.com/unbounce/pytorch-tree-lstm/blob/66f29a44e98c7332661b57d22501107bcb193f90/treelstm/util.py#L8

def top_sort(edge_index, graph_size):

    node_ids = numpy.arange(graph_size, dtype=int)

    node_order = numpy.zeros(graph_size, dtype=int)
    unevaluated_nodes = numpy.ones(graph_size, dtype=bool)

    parent_nodes = edge_index[0]
    child_nodes = edge_index[1]

    n = 0
    while unevaluated_nodes.any():
        # Find which parent nodes have not been evaluated
        unevaluated_mask = unevaluated_nodes[parent_nodes]

        # Find the child nodes of unevaluated parents
        unready_children = child_nodes[unevaluated_mask]

        # Mark nodes that have not yet been evaluated
        # and which are not in the list of children with unevaluated parent nodes
        nodes_to_evaluate = unevaluated_nodes & ~numpy.isin(node_ids, unready_children)

        node_order[nodes_to_evaluate] = n
        unevaluated_nodes[nodes_to_evaluate] = False

        n += 1

    return torch.from_numpy(node_order).long()


# to be able to use pyg's batch split everything into 1-dim tensors
def add_order_info_01(graph):
    print(graph)
    print(max(graph.edge_index[0,:]), min(graph.edge_index[0,:]))
    l0 = top_sort(graph.edge_index, graph.num_nodes)
    ei2 = torch.LongTensor([list(graph.edge_index[1]), list(graph.edge_index[0])])
    l1 = top_sort(ei2, graph.num_nodes)
    ns = torch.LongTensor([i for i in range(graph.num_nodes)])

    graph.__setattr__("bi_layer_idx0", l0)
    graph.__setattr__("bi_layer_index0", ns)
    graph.__setattr__("bi_layer_idx1", l1)
    graph.__setattr__("bi_layer_index1", ns)
    assert_order(graph.edge_index, l0, ns)
    assert_order(ei2, l1, ns)
    return graph
    



def assert_order(edge_index, o, ns):
    # already processed
    proc = []
    for i in range(max(o)+1):
        # nodes in position i in order
        l = o == i
        l = ns[l].tolist()
        for n in l:
            # predecessors
            ps = edge_index[0][edge_index[1] == n].tolist()
            for p in ps:
                assert p in proc
        proc += l


def add_order_info(graph):
    ns = torch.LongTensor([i for i in range(graph.num_nodes)])
    layers = torch.stack([top_sort(graph.edge_index, graph.num_nodes), ns], dim=0)
    ei2 = torch.LongTensor([list(graph.edge_index[1]), list(graph.edge_index[0])])
    layers2 = torch.stack([top_sort(ei2, graph.num_nodes), ns], dim=0)

    graph.__setattr__("bi_layer_index", torch.stack([layers, layers2], dim=0))



def read_graph_pyg(raw_dir, add_inverse_edge = False, additional_node_files = [], additional_edge_files = [], binary = False):

    graph_list = read_csv_graph_raw(raw_dir, add_inverse_edge, additional_node_files = additional_node_files, additional_edge_files = additional_edge_files)
    
    pyg_graph_list = []

    print('Converting graphs into PyG objects...')

    for graph in tqdm(graph_list):
        g = Data()
        g.__num_nodes__ = graph['num_nodes']
        g.edge_index = torch.from_numpy(graph['edge_index'])

        del graph['num_nodes']
        del graph['edge_index']

        if graph['edge_feat'] is not None:
            g.edge_attr = torch.from_numpy(graph['edge_feat'])
            del graph['edge_feat']

        if graph['node_feat'] is not None:
            g.x = torch.from_numpy(graph['node_feat'])
            del graph['node_feat']

        for key in additional_node_files:
            g[key] = torch.from_numpy(graph[key])
            del graph[key]
            
            
        for key in additional_edge_files:
            g[key] = torch.from_numpy(graph[key])
            del graph[key]
            
        g = add_order_info_01(g)  # DAGNN
        x = g.x
        x[:,0] = g.bi_layer_idx0
        g.x = x
        g.len_longest_path = float(torch.max(g.bi_layer_idx0).item())
        pyg_graph_list.append(g)



    return pyg_graph_list



if __name__ == '__main__':
    pass