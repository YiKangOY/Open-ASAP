'''
This file  from https://github.com/lydiawunan/LOSTIN/blob/main/GNN-LSTM/gnn.py.
'''
import torch
import torch.nn as nn
from torch_geometric.nn import MessagePassing,BatchNorm
from torch_geometric.nn import global_add_pool, global_mean_pool, global_max_pool, GlobalAttention, Set2Set
import torch.nn.functional as F
from torch_geometric.nn.inits import uniform
from torch.nn import Sequential, ReLU, Linear, ModuleList
from conv import GNN_node, GNN_node_Virtualnode


class GNN(torch.nn.Module):

    def __init__(self, num_tasks, num_layer = 5, emb_dim = 100, 
                    gnn_type = 'gin', virtual_node = True, residual = False, drop_ratio = 0.5, JK = "last", graph_pooling = "mean"):
        '''
            num_tasks (int): number of labels to be predicted
            virtual_node (bool): whether to add virtual node or not
        '''

        super(GNN, self).__init__()

        self.num_layer = num_layer
        self.drop_ratio = drop_ratio
        self.JK = JK
        self.emb_dim = emb_dim
        self.num_tasks = num_tasks
        self.graph_pooling = graph_pooling

        if self.num_layer < 2:
            raise ValueError("Number of GNN layers must be greater than 1.")

        ### GNN to generate node embeddings
        if virtual_node:
            self.gnn_node = GNN_node_Virtualnode(num_layer, emb_dim, JK = JK, drop_ratio = drop_ratio, residual = residual, gnn_type = gnn_type)
        else:
            self.gnn_node = GNN_node(num_layer, emb_dim, JK = JK, drop_ratio = drop_ratio, residual = residual, gnn_type = gnn_type)


        ### Pooling function to generate whole-graph embeddings
        if self.graph_pooling == "sum":
            self.pool = global_add_pool
        elif self.graph_pooling == "mean":
            self.pool = global_mean_pool
        elif self.graph_pooling == "max":
            self.pool = global_max_pool
        elif self.graph_pooling == "attention":
            self.pool = GlobalAttention(gate_nn = torch.nn.Sequential(torch.nn.Linear(emb_dim, 2*emb_dim), torch.nn.BatchNorm1d(2*emb_dim), torch.nn.ReLU(), torch.nn.Linear(2*emb_dim, 1)))
        elif self.graph_pooling == "set2set":
            self.pool = Set2Set(emb_dim, processing_steps = 2)
        else:
            raise ValueError("Invalid graph pooling type.")

        self.graph_pred_linear=ModuleList()
        self.graph_norm=ModuleList()

        if graph_pooling == "set2set":
            self.graph_pred_linear.append(Linear(2*emb_dim, emb_dim))

        else:
            self.graph_pred_linear.append(Linear(emb_dim, emb_dim))


    def forward(self, batched_data):
        h_node = self.gnn_node(batched_data)

        h_graph = self.pool(h_node, batched_data.batch)

        return self.graph_pred_linear[0](h_graph)

class GNN_old(torch.nn.Module):

    def __init__(self, num_tasks, num_layer = 5, emb_dim = 100, 
                    gnn_type = 'gin', virtual_node = True, residual = False, drop_ratio = 0.5, JK = "last", graph_pooling = "sum"):
        '''
            num_tasks (int): number of labels to be predicted
            virtual_node (bool): whether to add virtual node or not
        '''

        super(GNN_old, self).__init__()

        self.num_layer = num_layer
        self.drop_ratio = drop_ratio
        self.JK = JK
        self.emb_dim = emb_dim
        self.num_tasks = num_tasks
        self.graph_pooling = graph_pooling

        if self.num_layer < 2:
            raise ValueError("Number of GNN layers must be greater than 1.")

        ### GNN to generate node embeddings
        if virtual_node:
            self.gnn_node = GNN_node_Virtualnode(num_layer, emb_dim, JK = JK, drop_ratio = drop_ratio, residual = residual, gnn_type = gnn_type)
        else:
            self.gnn_node = GNN_node_old(num_layer, emb_dim, JK = JK, drop_ratio = drop_ratio, residual = residual, gnn_type = gnn_type)


        ### Pooling function to generate whole-graph embeddings
        if self.graph_pooling == "sum":
            self.pool = global_add_pool
        elif self.graph_pooling == "mean":
            self.pool = global_mean_pool
        elif self.graph_pooling == "max":
            self.pool = global_max_pool
        elif self.graph_pooling == "attention":
            self.pool = GlobalAttention(gate_nn = torch.nn.Sequential(torch.nn.Linear(emb_dim, 2*emb_dim), torch.nn.BatchNorm1d(2*emb_dim), torch.nn.ReLU(), torch.nn.Linear(2*emb_dim, 1)))
        elif self.graph_pooling == "set2set":
            self.pool = Set2Set(emb_dim, processing_steps = 2)
        else:
            raise ValueError("Invalid graph pooling type.")

        self.graph_pred_linear=ModuleList()
        self.graph_norm=ModuleList()

        if graph_pooling == "set2set":
            self.graph_pred_linear.append(Linear(2*emb_dim, emb_dim))

        else:
            self.graph_pred_linear.append(Linear(emb_dim, emb_dim))


    def forward(self, batched_data):
        h_node = self.gnn_node(batched_data)

        h_graph = self.pool(h_node, batched_data.batch)

        return self.graph_pred_linear[0](h_graph)

