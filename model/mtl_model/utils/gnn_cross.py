'''
This file is adapted from https://github.com/lydiawunan/LOSTIN/blob/main/GNN-LSTM/gnn.py, with multi task learning.
'''

import sys,os
sys.path.append(os.path.join(os.path.dirname("__file__"), './model/mtl_model/utils'))

import torch
import torch.nn as nn
from torch.nn import ReLU, Linear, BatchNorm1d, ModuleList
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import torch.nn.functional as F
from torch_geometric.nn import MessagePassing,BatchNorm
from torch_geometric.nn import global_add_pool, global_mean_pool, global_max_pool, GlobalAttention, Set2Set
import torch.nn.functional as F
from torch_geometric.nn.inits import uniform
from torch.nn import Sequential, ReLU, Linear, ModuleList
from torch_geometric.nn import global_mean_pool, global_add_pool
from node_encoder import NodeEncoder,EdgeEncoder
from conv_cross import GNN_node_cross, GNN_node_Virtualnode, GNN_node_MTAN, GNN_node_MTA
from conv_cross import mtl_attn, self_attn
from gnn import GNN
import copy


class GNN_Cross(torch.nn.Module):

    def __init__(self, num_tasks, num_layer = 5, emb_dim = 100, 
                    gnn_type = 'gin', virtual_node = True, residual = False, drop_ratio = 0.5, JK = "last", graph_pooling = "sum"):
        '''
            num_tasks (int): number of labels to be predicted
            virtual_node (bool): whether to add virtual node or not
        '''

        super(GNN_Cross, self).__init__()

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
            self.gnn_node = GNN_node_cross(num_layer, emb_dim, JK = JK, drop_ratio = drop_ratio, residual = residual, gnn_type = gnn_type)


        ### Pooling function to generate whole-graph embeddings
        if self.graph_pooling == "sum":
            self.pool_1 = global_add_pool
            self.pool_2 = global_add_pool
        elif self.graph_pooling == "mean":
            self.pool_1 = global_mean_pool
            self.pool_2 = global_mean_pool
        elif self.graph_pooling == "max":
            self.pool_1 = global_max_pool
            self.pool_2 = global_max_pool
        elif self.graph_pooling == "attention":
            self.pool_1 = GlobalAttention(gate_nn = torch.nn.Sequential(torch.nn.Linear(emb_dim, 2*emb_dim), torch.nn.BatchNorm1d(2*emb_dim), torch.nn.ReLU(), torch.nn.Linear(2*emb_dim, 1)))
            self.pool_2 = GlobalAttention(gate_nn = torch.nn.Sequential(torch.nn.Linear(emb_dim, 2*emb_dim), torch.nn.BatchNorm1d(2*emb_dim), torch.nn.ReLU(), torch.nn.Linear(2*emb_dim, 1)))
        elif self.graph_pooling == "set2set":
            self.pool_1 = Set2Set(emb_dim, processing_steps = 2)
            self.pool_2 = Set2Set(emb_dim, processing_steps = 2)
        else:
            raise ValueError("Invalid graph pooling type.")

        self.graph_pred_linear_1=ModuleList()
        self.graph_pred_linear_2=ModuleList()
        self.graph_norm=ModuleList()

        if graph_pooling == "set2set":
            self.graph_pred_linear.append(Linear(2*emb_dim, emb_dim))

        else:
            self.graph_pred_linear_1.append(Linear(emb_dim, emb_dim))
            self.graph_pred_linear_2.append(Linear(emb_dim, emb_dim))


    def forward(self, batched_data):
        h_node_1, h_node_2 = self.gnn_node(batched_data)

        h_graph_1 = self.pool_1(h_node_1, batched_data.batch)
        h_graph_2 = self.pool_2(h_node_2, batched_data.batch)

        return self.graph_pred_linear_1[0](h_graph_1), self.graph_pred_linear_2[0](h_graph_2)


class GNN_MTAN(torch.nn.Module):

    def __init__(self, num_tasks, num_layer = 5, emb_dim = 100, 
                    gnn_type = 'gin', virtual_node = True, residual = False, drop_ratio = 0.5, JK = "last", graph_pooling = "sum"):
        '''
            num_tasks (int): number of labels to be predicted
            virtual_node (bool): whether to add virtual node or not
        '''

        super(GNN_MTAN, self).__init__()

        self.num_layer = num_layer
        self.drop_ratio = drop_ratio
        self.JK = JK
        self.emb_dim = emb_dim
        self.num_tasks = num_tasks
        self.graph_pooling = graph_pooling

        if self.num_layer < 2:
            raise ValueError("Number of GNN layers must be greater than 1.")

        ### GNN to generate node embeddings

        self.gnn_node = GNN_node_MTAN(num_layer, emb_dim, JK = JK, drop_ratio = drop_ratio, residual = residual, gnn_type = gnn_type)


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

        self.graph_pred_linear_1=ModuleList()
        self.graph_pred_linear_2=ModuleList()
        self.graph_norm=ModuleList()

        if graph_pooling == "set2set":
            self.graph_pred_linear.append(Linear(2*emb_dim, emb_dim))

        else:
            self.graph_pred_linear_1.append(Linear(emb_dim, emb_dim))
            self.graph_pred_linear_2.append(Linear(emb_dim, emb_dim))


    def forward(self, batched_data):
        h_node_1, h_node_2 = self.gnn_node(batched_data)

        h_graph_1 = self.pool(h_node_1, batched_data.batch)
        h_graph_2 = self.pool(h_node_2, batched_data.batch)

        return self.graph_pred_linear_1[0](h_graph_1), self.graph_pred_linear_2[0](h_graph_2)


class GNN_MTA(torch.nn.Module):

    def __init__(self, num_tasks, num_heads = 2, num_layer = 5, emb_dim = 100, 
                    gnn_type = 'gin', virtual_node = True, residual = False, drop_ratio = 0.5, JK = "last", graph_pooling = "sum"):
        '''
            num_tasks (int): number of labels to be predicted
            virtual_node (bool): whether to add virtual node or not
        '''

        super(GNN_MTA, self).__init__()

        self.num_layer = num_layer
        self.drop_ratio = drop_ratio
        self.JK = JK
        self.emb_dim = emb_dim
        self.num_tasks = num_tasks
        self.graph_pooling = graph_pooling

        if self.num_layer < 2:
            raise ValueError("Number of GNN layers must be greater than 1.")

        ### GNN to generate node embeddings

        self.gnn_node = GNN_node_MTA(num_layer, emb_dim, num_heads = num_heads, JK = JK, drop_ratio = drop_ratio, residual = residual, gnn_type = gnn_type)


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

        self.graph_pred_linear_1=ModuleList()
        self.graph_pred_linear_2=ModuleList()
        self.graph_norm=ModuleList()

        if graph_pooling == "set2set":
            self.graph_pred_linear.append(Linear(2*emb_dim, emb_dim))

        else:
            self.graph_pred_linear_1.append(Linear(emb_dim, emb_dim))
            self.graph_pred_linear_2.append(Linear(emb_dim, emb_dim))


    def forward(self, batched_data):
        h_node_1, h_node_2 = self.gnn_node(batched_data)

        h_graph_1 = self.pool(h_node_1, batched_data.batch)
        h_graph_2 = self.pool(h_node_2, batched_data.batch)

        return self.graph_pred_linear_1[0](h_graph_1), self.graph_pred_linear_2[0](h_graph_2)

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

class GNN_MTA_EX(torch.nn.Module):

    def __init__(self, num_tasks, num_heads = 2, num_layer = 5, emb_dim = 100, 
                    gnn_type = 'gin', virtual_node = True, residual = False, drop_ratio = 0.5, JK = "last", graph_pooling = "sum"):
        '''
            num_tasks (int): number of labels to be predicted
            virtual_node (bool): whether to add virtual node or not
        '''

        super(GNN_MTA_EX, self).__init__()

        self.num_layer = num_layer
        self.drop_ratio = drop_ratio
        self.JK = JK
        self.emb_dim = emb_dim
        self.num_tasks = num_tasks
        self.graph_pooling = graph_pooling

        if self.num_layer < 2:
            raise ValueError("Number of GNN layers must be greater than 1.")

        ### GNN to generate node embeddings

        self.gnn_node = GNN_node_MTA(num_layer, emb_dim, num_heads = num_heads, JK = JK, drop_ratio = drop_ratio, residual = residual, gnn_type = gnn_type)


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

        self.graph_pred_linear_1=ModuleList()
        self.graph_pred_linear_2=ModuleList()
        self.graph_norm=ModuleList()

        if graph_pooling == "set2set":
            self.graph_pred_linear.append(Linear(2*emb_dim, emb_dim))

        else:
            self.graph_pred_linear_1.append(Linear(emb_dim, emb_dim))
            self.graph_pred_linear_2.append(Linear(emb_dim, emb_dim))

        self.combined_mlp1 = ex_mlp(emb_dim)
        self.combined_mlp2 = ex_mlp(emb_dim)

    def forward(self, batched_data):


        h_node_1, h_node_2 = self.gnn_node(batched_data)

        h_graph_1 = self.pool(h_node_1, batched_data.batch)
        h_graph_2 = self.pool(h_node_2, batched_data.batch)

        h_graph_1 = self.graph_pred_linear_1[0](h_graph_1)
        h_graph_2 = self.graph_pred_linear_2[0](h_graph_2)

        #combine ex feature
        ex_level = batched_data.len_longest_path
        ex_level = ex_level.reshape([ex_level.shape[0], 1])

        ex_ioratio = batched_data.io_ratio
        ex_ioratio = ex_ioratio.reshape([ex_level.shape[0], 1])

        combined_emb1 = self.combined_mlp1(h_graph_1, ex_level, ex_ioratio)
        combined_emb2 = self.combined_mlp2(h_graph_2, ex_level, ex_ioratio)

        return combined_emb1, combined_emb2


