'''
This file is adapted from https://github.com/lydiawunan/LOSTIN/blob/main/GNN-LSTM/features.py, with added node features.
'''
import json
import pandas as pd
import networkx as nx
import csv
allowable_features = {
    'node_type': ['input', 'intermediate', 'output'], 
    'op_type': ['$_AND_',  '$_NOT_', 'input', 'output'],
    
}

def safe_index(l, e):
    """
    Return index of element e in list l. If e is not present, return the last index
    """
    try:
        return l.index(e)
    except:
        print(l,e)
        raise ValueError("invalid index")
        return len(l) - 1


def node_type(opcode):
    if opcode == 'input' or opcode == 'output':
        return opcode
    if opcode in {'$_AND_', '$_NOT_'}:
        t='intermediate'
    return t


def node_to_feature_vector(node):
    """
    Converts node object to feature list of indices
    :return: list
    """
    node_feature = [
            safe_index(allowable_features['node_type'], node_type(node['node_attributes']['node_type'])),
            safe_index(allowable_features['op_type'], node['node_attributes']['node_type']),
            ]
   
    return node_feature

def node_to_feature_vector_G(node, ori_node, input_nodes, max_level, in_deg, out_deg):
    """
    Converts node object to feature list of indices
    :return: list
    """
    node_feature = [
            max_level,
            safe_index(allowable_features['op_type'], node['type']),
            in_deg,
            out_deg
            ]
   
    return node_feature


def get_node_feature_dims():
    return list(map(len, [
        [i for i in range(10000)],

        [i for i in range(3)],
        [i for i in range(10)],
        [i for i in range(1000)]
        ]))
        
def get_node_feature_dims_epfl():
    return list(map(len, [
        [i for i in range(50000)],

        [i for i in range(5)],
        [i for i in range(10)],
        [i for i in range(1000)]
        ]))

def edge_to_feature_vector(edge):
    """
    Converts edge to feature list of indices
    :return: list
    """
    bond_feature = [0]
    return bond_feature

def get_edge_feature_dims():
    return [1]


def gen_dataset():
    with open('dataset_all/vgraph/graph_info.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Num Nodes', 'Num Edges', 'Logic Level', 'Num AND', 'Num NOT', 'Num INPUT', 'Num OUTPUT'])

    read_dir='graph/'
    dest_dir = 'dataset_all/vgraph/raw/'
    vgraphs = []
    with open('designlist.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            vgraphs.append(line.strip()+'.json')
    
    input_nums = []
    output_nums = []
    with open('io_list.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            inputs = line.split()[0]
            outputs = line.split()[1]
            input_nums.append(int(inputs))
            output_nums.append(int(outputs))    
    node_feat=[]
    edge_list=[]
    edge_feat=[]
    num_node_list=[]
    num_edge_list=[]
    io_node_list = []
    graph_label_list = []
    for i in range(len(vgraphs)):
        csv_row = []
        print("Working on design {}".format(vgraphs[i]))
        f = open(read_dir+vgraphs[i], 'r')
        d = json.load(f)
        f.close()
        G = nx.DiGraph()
        G.add_nodes_from(d['nodes'])
        G.add_edges_from(d['edges'])
        input_nodes = []
        output_nodes = []
        output_nodes_idx = []
        for node in G.nodes:
            if G.in_degree(node) == 0:
                input_nodes.append(node)
        for node in G.nodes:
            if G.out_degree(node) == 0:
                output_nodes.append(node)
        G_in_deg = dict(G.in_degree(G.nodes))
        G_out_deg = dict(G.out_degree(G.nodes))

        nodes=d['nodes']
        edges=d['edges']

        node_index_map=dict() # map the node name to the index
        index=0

        for n in nodes:
            # print(n)
            
            if n[0] not in node_index_map:
                node_index_map[n[0]]=index
            n_in_deg = G_in_deg[n[0]]
            n_out_deg = G_out_deg[n[0]]

            max_level = 0


            node_feat.append(node_to_feature_vector_G(n[1], n[0], input_nodes, max_level, n_in_deg, n_out_deg))
            
            if n[0] in output_nodes:
                output_nodes_idx.append(int(index))
            index=index+1

        for e in edges:
            source=node_index_map[e[0]]
            sink=node_index_map[e[1]]
            edge_list.append([source,sink])
            edge_feat.append(edge_to_feature_vector(e[2]))
            
        num_node_list.append(len(nodes))
        num_edge_list.append(len(edges))

        graph_label_list.append([1])
        
        #process csv
        num_and = 0
        num_not = 0
        num_i = 0
        num_o = 0
        for n in G.nodes():
            if G.nodes[n]['type'] == '$_NOT_':
                num_not+=1
            elif G.nodes[n]['type'] == '$_AND_':
                num_and+=1
            elif G.nodes[n]['type'] == 'input':
                num_i+=1
            elif G.nodes[n]['type'] == 'output':
                num_o+=1
            else:
                print(n)
                print(G.nodes[n])
        
        csv_row.append(vgraphs[i].split('.')[0])
        csv_row.append(len(d['nodes']))
        csv_row.append(len(d['edges']))
        csv_row.append(0)
        csv_row.append(num_and)
        csv_row.append(num_not)
        csv_row.append(num_i)
        csv_row.append(num_o)
        with open('dataset_datapath/vgraph/graph_info.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(csv_row)
        

    NODE=pd.DataFrame(node_feat)
    EDGE_list=pd.DataFrame(edge_list)
    EDGE_feat=pd.DataFrame(edge_feat)
    node_num = pd.DataFrame(num_node_list)
    edge_num = pd.DataFrame(num_edge_list)
    # io_node_list = pd.DataFrame(io_node_list)
    graph_label = pd.DataFrame(graph_label_list)

    NODE.to_csv(dest_dir+'node-feat.csv',index=False,header=False)
    EDGE_list.to_csv(dest_dir+'edge.csv',index=False,header=False)
    EDGE_feat.to_csv(dest_dir+'edge-feat.csv',index=False,header=False)
    node_num.to_csv(dest_dir+'num-node-list.csv',index=False,header=False)
    edge_num.to_csv(dest_dir+'num-edge-list.csv',index=False,header=False)   
    # io_node_list.to_csv(dest_dir+'io-node-list.csv', index=False,header=False)
    graph_label.to_csv(dest_dir+'graph-label.csv', index=False,header=False)

if __name__ == '__main__':
    gen_dataset()