class GNN_ex(torch.nn.Module):

    def __init__(self, num_tasks, num_layer = 5, emb_dim = 64, 
                    gnn_type = 'gin', virtual_node = True, residual = False, drop_ratio = 0.5, JK = "last", graph_pooling = "sum"):
        '''
            num_tasks (int): number of labels to be predicted
            virtual_node (bool): whether to add virtual node or not
        '''

        super(GNN_ex, self).__init__()

        self.num_layer = num_layer
        self.drop_ratio = drop_ratio
        self.JK = JK
        self.emb_dim = emb_dim
        self.num_tasks = num_tasks
        self.graph_pooling = graph_pooling

        if self.num_layer < 2:
            raise ValueError("Number of GNN layers must be greater than 1.")

        ### GNN to generate node embeddings
        if virtual_node:
            self.gnn_node = GNN_node_Virtualnode(num_layer, emb_dim, JK = JK, drop_ratio = drop_ratio, residual = residual, gnn_type = gnn_type)
        else:
            self.gnn_node = GNN_node_ex(num_layer, emb_dim, JK = JK, drop_ratio = drop_ratio, residual = residual, gnn_type = gnn_type)





        ### Pooling function to generate whole-graph embeddings
        if self.graph_pooling == "sum":
            self.pool = global_add_pool
        elif self.graph_pooling == "mean":
            self.pool = global_mean_pool
        elif self.graph_pooling == "max":
            self.pool = global_max_pool
        elif self.graph_pooling == "attention":
            self.pool = GlobalAttention(gate_nn = torch.nn.Sequential(torch.nn.Linear(emb_dim, 2*emb_dim), torch.nn.BatchNorm1d(2*emb_dim), torch.nn.ReLU(), torch.nn.Linear(2*emb_dim, 1)))
        elif self.graph_pooling == "set2set":
            self.pool = Set2Set(emb_dim, processing_steps = 2)
        else:
            raise ValueError("Invalid graph pooling type.")

        self.graph_pred_linear=ModuleList()
        self.graph_norm=ModuleList()

        if graph_pooling == "set2set":
            self.graph_pred_linear.append(Linear(2*emb_dim, emb_dim))

        else:
            self.graph_pred_linear.append(Linear(emb_dim, emb_dim))

        self.combined_mlp = ex_mlp(emb_dim)

    def forward(self, batched_data):
        ex_level = batched_data.len_longest_path
        ex_level = ex_level.reshape([ex_level.shape[0], 1])

        ex_ioratio = batched_data.io_ratio
        ex_ioratio = ex_ioratio.reshape([ex_level.shape[0], 1])


        h_node = self.gnn_node(batched_data)

        h_graph = self.pool(h_node, batched_data.batch)

        h_graph = self.graph_pred_linear[0](h_graph)

        combined_emb = self.combined_mlp(h_graph, ex_level, ex_ioratio)

        return combined_emb

class ex_mlp(nn.Module):
    def __init__(self, graph_emb):
        super(ex_mlp, self).__init__()

        self.level_lin1 = nn.Linear(1, graph_emb)
        self.level_norm1 = nn.BatchNorm1d(graph_emb)

        self.ioratio_lin1 = nn.Linear(1,graph_emb)
        self.ioratio_norm1 = nn.BatchNorm1d(graph_emb)

        self.combine_lin1 = nn.Linear(graph_emb*3, graph_emb)
        self.combine_norm1 = nn.BatchNorm1d(graph_emb)

    def forward(self, graph_emb, level, io_ratio):
        level = self.level_lin1(level)
        level = F.relu(self.level_norm1(level))
        level = F.dropout(level, p=0.5, training=self.training)

        io_ratio = self.ioratio_lin1(io_ratio)
        io_ratio = F.relu(self.ioratio_norm1(io_ratio))
        io_ratio = F.dropout(io_ratio, p=0.5, training=self.training)

        combine_emb = torch.concat((graph_emb, io_ratio, level), dim=-1)

        combine_emb = self.combine_lin1(combine_emb)
        combine_emb = F.relu(self.combine_norm1(combine_emb))
        combine_emb = F.dropout(combine_emb, p=0.5, training=self.training)
        return combine_emb