class Hybridmodel_Cross(nn.Module):
    def __init__(self, input_dim, emb_dim, num_layer =2, layers =2 ,hidden_dim=64, graph_emb=11):
        super(Hybridmodel_Cross, self).__init__()

        self.embedding1 = nn.Embedding(input_dim, emb_dim)
        self.embedding2 = nn.Embedding(input_dim, emb_dim)

        self.lstm1 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)
        self.lstm2 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)
        self.gmodel = GNN_Cross(gnn_type = 'gin', num_tasks = 1, num_layer = layers, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)

        self.linear_a=ModuleList()
        self.linear_a.append(Linear(hidden_dim + graph_emb, 100))
        self.linear_a.append(Linear(100,100))
        self.linear_a.append(Linear(100,1))

        self.norm_a=ModuleList()
        self.norm_a.append(BatchNorm1d(100))
        self.norm_a.append(BatchNorm1d(100))

        self.linear_d=ModuleList()
        self.linear_d.append(Linear(hidden_dim + graph_emb, 100))
        self.linear_d.append(Linear(100,100))
        self.linear_d.append(Linear(100,1))

        self.norm_d=ModuleList()
        self.norm_d.append(BatchNorm1d(100))
        self.norm_d.append(BatchNorm1d(100))

        #cross units
        num_cross = len(self.linear_a) - 1
        self.cross_unit = nn.Parameter(data = torch.ones(num_cross,2,2)/2)

    def forward(self, text, text_len, graph_batch):
        text_emb1 = self.embedding1(text)
        text_emb2 = self.embedding2(text)

        packed_input1 = pack_padded_sequence(text_emb1, text_len, batch_first=True, enforce_sorted=False)
        packed_input2 = pack_padded_sequence(text_emb2, text_len, batch_first=True, enforce_sorted=False)
        packed_output1, _ = self.lstm1(packed_input1)
        packed_output2, _ = self.lstm2(packed_input2)
        output1, _ = pad_packed_sequence(packed_output1, batch_first=True)
        output2, _ = pad_packed_sequence(packed_output2, batch_first=True)

        out1 = output1[:, -1, :]
        out2 = output2[:, -1, :]
        g_emb_d, g_emb_a = self.gmodel(graph_batch)
        combined_emb_d = torch.cat((out1, g_emb_d[text[:,0]-7]),1)
        combined_emb_a = torch.cat((out2, g_emb_a[text[:,0]-7]),1)


        feat_d=F.relu(self.linear_d[0](combined_emb_d))
        feat_d=self.norm_d[0](feat_d)
        feat_a=F.relu(self.linear_a[0](combined_emb_a))
        feat_a=self.norm_a[0](feat_a)

        feat_a=F.dropout(feat_a,p=0.4,training=self.training)
        feat_d=F.dropout(feat_d,p=0.4,training=self.training)

        feat_d = self.cross_unit[0][0][0]*feat_d + self.cross_unit[0][0][1]*feat_a
        feat_a = self.cross_unit[0][1][0]*feat_d + self.cross_unit[0][1][1]*feat_a

        #FC2
        feat_d=F.relu(self.linear_d[1](feat_d))
        feat_d=self.norm_d[1](feat_d)
        feat_a=F.relu(self.linear_a[1](feat_a))
        feat_a=self.norm_a[1](feat_a)


        feat_d=F.dropout(feat_d,p=0.4,training=self.training)
        feat_a=F.dropout(feat_a,p=0.4,training=self.training)


        feat_d = self.cross_unit[1][0][0]*feat_d + self.cross_unit[1][0][1]*feat_a
        feat_a = self.cross_unit[1][1][0]*feat_d + self.cross_unit[1][1][1]*feat_a


        #FC3
        out_a=self.linear_a[2](feat_a)
        out_a = torch.squeeze(out_a, 1)

        out_d=self.linear_d[2](feat_d)
        out_d = torch.squeeze(out_d, 1)

        return out_d, out_a

    def init_cross(self, a_specific, a_different):
        for idx in range(len(self.cross_unit)):
            self.cross_unit[idx][0][0].data.fill_(a_specific)
            self.cross_unit[idx][1][1].data.fill_(a_specific)
            self.cross_unit[idx][0][1].data.fill_(a_different)  
            self.cross_unit[idx][1][0].data.fill_(a_different)

        for idx in range(len(self.gmodel.gnn_node.cross_unit)):
            self.gmodel.gnn_node.cross_unit[idx][0][0].data.fill_(a_specific)    
            self.gmodel.gnn_node.cross_unit[idx][1][1].data.fill_(a_specific)   
            self.gmodel.gnn_node.cross_unit[idx][0][1].data.fill_(a_different)    
            self.gmodel.gnn_node.cross_unit[idx][1][0].data.fill_(a_different)


    def init_pretrain(self, load_pathd, load_patha, device):
        state_dict_d = torch.load(load_pathd, map_location=device)['model_state_dict']
        state_dict_a = torch.load(load_patha, map_location=device)['model_state_dict']

        self_model_dict = self.state_dict()
        self_model_dict['embedding1.weight']=state_dict_d['embedding.weight']
        self_model_dict['embedding2.weight']=state_dict_a['embedding.weight']

        model_dict_store = {}
        for name, param in self.named_parameters():
            if param.requires_grad:
                model_dict_store[name] = param
        #lstm
        self_model_dict_bak = copy.deepcopy(model_dict_store)

        for k in self_model_dict.keys():
            if k.startswith('embedding1'):
                name = k.split('.', 1)[-1]
                self_model_dict[k] = state_dict_d['embedding.'+name]
            elif k.startswith('embedding2'):
                name = k.split('.', 1)[-1]
                self_model_dict[k] = state_dict_a['embedding.'+name]

            if k.startswith('lstm1'):
                name = k.split('.', 1)[-1]
                self_model_dict[k] = state_dict_d['lstm.'+name]
            elif k.startswith('lstm2'):
                name = k.split('.', 1)[-1]
                self_model_dict[k] = state_dict_a['lstm.'+name]

            if k.startswith('gmodel.gnn_node.node_encoder_1'):
                name = k.split('.', 3)[-1]
                self_model_dict[k] = state_dict_d['gmodel.gnn_node.node_encoder.'+name]
            elif k.startswith('gmodel.gnn_node.node_encoder_2'):
                name = k.split('.', 3)[-1]
                self_model_dict[k] = state_dict_a['gmodel.gnn_node.node_encoder.'+name]

            if k.startswith('gmodel.gnn_node.shared_convs_1'):
                name = k.split('.', 3)[-1]
                self_model_dict[k] = state_dict_d['gmodel.gnn_node.convs.'+name]
            elif k.startswith('gmodel.gnn_node.shared_convs_2'):
                name = k.split('.', 3)[-1]
                self_model_dict[k] = state_dict_a['gmodel.gnn_node.convs.'+name]


            if k.startswith('gmodel.gnn_node.shared_batch_norms_1'):
                name = k.split('.', 3)[-1]
                self_model_dict[k] = state_dict_d['gmodel.gnn_node.batch_norms.'+name]
            elif k.startswith('gmodel.gnn_node.shared_batch_norms_2'):
                name = k.split('.', 3)[-1]
                self_model_dict[k] = state_dict_a['gmodel.gnn_node.batch_norms.'+name]

            if k.startswith('gmodel.graph_pred_linear_1'):
                name = k.split('.', 2)[-1]
                self_model_dict[k] = state_dict_d['gmodel.graph_pred_linear.'+name]
            elif k.startswith('gmodel.graph_pred_linear_2'):
                name = k.split('.', 2)[-1]
                self_model_dict[k] = state_dict_a['gmodel.graph_pred_linear.'+name]

            if k.startswith('linear_d'):
                name = k.split('.', 1)[-1]
                self_model_dict[k] = state_dict_d['linear.'+name]
            elif k.startswith('linear_a'):
                name = k.split('.', 1)[-1]
                self_model_dict[k] = state_dict_a['linear.'+name]

            if k.startswith('norm_d'):
                name = k.split('.', 1)[-1]
                self_model_dict[k] = state_dict_d['norm.'+name]
            elif k.startswith('norm_a'):
                name = k.split('.', 1)[-1]
                self_model_dict[k] = state_dict_a['norm.'+name]

        self.load_state_dict(self_model_dict)
        for k in self_model_dict_bak.keys():
            if torch.equal(self_model_dict_bak[k], self_model_dict[k]):
                print('Not got init {}'.format(k))




