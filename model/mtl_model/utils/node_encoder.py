'''
This file is adapted from https://github.com/lydiawunan/LOSTIN/blob/main/GNN-LSTM/node_encoder.py, with added node features.
'''
import sys
import torch
from features import get_node_feature_dims, get_edge_feature_dims,get_node_feature_dims_epfl
from torch_geometric.data import DataLoader
full_node_feature_dims = get_node_feature_dims_epfl()
full_edge_feature_dims = get_edge_feature_dims()


class NodeEncoder(torch.nn.Module):

    def __init__(self, emb_dim):
        super(NodeEncoder, self).__init__()
        emb_dim = int(emb_dim/len(full_node_feature_dims))
        self.node_embedding_list = torch.nn.ModuleList()
        for i, dim in enumerate(full_node_feature_dims):
            emb = torch.nn.Embedding(dim, emb_dim)
            torch.nn.init.xavier_uniform_(emb.weight.data)
            self.node_embedding_list.append(emb)

    
    def forward(self, x):
        x_emb_list = []
        for i in range(0, x.shape[1]):
            x_emb_list.append(self.node_embedding_list[i](x[:,i]))
        x_embedding = x_emb_list[0]
        for i in range(1, x.shape[1]):
            x_embedding = torch.cat((x_embedding, x_emb_list[i]), 1)
        return x_embedding
    
class NodeEncoder_2f(torch.nn.Module):

    def __init__(self, emb_dim):
        super(NodeEncoder_2f, self).__init__()
        emb_dim = int(emb_dim/2)
        self.node_embedding_list = torch.nn.ModuleList()

        for i, dim in enumerate(full_node_feature_dims):
            emb = torch.nn.Embedding(dim, emb_dim)
            torch.nn.init.xavier_uniform_(emb.weight.data)
            self.node_embedding_list.append(emb)
            if i == 1:
                break

    def forward(self, x):
        x_emb_list = []
        for i in range(0, x.shape[1]):
            x_emb_list.append(self.node_embedding_list[i](x[:,i]))
        x_embedding = x_emb_list[0]
        for i in range(1, x.shape[1]):
            x_embedding = torch.cat((x_embedding, x_emb_list[i]), 1)
        return x_embedding




class EdgeEncoder(torch.nn.Module):
    
    def __init__(self, emb_dim):
        super(EdgeEncoder, self).__init__()
        
        self.edge_embedding_list = torch.nn.ModuleList()

        for i, dim in enumerate(full_edge_feature_dims):
            emb = torch.nn.Embedding(dim, emb_dim)
            torch.nn.init.xavier_uniform_(emb.weight.data)
            self.edge_embedding_list.append(emb)

    def forward(self, edge_attr):
        edge_embedding = 0
        for i in range(edge_attr.shape[1]):
            edge_embedding += self.edge_embedding_list[i](edge_attr[:,i])

        return edge_embedding   


if __name__ == '__main__':
    pass