class GNN_Num(torch.nn.Module):

    def __init__(self, num_tasks, num_layer = 5, emb_dim = 64, 
                    gnn_type = 'gin', virtual_node = True, residual = False, drop_ratio = 0.5, JK = "last", graph_pooling = "sum"):
        '''
            num_tasks (int): number of labels to be predicted
            virtual_node (bool): whether to add virtual node or not
            GNN with logic level encoded
        '''

        super(GNN_Num, self).__init__()

        self.num_layer = num_layer
        self.drop_ratio = drop_ratio
        self.JK = JK
        self.emb_dim = emb_dim
        self.num_tasks = num_tasks
        self.graph_pooling = graph_pooling

        if self.num_layer < 2:
            raise ValueError("Number of GNN layers must be greater than 1.")

        ### GNN to generate node embeddings
        if virtual_node:
            self.gnn_node = GNN_node_Virtualnode(num_layer, emb_dim, JK = JK, drop_ratio = drop_ratio, residual = residual, gnn_type = gnn_type)
        else:
            self.gnn_node = GNN_node_ex(num_layer, emb_dim, JK = JK, drop_ratio = drop_ratio, residual = residual, gnn_type = gnn_type)

        ### Pooling function to generate whole-graph embeddings
        if self.graph_pooling == "sum":
            self.pool = global_add_pool
        elif self.graph_pooling == "mean":
            self.pool = global_mean_pool
        elif self.graph_pooling == "max":
            self.pool = global_max_pool
        elif self.graph_pooling == "attention":
            self.pool = GlobalAttention(gate_nn = torch.nn.Sequential(torch.nn.Linear(emb_dim, 2*emb_dim), torch.nn.BatchNorm1d(2*emb_dim), torch.nn.ReLU(), torch.nn.Linear(2*emb_dim, 1)))
        elif self.graph_pooling == "set2set":
            self.pool = Set2Set(emb_dim, processing_steps = 2)
        else:
            raise ValueError("Invalid graph pooling type.")

        self.graph_pred_linear=ModuleList()
        self.graph_norm=ModuleList()

        if graph_pooling == "set2set":
            self.graph_pred_linear.append(Linear(2*emb_dim, emb_dim))

        else:
            self.graph_pred_linear.append(Linear(emb_dim, emb_dim))

        self.combined_mlp = ConcatLinMLP(emb_dim)

    def forward(self, batched_data):
        num_nodes = [y - x for x,y in zip(batched_data.ptr,batched_data.ptr[1:])]

        num_nodes = torch.concat([i.reshape(1) for i in num_nodes])
        num_nodes = torch.reshape(num_nodes, (num_nodes.shape[0],1))

        h_node = self.gnn_node(batched_data)

        h_graph = self.pool(h_node, batched_data.batch)

        h_graph = self.graph_pred_linear[0](h_graph)

        combined_emb = self.combined_mlp(h_graph, num_nodes.float())

        return combined_emb