class Hybridmodel_Cross_Sep(nn.Module):
    def __init__(self, input_dim, emb_dim, num_layer =2, layers =2 ,hidden_dim=64, graph_emb=11):
        super(Hybridmodel_Cross_Sep, self).__init__()

        self.embedding1 = nn.Embedding(input_dim, emb_dim)
        self.embedding2 = nn.Embedding(input_dim, emb_dim)

        self.lstm1 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)
        self.lstm2 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)
        self.gmodel = GNN_Cross(gnn_type = 'gin', num_tasks = 1, num_layer = layers, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)


        linear_size = int((((hidden_dim + graph_emb)//100)+1)*100)

        self.MLP_group_d = MLP_Group(hidden_dim + graph_emb, linear_size)
        self.MLP_group_a = MLP_Group(hidden_dim + graph_emb, linear_size)
        self.Classify_d = PredClass(hidden_dim + graph_emb, linear_size)
        self.Classify_a = PredClass(hidden_dim + graph_emb, linear_size)

    def forward(self, text, text_len, graph_batch, train_mask):
        text_emb1 = self.embedding1(text)
        text_emb2 = self.embedding2(text)

        packed_input1 = pack_padded_sequence(text_emb1, text_len, batch_first=True, enforce_sorted=False)
        packed_input2 = pack_padded_sequence(text_emb2, text_len, batch_first=True, enforce_sorted=False)
        packed_output1, _ = self.lstm1(packed_input1)
        packed_output2, _ = self.lstm2(packed_input2)
        output1, _ = pad_packed_sequence(packed_output1, batch_first=True)
        output2, _ = pad_packed_sequence(packed_output2, batch_first=True)

        out1 = output1[:, -1, :]
        out2 = output2[:, -1, :]

        g_emb_d, g_emb_a = self.gmodel(graph_batch)
        combined_emb_d = torch.cat((out1, g_emb_d[text[:,0]-7]),1)
        combined_emb_a = torch.cat((out2, g_emb_a[text[:,0]-7]),1)


        MLP_out_d = self.MLP_group_d(combined_emb_d)
        MLP_out_a = self.MLP_group_a(combined_emb_a)
        class_out_d = self.Classify_d(combined_emb_d)
        class_out_a = self.Classify_d(combined_emb_a)
        return MLP_out_d, MLP_out_a, class_out_d, class_out_a


    def init_cross(self, a_specific, a_different):


        for idx in range(len(self.gmodel.gnn_node.cross_unit)):
            self.gmodel.gnn_node.cross_unit[idx][0][0].data.fill_(a_specific)    
            self.gmodel.gnn_node.cross_unit[idx][1][1].data.fill_(a_specific)   
            self.gmodel.gnn_node.cross_unit[idx][0][1].data.fill_(a_different)    
            self.gmodel.gnn_node.cross_unit[idx][1][0].data.fill_(a_different)


class Hybridmodel_MTA(nn.Module):
    def __init__(self, input_dim, emb_dim, num_heads =2, layers =2 ,hidden_dim=64, graph_emb=11):
        super(Hybridmodel_MTA, self).__init__()

        self.embedding = nn.Embedding(input_dim, emb_dim)
        self.lstm1 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)
        self.lstm2 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)

        self.gmodel = GNN_MTA(gnn_type = 'gin', num_tasks = 1, num_layer = layers, num_heads = num_heads, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)

        self.linear_a=ModuleList()
        self.linear_a.append(Linear(hidden_dim + graph_emb, 100))
        self.linear_a.append(Linear(100,100))
        self.linear_a.append(Linear(100,1))

        self.norm_a=ModuleList()
        self.norm_a.append(BatchNorm1d(100))
        self.norm_a.append(BatchNorm1d(100))

        self.linear_d=ModuleList()
        self.linear_d.append(Linear(hidden_dim + graph_emb, 100))
        self.linear_d.append(Linear(100,100))
        self.linear_d.append(Linear(100,1))

        self.norm_d=ModuleList()
        self.norm_d.append(BatchNorm1d(100))
        self.norm_d.append(BatchNorm1d(100))

        self.attn1 =ModuleList()
        self.attn2 = ModuleList()

        for idx in range(2):
            self.attn1.append(mtl_attn(emb_dim=100, num_tasks=2, num_heads = 2))
            self.attn2.append(mtl_attn(emb_dim=100, num_tasks=2, num_heads = 2))

    def forward(self, text, text_len, graph_batch):
        text_emb = self.embedding(text)

        packed_input = pack_padded_sequence(text_emb, text_len, batch_first=True, enforce_sorted=False)
        packed_output1, _ = self.lstm1(packed_input)
        packed_output2, _ = self.lstm2(packed_input)
        output1, _ = pad_packed_sequence(packed_output1, batch_first=True)
        output2, _ = pad_packed_sequence(packed_output2, batch_first=True)

        out1 = output1[:, -1, :]
        out2 = output2[:, -1, :]

        g_emb_d, g_emb_a = self.gmodel(graph_batch)
        combined_emb_d = torch.cat((out1, g_emb_d[text[:,0]-7]),1)
        combined_emb_a = torch.cat((out2, g_emb_a[text[:,0]-7]),1)


        #FC1
        feat_a=F.relu(self.linear_a[0](combined_emb_a))
        feat_a=self.norm_a[0](feat_a)
        feat_d=F.relu(self.linear_d[0](combined_emb_d))
        feat_d=self.norm_d[0](feat_d)

        #attn first layer here
        feat_d = self.attn1[0]([feat_d, feat_a], 0)
        feat_a = self.attn2[0]([feat_d, feat_a], 1)

        feat_a=F.dropout(feat_a,p=0.4,training=self.training)
        feat_d=F.dropout(feat_d,p=0.4,training=self.training)


        #FC2
        feat_a=F.relu(self.linear_a[1](feat_a))
        feat_a=self.norm_a[1](feat_a)

        feat_d=F.relu(self.linear_d[1](feat_d))
        feat_d=self.norm_d[1](feat_d)

        #attn secode layer here
        feat_d = self.attn1[1]([feat_d, feat_a], 0)
        feat_a = self.attn2[1]([feat_d, feat_a], 1)

        feat_a=F.dropout(feat_a,p=0.4,training=self.training)
        feat_d=F.dropout(feat_d,p=0.4,training=self.training)

        #FC3
        out_a=self.linear_a[2](feat_a)
        out_a = torch.squeeze(out_a, 1)

        out_d=self.linear_d[2](feat_d)
        out_d = torch.squeeze(out_d, 1)

        return out_d, out_a

class Hybridmodel_MTA_sep(nn.Module):
    def __init__(self, input_dim, emb_dim, num_heads =2, layers =2 ,hidden_dim=64, graph_emb=11):
        super(Hybridmodel_MTA_sep, self).__init__()

        self.embedding1 = nn.Embedding(input_dim, emb_dim)
        self.embedding2 = nn.Embedding(input_dim, emb_dim)
        self.lstm1 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)
        self.lstm2 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)

        self.gmodel = GNN_MTA(gnn_type = 'gin', num_tasks = 1, num_layer = layers, num_heads = num_heads, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)

        linear_size = int((((hidden_dim + graph_emb)//100)+1)*100)
        self.MLP_group_d = MLP_Group(hidden_dim + graph_emb, linear_size)
        self.MLP_group_a = MLP_Group(hidden_dim + graph_emb, linear_size)
        self.Classify_d = PredClass(hidden_dim + graph_emb, linear_size)
        self.Classify_a = PredClass(hidden_dim + graph_emb, linear_size)

        self.attn1 =ModuleList()
        self.attn2 = ModuleList()

        for idx in range(2):
            self.attn1.append(mtl_attn(emb_dim=hidden_dim + graph_emb, num_tasks=2, num_heads = num_heads))
            self.attn2.append(mtl_attn(emb_dim=hidden_dim + graph_emb, num_tasks=2, num_heads = num_heads))

    def forward(self, text, text_len, graph_batch, mask):

        text_emb1 = self.embedding1(text)
        text_emb2 = self.embedding2(text)

        packed_input1 = pack_padded_sequence(text_emb1, text_len, batch_first=True, enforce_sorted=False)
        packed_input2 = pack_padded_sequence(text_emb2, text_len, batch_first=True, enforce_sorted=False)
        packed_output1, _ = self.lstm1(packed_input1)
        packed_output2, _ = self.lstm2(packed_input2)
        output1, _ = pad_packed_sequence(packed_output1, batch_first=True)
        output2, _ = pad_packed_sequence(packed_output2, batch_first=True)

        out1 = output1[:, -1, :]
        out2 = output2[:, -1, :]

        g_emb_d, g_emb_a = self.gmodel(graph_batch)
        combined_emb_d = torch.cat((out1, g_emb_d[text[:,0]-7]),1)
        combined_emb_a = torch.cat((out2, g_emb_a[text[:,0]-7]),1)

        #put attn here
        atten_emb_list_d = []
        atten_emb_list_a = []

        atten_emb_list_d.append(torch.reshape(combined_emb_d, (combined_emb_d.shape[0], 1, combined_emb_d.shape[1])))
        atten_emb_list_a.append(torch.reshape(combined_emb_a, (combined_emb_a.shape[0], 1, combined_emb_a.shape[1])))

        for idx in range(len(self.attn1)):
            atten_emb_list_d.append(self.attn1[idx]([atten_emb_list_d[idx], atten_emb_list_a[idx]], 0))
            atten_emb_list_a.append(self.attn2[idx]([atten_emb_list_d[idx], atten_emb_list_a[idx]], 1))

        atten_out_d = torch.reshape(atten_emb_list_d[-1], (atten_emb_list_d[-1].shape[0], atten_emb_list_d[-1].shape[2]))
        atten_out_a = torch.reshape(atten_emb_list_a[-1], (atten_emb_list_a[-1].shape[0], atten_emb_list_a[-1].shape[2]))

        #FC1
        MLP_out_d = self.MLP_group_d(atten_out_d)
        MLP_out_a = self.MLP_group_a(atten_out_a)
        class_out_d = self.Classify_d(atten_out_d)
        class_out_a = self.Classify_d(atten_out_a)
        return MLP_out_d, MLP_out_a, class_out_d, class_out_a

        return out_d, out_a

class Hybridmodel_MTA_sep_EX(nn.Module):
    def __init__(self, input_dim, emb_dim, num_heads =2, layers =2 ,hidden_dim=64, graph_emb=11):
        super(Hybridmodel_MTA_sep_EX, self).__init__()

        self.embedding1 = nn.Embedding(input_dim, emb_dim)
        self.embedding2 = nn.Embedding(input_dim, emb_dim)
        self.lstm1 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)
        self.lstm2 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)

        self.gmodel = GNN_MTA(gnn_type = 'gin', num_tasks = 1, num_layer = layers, num_heads = num_heads, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)

        linear_size = int((((hidden_dim + graph_emb)//100)+1)*100)
        self.linear_a=ModuleList()
        self.linear_a.append(Linear(hidden_dim + graph_emb, linear_size))
        self.linear_a.append(Linear(linear_size,linear_size))
        self.linear_a.append(Linear(linear_size,1))

        self.norm_a=ModuleList()
        self.norm_a.append(BatchNorm1d(linear_size))
        self.norm_a.append(BatchNorm1d(linear_size))

        self.linear_d=ModuleList()
        self.linear_d.append(Linear(hidden_dim + graph_emb, linear_size))
        self.linear_d.append(Linear(linear_size,linear_size))
        self.linear_d.append(Linear(linear_size,1))

        self.norm_d=ModuleList()
        self.norm_d.append(BatchNorm1d(linear_size))
        self.norm_d.append(BatchNorm1d(linear_size))

        self.attn1 =ModuleList()
        self.attn2 = ModuleList()

        for idx in range(2):
            self.attn1.append(mtl_attn(emb_dim=hidden_dim + graph_emb, num_tasks=2, num_heads = 2))
            self.attn2.append(mtl_attn(emb_dim=hidden_dim + graph_emb, num_tasks=2, num_heads = 2))

        self.exMLP = ConcatEmbedMLP(hidden_dim + graph_emb)

    def forward(self, text, text_len, graph_batch, mask):
        text_emb1 = self.embedding1(text)
        text_emb2 = self.embedding2(text)

        packed_input_1 = pack_padded_sequence(text_emb1, text_len, batch_first=True, enforce_sorted=False)
        packed_input_2 = pack_padded_sequence(text_emb2, text_len, batch_first=True, enforce_sorted=False)
        packed_output1, _ = self.lstm1(packed_input_1)
        packed_output2, _ = self.lstm2(packed_input_2)
        output1, _ = pad_packed_sequence(packed_output1, batch_first=True)
        output2, _ = pad_packed_sequence(packed_output2, batch_first=True)

        out1 = output1[:, -1, :]
        out2 = output2[:, -1, :]

        g_emb_d, g_emb_a = self.gmodel(graph_batch)
        combined_emb_d = torch.cat((out1, g_emb_d[text[:,0]-7]),1)
        combined_emb_a = torch.cat((out2, g_emb_a[text[:,0]-7]),1)


        #put attn here
        for idx in range(len(self.attn1)):
            combined_emb_d = self.attn1[idx]([combined_emb_d, combined_emb_a], 0)
            combined_emb_a = self.attn2[idx]([combined_emb_d, combined_emb_a], 1)

        ex_info = graph_batch.len_longest_path

        ex_info = ex_info.reshape([ex_info.shape[0], 1])
        ex_info = ex_info[text[:,0]-7]

        combined_emb_d = self.exMLP(combined_emb_d, ex_info.int())



        #FC1
        feat_a=F.relu(self.linear_a[0](combined_emb_a))
        feat_a=self.norm_a[0](feat_a)
        feat_d=F.relu(self.linear_d[0](combined_emb_d))
        feat_d=self.norm_d[0](feat_d)


        feat_a=F.dropout(feat_a,p=0.4,training=self.training)
        feat_d=F.dropout(feat_d,p=0.4,training=self.training)

        #FC2
        feat_a=F.relu(self.linear_a[1](feat_a))
        feat_a=self.norm_a[1](feat_a)

        feat_d=F.relu(self.linear_d[1](feat_d))
        feat_d=self.norm_d[1](feat_d)


        feat_a=F.dropout(feat_a,p=0.4,training=self.training)
        feat_d=F.dropout(feat_d,p=0.4,training=self.training)

        #FC3
        out_a=self.linear_a[2](feat_a)
        out_a = torch.squeeze(out_a, 1)

        out_d=self.linear_d[2](feat_d)
        out_d = torch.squeeze(out_d, 1)

        return out_d, out_a

class Hybridmodel_MTA_sep_ExProj(nn.Module):
    def __init__(self, input_dim, emb_dim, num_heads =2, layers =2 ,hidden_dim=64, graph_emb=11):
        super(Hybridmodel_MTA_sep_ExProj, self).__init__()

        self.embedding1 = nn.Embedding(input_dim, emb_dim)
        self.embedding2 = nn.Embedding(input_dim, emb_dim)
        self.lstm1 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)
        self.lstm2 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)

        self.gmodel = GNN_MTA(gnn_type = 'gin', num_tasks = 1, num_layer = layers, num_heads = num_heads, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)

        linear_size = int((((hidden_dim + graph_emb)//100)+1)*100)
        self.linear_a=ModuleList()
        self.linear_a.append(Linear(hidden_dim + graph_emb, linear_size))
        self.linear_a.append(Linear(linear_size,linear_size))
        self.linear_a.append(Linear(linear_size,1))

        self.norm_a=ModuleList()
        self.norm_a.append(BatchNorm1d(linear_size))
        self.norm_a.append(BatchNorm1d(linear_size))

        self.linear_d=ModuleList()
        self.linear_d.append(Linear(hidden_dim + graph_emb, linear_size))
        self.linear_d.append(Linear(linear_size,linear_size))
        self.linear_d.append(Linear(linear_size,1))

        self.norm_d=ModuleList()
        self.norm_d.append(BatchNorm1d(linear_size))
        self.norm_d.append(BatchNorm1d(linear_size))

        self.attn1 =ModuleList()
        self.attn2 = ModuleList()

        for idx in range(2):
            self.attn1.append(mtl_attn(emb_dim=hidden_dim + graph_emb, num_tasks=2, num_heads = 2))
            self.attn2.append(mtl_attn(emb_dim=hidden_dim + graph_emb, num_tasks=2, num_heads = 2))

        self.exMLP = ConcatEmbedMLP(hidden_dim + graph_emb)
        self.projMLP = ConcatLinMLP(hidden_dim + graph_emb)

    def forward(self, text, text_len, graph_batch, mask):
        text_emb1 = self.embedding1(text)
        text_emb2 = self.embedding2(text)

        packed_input_1 = pack_padded_sequence(text_emb1, text_len, batch_first=True, enforce_sorted=False)
        packed_input_2 = pack_padded_sequence(text_emb2, text_len, batch_first=True, enforce_sorted=False)
        packed_output1, _ = self.lstm1(packed_input_1)
        packed_output2, _ = self.lstm2(packed_input_2)
        output1, _ = pad_packed_sequence(packed_output1, batch_first=True)
        output2, _ = pad_packed_sequence(packed_output2, batch_first=True)

        out1 = output1[:, -1, :]
        out2 = output2[:, -1, :]

        g_emb_d, g_emb_a = self.gmodel(graph_batch)
        combined_emb_d = torch.cat((out1, g_emb_d[text[:,0]-7]),1)
        combined_emb_a = torch.cat((out2, g_emb_a[text[:,0]-7]),1)

        #put attn here
        for idx in range(len(self.attn1)):
            combined_emb_d = self.attn1[idx]([combined_emb_d, combined_emb_a], 0)
            combined_emb_a = self.attn2[idx]([combined_emb_d, combined_emb_a], 1)

        ex_info = graph_batch.len_longest_path

        ex_info = ex_info.reshape([ex_info.shape[0], 1])
        ex_info = ex_info[text[:,0]-7]

        combined_emb_d = self.exMLP(combined_emb_d, ex_info.int())

        #add a MLP for area also
        num_nodes = [y - x for x,y in zip(graph_batch.ptr,graph_batch.ptr[1:])]

        num_nodes = torch.concat([i.reshape(1) for i in num_nodes])
        num_nodes = torch.reshape(num_nodes, (num_nodes.shape[0],1))
        num_nodes = num_nodes[text[:,0]-7]

        combined_emb_a = self.projMLP(combined_emb_a, num_nodes.to(torch.float32))

        #FC1
        feat_a=F.relu(self.linear_a[0](combined_emb_a))
        feat_a=self.norm_a[0](feat_a)
        feat_d=F.relu(self.linear_d[0](combined_emb_d))
        feat_d=self.norm_d[0](feat_d)


        feat_a=F.dropout(feat_a,p=0.4,training=self.training)
        feat_d=F.dropout(feat_d,p=0.4,training=self.training)

        #FC2
        feat_a=F.relu(self.linear_a[1](feat_a))
        feat_a=self.norm_a[1](feat_a)

        feat_d=F.relu(self.linear_d[1](feat_d))
        feat_d=self.norm_d[1](feat_d)


        feat_a=F.dropout(feat_a,p=0.4,training=self.training)
        feat_d=F.dropout(feat_d,p=0.4,training=self.training)

        #FC3
        out_a=self.linear_a[2](feat_a)
        out_a = torch.squeeze(out_a, 1)

        out_d=self.linear_d[2](feat_d)
        out_d = torch.squeeze(out_d, 1)

        return out_d, out_a

class Hybridmodel_MTA_sep_ExEmb(nn.Module):
    def __init__(self, input_dim, emb_dim, num_heads =2, layers =2 ,hidden_dim=64, graph_emb=11):
        super(Hybridmodel_MTA_sep_ExEmb, self).__init__()

        self.embedding1 = nn.Embedding(input_dim, emb_dim)
        self.embedding2 = nn.Embedding(input_dim, emb_dim)
        self.lstm1 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)
        self.lstm2 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)

        self.gmodel = GNN_MTA(gnn_type = 'gin', num_tasks = 1, num_layer = layers, num_heads = num_heads, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)

        linear_size = int((((hidden_dim + graph_emb)//100)+1)*100)
        self.linear_a=ModuleList()
        self.linear_a.append(Linear(hidden_dim + graph_emb, linear_size))
        self.linear_a.append(Linear(linear_size,linear_size))
        self.linear_a.append(Linear(linear_size,1))

        self.norm_a=ModuleList()
        self.norm_a.append(BatchNorm1d(linear_size))
        self.norm_a.append(BatchNorm1d(linear_size))

        self.linear_d=ModuleList()
        self.linear_d.append(Linear(hidden_dim + graph_emb, linear_size))
        self.linear_d.append(Linear(linear_size,linear_size))
        self.linear_d.append(Linear(linear_size,1))

        self.norm_d=ModuleList()
        self.norm_d.append(BatchNorm1d(linear_size))
        self.norm_d.append(BatchNorm1d(linear_size))

        self.attn1 =ModuleList()
        self.attn2 = ModuleList()

        for idx in range(2):
            self.attn1.append(mtl_attn(emb_dim=hidden_dim + graph_emb, num_tasks=2, num_heads = 2))
            self.attn2.append(mtl_attn(emb_dim=hidden_dim + graph_emb, num_tasks=2, num_heads = 2))

        self.exMLP = ConcatEmbedMLP(10000, hidden_dim + graph_emb)
        self.NumMLP = ConcatEmbedMLP(150000, hidden_dim + graph_emb)

    def forward(self, text, text_len, graph_batch, mask):
        text_emb1 = self.embedding1(text[:,1:])
        text_emb2 = self.embedding2(text[:,1:])

        packed_input_1 = pack_padded_sequence(text_emb1, text_len-1, batch_first=True, enforce_sorted=False)
        packed_input_2 = pack_padded_sequence(text_emb2, text_len-1, batch_first=True, enforce_sorted=False)
        packed_output1, _ = self.lstm1(packed_input_1)
        packed_output2, _ = self.lstm2(packed_input_2)
        output1, _ = pad_packed_sequence(packed_output1, batch_first=True)
        output2, _ = pad_packed_sequence(packed_output2, batch_first=True)

        out1 = output1[:, -1, :]
        out2 = output2[:, -1, :]

        g_emb_d, g_emb_a = self.gmodel(graph_batch)
        combined_emb_d = torch.cat((out1, g_emb_d[text[:,0]-7]),1)
        combined_emb_a = torch.cat((out2, g_emb_a[text[:,0]-7]),1)

        #put attn here
        for idx in range(len(self.attn1)):
            combined_emb_d = self.attn1[idx]([combined_emb_d, combined_emb_a], 0)
            combined_emb_a = self.attn2[idx]([combined_emb_d, combined_emb_a], 1)

        ex_info = graph_batch.len_longest_path

        ex_info = ex_info.reshape([ex_info.shape[0], 1])
        ex_info = ex_info[text[:,0]-7]

        combined_emb_d = self.exMLP(combined_emb_d, ex_info.int())

        #add a MLP for area also
        num_nodes = [y - x for x,y in zip(graph_batch.ptr,graph_batch.ptr[1:])]

        num_nodes = torch.concat([i.reshape(1) for i in num_nodes])
        num_nodes = torch.reshape(num_nodes, (num_nodes.shape[0],1))
        num_nodes = num_nodes[text[:,0]-7]

        combined_emb_a = self.NumMLP(combined_emb_a, num_nodes)

        #FC1
        feat_a=F.relu(self.linear_a[0](combined_emb_a))
        feat_a=self.norm_a[0](feat_a)
        feat_d=F.relu(self.linear_d[0](combined_emb_d))
        feat_d=self.norm_d[0](feat_d)


        feat_a=F.dropout(feat_a,p=0.4,training=self.training)
        feat_d=F.dropout(feat_d,p=0.4,training=self.training)

        #FC2
        feat_a=F.relu(self.linear_a[1](feat_a))
        feat_a=self.norm_a[1](feat_a)

        feat_d=F.relu(self.linear_d[1](feat_d))
        feat_d=self.norm_d[1](feat_d)


        feat_a=F.dropout(feat_a,p=0.4,training=self.training)
        feat_d=F.dropout(feat_d,p=0.4,training=self.training)

        #FC3
        out_a=self.linear_a[2](feat_a)
        out_a = torch.squeeze(out_a, 1)

        out_d=self.linear_d[2](feat_d)
        out_d = torch.squeeze(out_d, 1)

        return out_d, out_a

class Hybridmodel_MTA_sep_Ex_SinEMB(nn.Module):
    def __init__(self, input_dim, emb_dim, num_heads =2, layers =2 ,hidden_dim=64, graph_emb=11):
        super(Hybridmodel_MTA_sep_Ex_SinEMB, self).__init__()

        self.embedding1 = nn.Embedding(input_dim, emb_dim)

        self.lstm1 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)
        self.lstm2 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)

        self.gmodel = GNN_MTA(gnn_type = 'gin', num_tasks = 1, num_layer = layers, num_heads = num_heads, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)

        linear_size = int((((hidden_dim + graph_emb)//100)+1)*100)
        self.linear_a=ModuleList()
        self.linear_a.append(Linear(hidden_dim + graph_emb, linear_size))
        self.linear_a.append(Linear(linear_size,linear_size))
        self.linear_a.append(Linear(linear_size,1))

        self.norm_a=ModuleList()
        self.norm_a.append(BatchNorm1d(linear_size))
        self.norm_a.append(BatchNorm1d(linear_size))

        self.linear_d=ModuleList()
        self.linear_d.append(Linear(hidden_dim + graph_emb, linear_size))
        self.linear_d.append(Linear(linear_size,linear_size))
        self.linear_d.append(Linear(linear_size,1))

        self.norm_d=ModuleList()
        self.norm_d.append(BatchNorm1d(linear_size))
        self.norm_d.append(BatchNorm1d(linear_size))

        self.attn1 =ModuleList()
        self.attn2 = ModuleList()

        for idx in range(2):
            self.attn1.append(mtl_attn(emb_dim=hidden_dim + graph_emb, num_tasks=2, num_heads = 2))
            self.attn2.append(mtl_attn(emb_dim=hidden_dim + graph_emb, num_tasks=2, num_heads = 2))

        self.exMLP = ConcatEmbedMLP(10000, hidden_dim + graph_emb)
        self.NumMLP = ConcatEmbedMLP(150000, hidden_dim + graph_emb)

    def forward(self, text, text_len, graph_batch, mask):
        text_emb1 = self.embedding1(text[:,1:])


        packed_input_1 = pack_padded_sequence(text_emb1, text_len-1, batch_first=True, enforce_sorted=False)
        packed_input_2 = pack_padded_sequence(text_emb1, text_len-1, batch_first=True, enforce_sorted=False)
        packed_output1, _ = self.lstm1(packed_input_1)
        packed_output2, _ = self.lstm2(packed_input_2)
        output1, _ = pad_packed_sequence(packed_output1, batch_first=True)
        output2, _ = pad_packed_sequence(packed_output2, batch_first=True)

        out1 = output1[:, -1, :]
        out2 = output2[:, -1, :]

        g_emb_d, g_emb_a = self.gmodel(graph_batch)
        combined_emb_d = torch.cat((out1, g_emb_d[text[:,0]-7]),1)
        combined_emb_a = torch.cat((out2, g_emb_a[text[:,0]-7]),1)

        #put attn here
        for idx in range(len(self.attn1)):
            combined_emb_d = self.attn1[idx]([combined_emb_d, combined_emb_a], 0)
            combined_emb_a = self.attn2[idx]([combined_emb_d, combined_emb_a], 1)

        ex_info = graph_batch.len_longest_path

        ex_info = ex_info.reshape([ex_info.shape[0], 1])
        ex_info = ex_info[text[:,0]-7]

        combined_emb_d = self.exMLP(combined_emb_d, ex_info.int())

        #add a MLP for area also
        num_nodes = [y - x for x,y in zip(graph_batch.ptr,graph_batch.ptr[1:])]

        num_nodes = torch.concat([i.reshape(1) for i in num_nodes])
        num_nodes = torch.reshape(num_nodes, (num_nodes.shape[0],1))
        num_nodes = num_nodes[text[:,0]-7]

        combined_emb_a = self.NumMLP(combined_emb_a, num_nodes)

        #FC1
        feat_a=F.relu(self.linear_a[0](combined_emb_a))
        feat_a=self.norm_a[0](feat_a)
        feat_d=F.relu(self.linear_d[0](combined_emb_d))
        feat_d=self.norm_d[0](feat_d)


        feat_a=F.dropout(feat_a,p=0.4,training=self.training)
        feat_d=F.dropout(feat_d,p=0.4,training=self.training)

        #FC2
        feat_a=F.relu(self.linear_a[1](feat_a))
        feat_a=self.norm_a[1](feat_a)

        feat_d=F.relu(self.linear_d[1](feat_d))
        feat_d=self.norm_d[1](feat_d)


        feat_a=F.dropout(feat_a,p=0.4,training=self.training)
        feat_d=F.dropout(feat_d,p=0.4,training=self.training)

        #FC3
        out_a=self.linear_a[2](feat_a)
        out_a = torch.squeeze(out_a, 1)

        out_d=self.linear_d[2](feat_d)
        out_d = torch.squeeze(out_d, 1)

        return out_d, out_a

class Hybridmodel_MTA_sep_ExLin(nn.Module):
    def __init__(self, input_dim, emb_dim, num_heads =2, layers =2 ,hidden_dim=64, graph_emb=11):
        super(Hybridmodel_MTA_sep_ExLin, self).__init__()

        self.embedding1 = nn.Embedding(input_dim, emb_dim)

        self.lstm1 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)
        self.lstm2 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)

        self.gmodel = GNN_MTA(gnn_type = 'gin', num_tasks = 1, num_layer = layers, num_heads = num_heads, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)

        linear_size = int((((hidden_dim + graph_emb)//100)+1)*100)
        self.linear_a=ModuleList()
        self.linear_a.append(Linear(hidden_dim + graph_emb, linear_size))
        self.linear_a.append(Linear(linear_size,linear_size))
        self.linear_a.append(Linear(linear_size,1))

        self.norm_a=ModuleList()
        self.norm_a.append(BatchNorm1d(linear_size))
        self.norm_a.append(BatchNorm1d(linear_size))

        self.linear_d=ModuleList()
        self.linear_d.append(Linear(hidden_dim + graph_emb, linear_size))
        self.linear_d.append(Linear(linear_size,linear_size))
        self.linear_d.append(Linear(linear_size,1))

        self.norm_d=ModuleList()
        self.norm_d.append(BatchNorm1d(linear_size))
        self.norm_d.append(BatchNorm1d(linear_size))

        self.attn1 =ModuleList()
        self.attn2 = ModuleList()

        for idx in range(2):
            self.attn1.append(mtl_attn(emb_dim=hidden_dim + graph_emb, num_tasks=2, num_heads = 2))
            self.attn2.append(mtl_attn(emb_dim=hidden_dim + graph_emb, num_tasks=2, num_heads = 2))

        self.exMLP = ConcatLinMLP(hidden_dim + graph_emb)
        self.NumMLP = ConcatLinMLP(hidden_dim + graph_emb)

    def forward(self, text, text_len, graph_batch, mask):
        text_emb1 = self.embedding1(text)


        packed_input_1 = pack_padded_sequence(text_emb1, text_len, batch_first=True, enforce_sorted=False)
        packed_input_2 = pack_padded_sequence(text_emb1, text_len, batch_first=True, enforce_sorted=False)
        packed_output1, _ = self.lstm1(packed_input_1)
        packed_output2, _ = self.lstm2(packed_input_2)
        output1, _ = pad_packed_sequence(packed_output1, batch_first=True)
        output2, _ = pad_packed_sequence(packed_output2, batch_first=True)

        out1 = output1[:, -1, :]
        out2 = output2[:, -1, :]

        g_emb_d, g_emb_a = self.gmodel(graph_batch)
        combined_emb_d = torch.cat((out1, g_emb_d[text[:,0]-7]),1)
        combined_emb_a = torch.cat((out2, g_emb_a[text[:,0]-7]),1)

        #put attn here
        for idx in range(len(self.attn1)):
            combined_emb_d = self.attn1[idx]([combined_emb_d, combined_emb_a], 0)
            combined_emb_a = self.attn2[idx]([combined_emb_d, combined_emb_a], 1)

        ex_info = graph_batch.len_longest_path

        ex_info = ex_info.reshape([ex_info.shape[0], 1])
        ex_info = ex_info[text[:,0]-7]

        combined_emb_d = self.exMLP(combined_emb_d, ex_info.to(torch.float32))

        #add a MLP for area also
        num_nodes = [y - x for x,y in zip(graph_batch.ptr,graph_batch.ptr[1:])]

        num_nodes = torch.concat([i.reshape(1) for i in num_nodes])
        num_nodes = torch.reshape(num_nodes, (num_nodes.shape[0],1))
        num_nodes = num_nodes[text[:,0]-7]

        combined_emb_a = self.NumMLP(combined_emb_a, num_nodes.to(torch.float32))

        #FC1
        feat_a=F.relu(self.linear_a[0](combined_emb_a))
        feat_a=self.norm_a[0](feat_a)
        feat_d=F.relu(self.linear_d[0](combined_emb_d))
        feat_d=self.norm_d[0](feat_d)


        feat_a=F.dropout(feat_a,p=0.4,training=self.training)
        feat_d=F.dropout(feat_d,p=0.4,training=self.training)

        #FC2
        feat_a=F.relu(self.linear_a[1](feat_a))
        feat_a=self.norm_a[1](feat_a)

        feat_d=F.relu(self.linear_d[1](feat_d))
        feat_d=self.norm_d[1](feat_d)


        feat_a=F.dropout(feat_a,p=0.4,training=self.training)
        feat_d=F.dropout(feat_d,p=0.4,training=self.training)

        #FC3
        out_a=self.linear_a[2](feat_a)
        out_a = torch.squeeze(out_a, 1)

        out_d=self.linear_d[2](feat_d)
        out_d = torch.squeeze(out_d, 1)

        return out_d, out_a

class LSTM_MLP(nn.Module):
    def __init__(self, emb_in, embedding_dim):
        super().__init__()
        self.project_linear0 = nn.Linear(emb_in, embedding_dim*2)
        self.project_linear1 = nn.Linear(embedding_dim*2, embedding_dim)
        self.project_linear2 = nn.Linear(embedding_dim, embedding_dim)

        self.norm1 = nn.BatchNorm1d(embedding_dim*2)
        self.norm2 = nn.BatchNorm1d(embedding_dim)

    def forward(self, lstm_embedding):
        h = self.project_linear0(lstm_embedding)
        h = F.relu(self.norm1(h))
        h = F.dropout(h, p=0.3, training=self.training)
        h = self.project_linear1(h)
        h = F.relu(self.norm2(h))
        h = F.dropout(h, p=0.3, training=self.training)
        h = self.project_linear2(h)
        return h

class ConcatEmbedMLP(nn.Module):
    def __init__(self, emb_in, embedding_dim):
        super().__init__()
        self.embedding = nn.Embedding(emb_in, embedding_dim)
        self.concat_linear = nn.Linear(embedding_dim+embedding_dim, embedding_dim*2)
        self.project_linear1 = nn.Linear(embedding_dim*2, embedding_dim)
        self.project_linear2 = nn.Linear(embedding_dim, embedding_dim)

        self.norm1 = nn.BatchNorm1d(embedding_dim*2)
        self.norm2 = nn.BatchNorm1d(embedding_dim)

    def forward(self, graph_embedding, discrete_tensor):
        discrete_embedding = self.embedding(discrete_tensor.squeeze(1))
        concatenated = torch.cat((graph_embedding, discrete_embedding), dim=-1)
        h = self.concat_linear(concatenated)
        h = F.relu(self.norm1(h))
        h = F.dropout(h, p=0.4, training=self.training)
        h = self.project_linear1(h)
        h = F.relu(self.norm2(h))
        h = F.dropout(h, p=0.4, training=self.training)
        h = self.project_linear2(h)
        return h

class ConcatLinMLP(nn.Module):
    def __init__(self, embedding_dim):
        super().__init__()
        self.lin1 = nn.Linear(1, embedding_dim)
        self.lin2 = nn.Linear(embedding_dim, embedding_dim)
        self.norm_lin1 = nn.BatchNorm1d(embedding_dim)


        self.concat_linear = nn.Linear(embedding_dim*2, embedding_dim*2)
        self.project_linear1 = nn.Linear(embedding_dim*2, embedding_dim)
        self.project_linear2 = nn.Linear(embedding_dim, embedding_dim)

        self.norm1 = nn.BatchNorm1d(embedding_dim*2)
        self.norm2 = nn.BatchNorm1d(embedding_dim)

    def forward(self, graph_embedding, discrete_tensor):
        discrete_lin = F.relu(self.norm_lin1(self.lin1(discrete_tensor)))
        discrete_lin = F.dropout(discrete_lin, p=0.4, training=self.training)
        discrete_lin = self.lin2(discrete_lin)
        discrete_lin = F.dropout(discrete_lin, p=0.4, training=self.training)
        concatenated = torch.cat((graph_embedding, discrete_lin), dim=-1)
        h = self.concat_linear(concatenated)
        h = F.relu(self.norm1(h))
        h = F.dropout(h, p=0.4, training=self.training)
        h = self.project_linear1(h)
        h = F.relu(self.norm2(h))
        h = F.dropout(h, p=0.4, training=self.training)
        h = self.project_linear2(h)
        return h

class Hybridmodel_MTAN(nn.Module):
    def __init__(self, input_dim, emb_dim, num_layer =2, layers =2 ,hidden_dim=64, graph_emb=11):
        super(Hybridmodel_MTAN, self).__init__()

        self.embedding = nn.Embedding(input_dim, emb_dim)
        self.lstm1 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)
        self.lstm2 = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)

        self.gmodel = GNN_MTAN(gnn_type = 'gin', num_tasks = 1, num_layer = layers, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)

        self.linear_a=ModuleList()
        self.linear_a.append(Linear(hidden_dim + graph_emb, 100))
        self.linear_a.append(Linear(100,100))
        self.linear_a.append(Linear(100,1))

        self.norm_a=ModuleList()
        self.norm_a.append(BatchNorm1d(100))
        self.norm_a.append(BatchNorm1d(100))

        self.linear_d=ModuleList()
        self.linear_d.append(Linear(hidden_dim + graph_emb, 100))
        self.linear_d.append(Linear(100,100))
        self.linear_d.append(Linear(100,1))

        self.norm_d=ModuleList()
        self.norm_d.append(BatchNorm1d(100))
        self.norm_d.append(BatchNorm1d(100))

    def forward(self, text, text_len, graph_batch):
        text_emb = self.embedding(text)

        packed_input = pack_padded_sequence(text_emb, text_len, batch_first=True, enforce_sorted=False)
        packed_output1, _ = self.lstm1(packed_input)
        packed_output2, _ = self.lstm2(packed_input)
        output1, _ = pad_packed_sequence(packed_output1, batch_first=True)
        output2, _ = pad_packed_sequence(packed_output2, batch_first=True)

        out1 = output1[:, -1, :]
        out2 = output2[:, -1, :]

        g_emb_d, g_emb_a = self.gmodel(graph_batch)
        combined_emb_d = torch.cat((out1, g_emb_d[text[:,0]-7]),1)
        combined_emb_a = torch.cat((out2, g_emb_a[text[:,0]-7]),1)


        #FC1
        feat_a=F.relu(self.linear_a[0](combined_emb_a))
        feat_a=self.norm_a[0](feat_a)
        feat_d=F.relu(self.linear_d[0](combined_emb_d))
        feat_d=self.norm_d[0](feat_d)

        feat_a=F.dropout(feat_a,p=0.4,training=self.training)
        feat_d=F.dropout(feat_d,p=0.4,training=self.training)

        #FC2
        feat_a=F.relu(self.linear_a[1](feat_a))
        feat_a=self.norm_a[1](feat_a)

        feat_d=F.relu(self.linear_d[1](feat_d))
        feat_d=self.norm_d[1](feat_d)

        feat_a=F.dropout(feat_a,p=0.4,training=self.training)
        feat_d=F.dropout(feat_d,p=0.4,training=self.training)

        #FC3
        out_a=self.linear_a[2](feat_a)
        out_a = torch.squeeze(out_a, 1)

        out_d=self.linear_d[2](feat_d)
        out_d = torch.squeeze(out_d, 1)

        return out_d, out_a




class PredMLP(nn.Module):
    def __init__(self, input_dim, linear_size):
        super(PredMLP, self).__init__()


        self.linear=ModuleList()
        self.linear.append(Linear(input_dim, linear_size))
        self.linear.append(Linear(linear_size,linear_size))
        self.linear.append(Linear(linear_size,1))

        self.norm=ModuleList()
        self.norm.append(BatchNorm1d(linear_size))
        self.norm.append(BatchNorm1d(linear_size))
    def forward(self, combined_emb):

        flow_fea=F.relu(self.linear[0](combined_emb))
        flow_fea=self.norm[0](flow_fea)
        flow_fea=F.dropout(flow_fea,p=0.4,training=self.training)

        flow_fea=F.relu(self.linear[1](flow_fea))
        flow_fea=self.norm[1](flow_fea)
        flow_fea=F.dropout(flow_fea,p=0.4,training=self.training)

        flow_out=self.linear[2](flow_fea)
        flow_out = torch.squeeze(flow_out, 1)
        return flow_out

class MLP_Group(nn.Module):
    def __init__(self, input_dim, linear_size):
        super(MLP_Group, self).__init__()
        self.MLP_1= PredMLP(input_dim, linear_size)
        self.MLP_0_1= PredMLP(input_dim, linear_size)
        self.MLP_00_1= PredMLP(input_dim, linear_size)
        self.MLP_000_1= PredMLP(input_dim, linear_size)

    def forward(self, combined_emb):

        out_1 = self.MLP_1(combined_emb)
        out_0_1 = self.MLP_0_1(combined_emb)
        out_00_1 = self.MLP_00_1(combined_emb)
        out_000_1 = self.MLP_000_1(combined_emb)

        return (out_000_1, out_00_1, out_0_1, out_1)

class PredClass(nn.Module):
    def __init__(self, input_dim, linear_size):
        super(PredClass, self).__init__()


        self.linear=ModuleList()
        self.linear.append(Linear(input_dim, linear_size))
        self.linear.append(Linear(linear_size,linear_size))
        self.linear.append(Linear(linear_size,4))

        self.norm=ModuleList()
        self.norm.append(BatchNorm1d(linear_size))
        self.norm.append(BatchNorm1d(linear_size))
    def forward(self, combined_emb):

        flow_fea=F.relu(self.linear[0](combined_emb))
        flow_fea=self.norm[0](flow_fea)
        flow_fea=F.dropout(flow_fea,p=0.4,training=self.training)

        flow_fea=F.relu(self.linear[1](flow_fea))
        flow_fea=self.norm[1](flow_fea)
        flow_fea=F.dropout(flow_fea,p=0.4,training=self.training)

        flow_out=self.linear[2](flow_fea)

        return flow_out


class MTFormer_MLP(nn.Module):
    def __init__(self, input_dim, emb_dim, num_heads =2, layers =2 ,hidden_dim=64, graph_emb=11, num_attn_layers = 2):
        super(MTFormer_MLP, self).__init__()

        self.embedding = nn.Embedding(input_dim, emb_dim)

        self.lstm = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)


        self.gmodel = GNN(gnn_type = 'gin', num_tasks = 1, num_layer = layers, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)

        linear_size = int((((hidden_dim + graph_emb)//100)+1)*100)

        self.MLP_group_d = MLP_Group(hidden_dim + graph_emb, linear_size)
        self.MLP_group_a = MLP_Group(hidden_dim + graph_emb, linear_size)
        self.Classify_d = PredClass(hidden_dim + graph_emb, linear_size)
        self.Classify_a = PredClass(hidden_dim + graph_emb, linear_size)

        self.cross_attn1 =ModuleList()
        self.cross_attn2 = ModuleList()

        for idx in range(num_attn_layers):
            self.cross_attn1.append(mtl_attn(emb_dim=hidden_dim + graph_emb, num_tasks=2, num_heads = num_heads))
            self.cross_attn2.append(mtl_attn(emb_dim=hidden_dim + graph_emb, num_tasks=2, num_heads = num_heads))

        self.self_attn1 = ModuleList()
        self.self_attn2 = ModuleList()
        for idx in range(num_attn_layers):
            self.self_attn1.append(self_attn(emb_dim=hidden_dim + graph_emb,  num_heads = num_heads))
            self.self_attn2.append(self_attn(emb_dim=hidden_dim + graph_emb,  num_heads = num_heads))

    def forward(self, text,graph_lable, graph_batch,skip_embedding=False):
        
        if not skip_embedding:
            text_emb = self.embedding(text)
        else:
            text_emb=text

        packed_output, _ = self.lstm(text_emb)


        out = packed_output[:, -1, :]
        
        g_emb = self.gmodel(graph_batch)

        combined_emb = torch.cat((out, g_emb[text[:,0]-7]),1)

        #put attn here
        self_atten_emb_list_d = []
        self_atten_emb_list_a = []

        self_atten_emb_list_d.append(torch.reshape(combined_emb, (combined_emb.shape[0], 1, combined_emb.shape[1])))
        self_atten_emb_list_a.append(torch.reshape(combined_emb, (combined_emb.shape[0], 1, combined_emb.shape[1])))

        for idx in range(len(self.self_attn1)):
            self_atten_emb_list_d.append(self.self_attn1[idx](self_atten_emb_list_d[idx]))
            self_atten_emb_list_a.append(self.self_attn2[idx](self_atten_emb_list_a[idx]))

        cross_atten_list_d = []
        cross_atten_list_a = []
        cross_atten_list_d.append(self_atten_emb_list_d[-1])
        cross_atten_list_a.append(self_atten_emb_list_a[-1])

        for idx in range(len(self.cross_attn1)):
            cross_atten_list_d.append(self.cross_attn1[idx]([cross_atten_list_d[idx], cross_atten_list_a[idx]], 0))
            cross_atten_list_a.append(self.cross_attn2[idx]([cross_atten_list_d[idx], cross_atten_list_a[idx]], 1))


        cross_atten_out_d = torch.reshape(cross_atten_list_d[-1], (cross_atten_list_d[-1].shape[0], cross_atten_list_d[-1].shape[2]))
        cross_atten_out_a = torch.reshape(cross_atten_list_a[-1], (cross_atten_list_a[-1].shape[0], cross_atten_list_a[-1].shape[2]))


        MLP_out_d = self.MLP_group_d(cross_atten_out_d)
        MLP_out_a = self.MLP_group_a(cross_atten_out_a)
        class_out_d = self.Classify_d(cross_atten_out_d)
        class_out_a = self.Classify_d(cross_atten_out_a)
        return MLP_out_d, MLP_out_a, class_out_d, class_out_a


class MTFormer_MLP_2(nn.Module):
    def __init__(self, input_dim, emb_dim, num_heads =2, layers =2 ,hidden_dim=64, graph_emb=11, num_attn_layers = 2):
        super(MTFormer_MLP_2, self).__init__()

        self.embedding = nn.Embedding(input_dim, emb_dim)

        self.lstm = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)


        self.gmodel = GNN(gnn_type = 'gin', num_tasks = 1, num_layer = layers, emb_dim = graph_emb, drop_ratio = 0, virtual_node = False)

        linear_size = int((((hidden_dim+graph_emb)//100)+1)*100)

    

        self.MLP_d = PredMLP(hidden_dim+graph_emb, linear_size)
        self.MLP_a = PredMLP(hidden_dim+graph_emb, linear_size)


        self.cross_attn1 =ModuleList()
        self.cross_attn2 = ModuleList()

        for idx in range(num_attn_layers):
            self.cross_attn1.append(mtl_attn(emb_dim=hidden_dim+graph_emb, num_tasks=2, num_heads = num_heads))
            self.cross_attn2.append(mtl_attn(emb_dim=hidden_dim+graph_emb, num_tasks=2, num_heads = num_heads))

        self.self_attn1 = ModuleList()
        self.self_attn2 = ModuleList()
        for idx in range(num_attn_layers):
            self.self_attn1.append(self_attn(emb_dim=hidden_dim+graph_emb,  num_heads = num_heads))
            self.self_attn2.append(self_attn(emb_dim=hidden_dim+graph_emb,  num_heads = num_heads))

    def forward(self, text,graph_lable, graph_batch,skip_embedding=False):
        if not skip_embedding:
            text_emb = self.embedding(text)
        else:
            text_emb=text
        # packed_input = pack_padded_sequence(text_emb, text_len, batch_first=True, enforce_sorted=False)
        packed_output, _ = self.lstm(text_emb)

        # output, _ = pad_packed_sequence(packed_output, batch_first=True)

        out = packed_output[:, -1, :]
        
        g_emb = self.gmodel(graph_batch)

        combined_emb = torch.cat((out, g_emb[graph_lable-7]),1)

        #put attn here
        self_atten_emb_list_d = []
        self_atten_emb_list_a = []

        self_atten_emb_list_d.append(torch.reshape(combined_emb, (combined_emb.shape[0], 1, combined_emb.shape[1])))
        self_atten_emb_list_a.append(torch.reshape(combined_emb, (combined_emb.shape[0], 1, combined_emb.shape[1])))

        for idx in range(len(self.self_attn1)):
            self_atten_emb_list_d.append(self.self_attn1[idx](self_atten_emb_list_d[idx]))
            self_atten_emb_list_a.append(self.self_attn2[idx](self_atten_emb_list_a[idx]))

        cross_atten_list_d = []
        cross_atten_list_a = []
        cross_atten_list_d.append(self_atten_emb_list_d[-1])
        cross_atten_list_a.append(self_atten_emb_list_a[-1])

        for idx in range(len(self.cross_attn1)):
            cross_atten_list_d.append(self.cross_attn1[idx]([cross_atten_list_d[idx], cross_atten_list_a[idx]], 0))
            cross_atten_list_a.append(self.cross_attn2[idx]([cross_atten_list_d[idx], cross_atten_list_a[idx]], 1))


        cross_atten_out_d = torch.reshape(cross_atten_list_d[-1], (cross_atten_list_d[-1].shape[0], cross_atten_list_d[-1].shape[2]))
        cross_atten_out_a = torch.reshape(cross_atten_list_a[-1], (cross_atten_list_a[-1].shape[0], cross_atten_list_a[-1].shape[2]))


        MLP_out_d = self.MLP_d(cross_atten_out_d)
        MLP_out_a = self.MLP_a(cross_atten_out_a)
        # class_out_d = self.Classify_d(out)
        # class_out_a = self.Classify_d(out)
        return MLP_out_d, MLP_out_a, text_emb


class MTL_MLP(nn.Module):
    def __init__(self, input_dim, emb_dim, num_heads =2, layers =2 ,hidden_dim=64, graph_emb=11, num_attn_layers = 2):
        super(MTL_MLP, self).__init__()

        self.embedding = nn.Embedding(input_dim, emb_dim)

        self.lstm = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)

        # TODO: drop_ratio
        self.gmodel = GNN(gnn_type = 'gin', num_tasks = 1, num_layer = layers, emb_dim = graph_emb, drop_ratio = 0, virtual_node = False)



        linear_size = int((((hidden_dim + graph_emb)//100)+1)*100)

        self.MLP_group_d = MLP_Group(hidden_dim + graph_emb, linear_size)
        self.MLP_group_a = MLP_Group(hidden_dim + graph_emb, linear_size)
        self.Classify_d = PredClass(hidden_dim + graph_emb, linear_size)
        self.Classify_a = PredClass(hidden_dim + graph_emb, linear_size)

    def forward(self, text, text_len, graph_batch, mask):

        text_emb = self.embedding(text)


        packed_input = pack_padded_sequence(text_emb, text_len, batch_first=True, enforce_sorted=False)

        packed_output, _ = self.lstm(packed_input)

        output, _ = pad_packed_sequence(packed_output, batch_first=True)


        out = output[:, -1, :]


        g_emb = self.gmodel(graph_batch)
        combined_emb = torch.cat((out, g_emb[text[:,0]-7]),1)


        MLP_out_d = self.MLP_group_d(combined_emb)
        MLP_out_a = self.MLP_group_a(combined_emb)
        class_out_d = self.Classify_d(combined_emb)
        class_out_a = self.Classify_d(combined_emb)
        return MLP_out_d, MLP_out_a, class_out_d, class_out_a

class MTFormer_SELF(nn.Module):
    def __init__(self, input_dim, emb_dim, num_heads =2, layers =2 ,hidden_dim=64, graph_emb=11, num_attn_layers = 2):
        super(MTFormer_SELF, self).__init__()

        self.embedding = nn.Embedding(input_dim, emb_dim)

        self.lstm = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)


        self.gmodel = GNN(gnn_type = 'gin', num_tasks = 1, num_layer = layers, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)


        linear_size = int((((hidden_dim + graph_emb)//100)+1)*100)
        self.MLP_group_d = MLP_Group(hidden_dim + graph_emb, linear_size)
        self.MLP_group_a = MLP_Group(hidden_dim + graph_emb, linear_size)
        self.Classify_d = PredClass(hidden_dim + graph_emb, linear_size)
        self.Classify_a = PredClass(hidden_dim + graph_emb, linear_size)


        self.self_attn1 = ModuleList()
        self.self_attn2 = ModuleList()
        for idx in range(num_attn_layers):
            self.self_attn1.append(self_attn(emb_dim=hidden_dim + graph_emb,  num_heads = num_heads))
            self.self_attn2.append(self_attn(emb_dim=hidden_dim + graph_emb,  num_heads = num_heads))
    def forward(self, text, text_len, graph_batch):

        text_emb = self.embedding(text)


        packed_input = pack_padded_sequence(text_emb, text_len, batch_first=True, enforce_sorted=False)

        packed_output, _ = self.lstm(packed_input)

        output, _ = pad_packed_sequence(packed_output, batch_first=True)


        out = output[:, -1, :]


        g_emb = self.gmodel(graph_batch)
        combined_emb = torch.cat((out, g_emb[text[:,0]-7]),1)


        #put attn here
        self_atten_emb_list_d = []
        self_atten_emb_list_a = []
        self_atten_emb_list_d.append(torch.reshape(combined_emb, (combined_emb.shape[0], 1, combined_emb.shape[1])))
        self_atten_emb_list_a.append(torch.reshape(combined_emb, (combined_emb.shape[0], 1, combined_emb.shape[1])))
        for idx in range(len(self.self_attn1)):
            self_atten_emb_list_d.append(self.self_attn1[idx](self_atten_emb_list_d[idx]))
            self_atten_emb_list_a.append(self.self_attn2[idx](self_atten_emb_list_a[idx]))

        self_atten_out_d = torch.reshape(self_atten_emb_list_d[-1], (self_atten_emb_list_d[-1].shape[0], self_atten_emb_list_d[-1].shape[2]))
        self_atten_out_a = torch.reshape(self_atten_emb_list_a[-1], (self_atten_emb_list_a[-1].shape[0], self_atten_emb_list_a[-1].shape[2]))
        #FC1
        MLP_out_d = self.MLP_group_d(self_atten_out_d)
        MLP_out_a = self.MLP_group_a(self_atten_out_a)
        class_out_d = self.Classify_d(self_atten_out_d)
        class_out_a = self.Classify_d(self_atten_out_a)
        return MLP_out_d, MLP_out_a, class_out_d, class_out_a


if __name__ == "__main__":
    pass