class GNN_LL(torch.nn.Module):

    def __init__(self, num_tasks, num_layer = 5, emb_dim = 64, 
                    gnn_type = 'gin', virtual_node = True, residual = False, drop_ratio = 0.5, JK = "last", graph_pooling = "sum"):
        '''
            num_tasks (int): number of labels to be predicted
            virtual_node (bool): whether to add virtual node or not
            GNN with logic level encoded
        '''

        super(GNN_LL, self).__init__()

        self.num_layer = num_layer
        self.drop_ratio = drop_ratio
        self.JK = JK
        self.emb_dim = emb_dim
        self.num_tasks = num_tasks
        self.graph_pooling = graph_pooling

        if self.num_layer < 2:
            raise ValueError("Number of GNN layers must be greater than 1.")

        ### GNN to generate node embeddings
        if virtual_node:
            self.gnn_node = GNN_node_Virtualnode(num_layer, emb_dim, JK = JK, drop_ratio = drop_ratio, residual = residual, gnn_type = gnn_type)
        else:
            self.gnn_node = GNN_node_ex(num_layer, emb_dim, JK = JK, drop_ratio = drop_ratio, residual = residual, gnn_type = gnn_type)

        ### Pooling function to generate whole-graph embeddings
        if self.graph_pooling == "sum":
            self.pool = global_add_pool
        elif self.graph_pooling == "mean":
            self.pool = global_mean_pool
        elif self.graph_pooling == "max":
            self.pool = global_max_pool
        elif self.graph_pooling == "attention":
            self.pool = GlobalAttention(gate_nn = torch.nn.Sequential(torch.nn.Linear(emb_dim, 2*emb_dim), torch.nn.BatchNorm1d(2*emb_dim), torch.nn.ReLU(), torch.nn.Linear(2*emb_dim, 1)))
        elif self.graph_pooling == "set2set":
            self.pool = Set2Set(emb_dim, processing_steps = 2)
        else:
            raise ValueError("Invalid graph pooling type.")

        self.graph_pred_linear=ModuleList()
        self.graph_norm=ModuleList()

        if graph_pooling == "set2set":
            self.graph_pred_linear.append(Linear(2*emb_dim, emb_dim))

        else:
            self.graph_pred_linear.append(Linear(emb_dim, emb_dim))

        self.combined_mlp = ConcatEmbedMLP(10000, emb_dim, emb_dim)

    def forward(self, batched_data):
        ex_level = batched_data.len_longest_path
        ex_level = ex_level.reshape([ex_level.shape[0], 1])
        h_node = self.gnn_node(batched_data)

        h_graph = self.pool(h_node, batched_data.batch)

        h_graph = self.graph_pred_linear[0](h_graph)

        combined_emb = self.combined_mlp(h_graph, ex_level.to(torch.int))

        return combined_emb


class ConcatEmbedMLP(nn.Module):
    def __init__(self, input_dim, embedding_dim, graph_linear_size):
        super().__init__()
        concat_size = (int((graph_linear_size+embedding_dim)//100)+1)*100
        self.embedding = nn.Embedding(input_dim, embedding_dim)
        self.concat_linear = nn.Linear(graph_linear_size+embedding_dim, concat_size)
        self.project_linear1 = nn.Linear(concat_size, graph_linear_size)
        self.project_linear2 = nn.Linear(graph_linear_size, graph_linear_size)
        self.batchnorm_concat = nn.BatchNorm1d(concat_size)
        self.batchnorm_1 = nn.BatchNorm1d(graph_linear_size)



    def forward(self, graph_embedding, discrete_tensor):
        discrete_embedding = self.embedding(discrete_tensor.squeeze())
        concatenated = torch.cat((graph_embedding, discrete_embedding), dim=-1)
        h = self.concat_linear(concatenated)
        h = self.batchnorm_concat(h)
        h = F.relu(h)
        h = self.project_linear1(h)
        h = self.batchnorm_1(h)
        h = F.relu(h)
        h = self.project_linear2(h)
        return h

class ConcatLinMLP(nn.Module):
    def __init__(self, embedding_dim):
        super().__init__()
        self.lin1 = nn.Linear(1, embedding_dim)
        self.lin2 = nn.Linear(embedding_dim, embedding_dim)
        self.norm_lin1 = nn.BatchNorm1d(embedding_dim)


        self.concat_linear = nn.Linear(embedding_dim+embedding_dim, embedding_dim*2)
        self.project_linear1 = nn.Linear(embedding_dim*2, embedding_dim)
        self.project_linear2 = nn.Linear(embedding_dim, embedding_dim)

        self.norm1 = nn.BatchNorm1d(embedding_dim*2)
        self.norm2 = nn.BatchNorm1d(embedding_dim)

    def forward(self, graph_embedding, discrete_tensor):
        discrete_lin = F.relu(self.norm_lin1(self.lin1(discrete_tensor)))
        discrete_lin = F.dropout(discrete_lin, p=0.4, training=self.training)
        discrete_lin = self.lin2(discrete_lin)

        concatenated = torch.cat((graph_embedding, discrete_lin), dim=-1)
        h = self.concat_linear(concatenated)
        h = F.relu(self.norm1(h))
        h = F.dropout(h, p=0.4, training=self.training)
        h = self.project_linear1(h)
        h = F.relu(self.norm2(h))
        h = F.dropout(h, p=0.4, training=self.training)
        h = self.project_linear2(h)
        return h

if __name__ == '__main__':
    GNN(num_tasks = 10)