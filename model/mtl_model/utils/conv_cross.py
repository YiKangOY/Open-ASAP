'''
This file is adapted from https://github.com/lydiawunan/LOSTIN/blob/main/GNN-LSTM/conv.py with added GNNs for multi-task learning.
'''
import torch
from torch_geometric.nn import MessagePassing
import torch.nn.functional as F
import torch.nn as nn
from  torch.nn import MultiheadAttention
from torch_geometric.nn import global_mean_pool, global_add_pool, GATConv
from node_encoder import NodeEncoder,EdgeEncoder
from torch_geometric.utils import degree



### GIN convolution along the graph structure
class GINConv(MessagePassing):
    def __init__(self, emb_dim):
        '''
            emb_dim (int): node embedding dimensionality
        '''

        super(GINConv, self).__init__(aggr = "add")
        self.mlp = torch.nn.Sequential(torch.nn.Linear(emb_dim, emb_dim))
        self.eps = torch.nn.Parameter(torch.Tensor([0]))

        self.edge_encoder = EdgeEncoder(emb_dim = emb_dim)

    def forward(self, x, edge_index, edge_attr):
        edge_embedding = self.edge_encoder(edge_attr)
        out = self.mlp((1 + self.eps) *x + self.propagate(edge_index, x=x, edge_attr=edge_embedding))

        return out

    def message(self, x_j, edge_attr):
        return F.relu(x_j + edge_attr)

    def update(self, aggr_out):
        return aggr_out

class GCNConv(MessagePassing):
    def __init__(self, emb_dim):
        super(GCNConv, self).__init__(aggr='add')

        self.linear = torch.nn.Linear(emb_dim, emb_dim)
        self.root_emb = torch.nn.Embedding(1, emb_dim)
        self.edge_encoder = EdgeEncoder(emb_dim = emb_dim)

    def forward(self, x, edge_index, edge_attr):
        x = self.linear(x)
        edge_embedding = self.edge_encoder(edge_attr)

        row, col = edge_index
        deg = degree(row, x.size(0), dtype = x.dtype) + 1
        deg_inv_sqrt = deg.pow(-0.5)
        deg_inv_sqrt[deg_inv_sqrt == float('inf')] = 0

        norm = deg_inv_sqrt[row] * deg_inv_sqrt[col]

        return self.propagate(edge_index, x=x, edge_attr = edge_embedding, norm=norm) + F.relu(x + self.root_emb.weight) * 1./deg.view(-1,1)

    def message(self, x_j, edge_attr, norm):
        return norm.view(-1, 1) * F.relu(x_j + edge_attr)

    def update(self, aggr_out):
        return aggr_out

class GINConv_AttnMask(MessagePassing):
    def __init__(self, emb_dim):
        '''
            emb_dim (int): node embedding dimensionality
        '''
        self.emb_dim = emb_dim
        super(GINConv_AttnMask, self).__init__(aggr = "add")
        self.mlp = torch.nn.Sequential(torch.nn.Linear(emb_dim, emb_dim))
        self.eps = torch.nn.Parameter(torch.Tensor([0]))

        self.edge_encoder = EdgeEncoder(emb_dim = emb_dim)

    def forward(self, x, edge_index, edge_attr):
        edge_embedding = self.edge_encoder(edge_attr)
        out = self.mlp((1 + self.eps) *x + self.propagate(edge_index, x=x, edge_attr=edge_embedding))

        return out, edge_embedding

    def message(self, x_j, edge_attr):

        return F.relu(x_j + edge_attr)

    def update(self, aggr_out):
        return aggr_out


class GINConv_withAttn(MessagePassing):
    def __init__(self, emb_dim):
        '''
            emb_dim (int): node embedding dimensionality
        '''
        self.emb_dim = emb_dim
        super(GINConv_withAttn, self).__init__(aggr = "add")

        self.mlp = torch.nn.Sequential(torch.nn.Linear(emb_dim, emb_dim))
        self.eps = torch.nn.Parameter(torch.Tensor([0]))

        self.edge_encoder = EdgeEncoder(emb_dim = emb_dim)
        self.attn_mask = GATConv(self.emb_dim, self.emb_dim, add_self_loops = False)

    def forward(self, x, shared_x, edge_index, edge_attr, shared_edge_attr):
        edge_embedding = self.edge_encoder(edge_attr)

        #print(shared_x, edge_index, shared_edge_attr)
        y, attn = self.attn_mask(shared_x, edge_index, shared_edge_attr, return_attention_weights=True)
        attn_mask = attn[1]
        out = self.mlp((1 + self.eps) *x + self.propagate(edge_index, x=x, edge_attr=edge_embedding, attn_mask = attn_mask))

        return out

    def message(self, x_j, edge_attr, attn_mask):

        return F.relu(attn_mask * (x_j + edge_attr))

    def update(self, aggr_out):
        return aggr_out


class GNN_node_cross(torch.nn.Module):
    """
    Output:
        node representations
    """
    def __init__(self, num_layer, emb_dim, drop_ratio = 0.5, JK = "last", residual = False, gnn_type = 'gin'):
        '''
            emb_dim (int): node embedding dimensionality
            num_layer (int): number of GNN message passing layers
        '''

        super(GNN_node_cross, self).__init__()
        self.num_layer = num_layer
        self.drop_ratio = drop_ratio
        self.JK = JK
        ### add residual connection or not
        self.residual = residual

        if self.num_layer < 2:
            raise ValueError("Number of GNN layers must be greater than 1.")

        self.node_encoder_1 = NodeEncoder(emb_dim)
        self.node_encoder_2 = NodeEncoder(emb_dim)

        ###List of GNNs
        self.shared_convs_1 = torch.nn.ModuleList()
        self.shared_batch_norms_1 = torch.nn.ModuleList()
        self.shared_convs_2 = torch.nn.ModuleList()
        self.shared_batch_norms_2 = torch.nn.ModuleList()

        self.cross_unit = nn.Parameter(data = torch.ones(self.num_layer,2,2)/2)
        for layer in range(num_layer):
            if gnn_type == 'gin':
                self.shared_convs_1.append(GINConv(emb_dim))
                self.shared_convs_2.append(GINConv(emb_dim))
            elif gnn_type == 'gcn':
                self.shared_convs_1.append(GCNConv(emb_dim))
                self.shared_convs_2.append(GCNConv(emb_dim))
            else:
                raise ValueError('Undefined GNN type called {}'.format(gnn_type))

            self.shared_batch_norms_1.append(torch.nn.BatchNorm1d(emb_dim))
            self.shared_batch_norms_2.append(torch.nn.BatchNorm1d(emb_dim))

    def forward(self, batched_data):
        x, edge_index, edge_attr, batch = batched_data.x, batched_data.edge_index, batched_data.edge_attr, batched_data.batch

        ### computing input node embedding

        h_list_1 = [self.node_encoder_1(x)]
        h_list_2 = [self.node_encoder_2(x)]
        for layer in range(self.num_layer):

            h_1 = self.shared_convs_1[layer](h_list_1[layer], edge_index, edge_attr)
            h_1 = self.shared_batch_norms_1[layer](h_1)

            h_2 = self.shared_convs_2[layer](h_list_2[layer], edge_index, edge_attr)
            h_2 = self.shared_batch_norms_2[layer](h_2)


            if layer == self.num_layer - 1:
                h_1 = F.dropout(h_1, self.drop_ratio, training = self.training)
                h_2 = F.dropout(h_2, self.drop_ratio, training = self.training)
            else:
                h_1 = F.dropout(F.relu(h_1), self.drop_ratio, training = self.training)
                h_2 = F.dropout(F.relu(h_2), self.drop_ratio, training = self.training)

            h_1 = self.cross_unit[layer][0][0]*h_1 + self.cross_unit[layer][0][1]*h_2
            h_2 = self.cross_unit[layer][1][0]*h_1 + self.cross_unit[layer][1][1]*h_2


            if self.residual:
                h_1 += h_list_1[layer]
                h_2 += h_list_2[layer]

            h_list_1.append(h_1)
            h_list_2.append(h_2)

        ### Different implementations of Jk-concat
        if self.JK == "last":
            node_representation_1 = h_list_1[-1]
            node_representation_2 = h_list_2[-1]
        elif self.JK == "sum":
            node_representation_1 = 0
            node_representation_2 = 0
            for layer in range(self.num_layer):
                node_representation_1 += h_list_1[layer]
                node_representation_2 += h_list_2[layer]

        return node_representation_1, node_representation_2



class GNN_node_MTAN(torch.nn.Module):
    """
    Output:
        node representations
    """
    def __init__(self, num_layer, emb_dim, drop_ratio = 0.5, JK = "last", residual = False, gnn_type = 'gin'):
        '''
            emb_dim (int): node embedding dimensionality
            num_layer (int): number of GNN message passing layers
        '''

        super(GNN_node_MTAN, self).__init__()
        self.num_layer = num_layer
        self.drop_ratio = drop_ratio
        self.JK = JK
        ### add residual connection or not
        self.residual = residual

        if self.num_layer < 2:
            raise ValueError("Number of GNN layers must be greater than 1.")

        self.node_encoder = NodeEncoder(emb_dim)
        self.node_encoder_1 = NodeEncoder(emb_dim)
        self.node_encoder_2 = NodeEncoder(emb_dim)

        ###List of GNNs
        self.shared_convs = torch.nn.ModuleList()
        self.shared_batch_norms = torch.nn.ModuleList()

        self.conv1 = torch.nn.ModuleList()
        self.batch_norm1 = torch.nn.ModuleList()
        self.conv2 = torch.nn.ModuleList()
        self.batch_norm2 = torch.nn.ModuleList()


        for layer in range(num_layer):
            self.shared_convs.append(GINConv_AttnMask(emb_dim))
            self.shared_batch_norms.append(torch.nn.BatchNorm1d(emb_dim))

            self.conv1.append(GINConv_withAttn(emb_dim))
            self.batch_norm1.append(torch.nn.BatchNorm1d(emb_dim))

            self.conv2.append(GINConv_withAttn(emb_dim))
            self.batch_norm2.append(torch.nn.BatchNorm1d(emb_dim))

        self.pool = global_add_pool



    def forward(self, batched_data):
        x, edge_index, edge_attr, batch = batched_data.x, batched_data.edge_index, batched_data.edge_attr, batched_data.batch

        ### computing input node embedding
        h_list = [self.node_encoder(x)]
        h_1_list = [self.node_encoder_1(x)]
        h_2_list = [self.node_encoder_2(x)]
        for layer in range(self.num_layer):

            h_share, edge_attr_share= self.shared_convs[layer](h_list[layer], edge_index, edge_attr)
            h_share = self.shared_batch_norms[layer](h_share) 


            h_1 = self.conv1[layer](h_1_list[layer], h_share, edge_index, edge_attr, edge_attr_share)
            h_1 = self.batch_norm1[layer](h_1)

            h_2 = self.conv2[layer](h_2_list[layer], h_share, edge_index, edge_attr, edge_attr_share)
            h_2 = self.batch_norm2[layer](h_2)

            if layer == self.num_layer - 1:
                #remove relu for the last layer
                h_share = F.dropout(h_share, self.drop_ratio, training = self.training)
                h_1 = F.dropout(h_1, self.drop_ratio, training = self.training)
                h_2 = F.dropout(h_2, self.drop_ratio, training = self.training)
            else:
                h_share = F.dropout(F.relu(h_share), self.drop_ratio, training = self.training)
                h_1 = F.dropout(F.relu(h_1), self.drop_ratio, training = self.training)
                h_2 = F.dropout(F.relu(h_2), self.drop_ratio, training = self.training)

            if self.residual:
                h_share += h_list[layer]

            h_list.append(h_share)
            h_1_list.append(h_1)
            h_2_list.append(h_2)

        ### Different implementations of Jk-concat
        if self.JK == "last":
            node_representation1 = h_1_list[-1]
            node_representation2 = h_2_list[-1]
        elif self.JK == "sum":
            node_representation1 = 0
            node_representation2 = 0
            for layer in range(self.num_layer):
                node_representation1 += h_1_list[layer]
                node_representation2 +=h_2_list[layer]

        return node_representation1, node_representation2

class mtl_attn(torch.nn.Module):
    def __init__(self, emb_dim=32, num_tasks=2, num_heads = 2):
        """
        Use self attntion of features and combination of multi features' attention map to gen new features
        """
        super(mtl_attn, self).__init__()
        self.attns = torch.nn.ModuleList()
        for i in range(num_tasks):
            self.attns.append(MultiheadAttention(emb_dim, num_heads = num_heads, batch_first=True))


        self.mlp1 = torch.nn.Sequential(
            torch.nn.Linear(num_tasks*emb_dim, emb_dim),
            torch.nn.ReLU(),
            torch.nn.Dropout1d(p=0.4),
            torch.nn.Linear(emb_dim, emb_dim)
        )
        self.mlp2 = torch.nn.Sequential(
            torch.nn.Linear(emb_dim, emb_dim),
            torch.nn.ReLU(),
            torch.nn.Dropout1d(p=0.4),
            torch.nn.Linear(emb_dim, emb_dim)
        )

        self.attn_mlp1 = torch.nn.Sequential(
            torch.nn.Linear(emb_dim, emb_dim),
            torch.nn.ReLU(),
            torch.nn.Dropout1d(p=0.4),
            torch.nn.Linear(emb_dim, emb_dim)
        )
        self.attn_mlp2 = torch.nn.Sequential(
            torch.nn.Linear(emb_dim, emb_dim),
            torch.nn.ReLU(),
            torch.nn.Dropout1d(p=0.4),
            torch.nn.Linear(emb_dim, emb_dim)
        )

        self.layernorms = torch.nn.ModuleList()
        for idx in range(num_tasks):
            self.layernorms.append(torch.nn.LayerNorm(emb_dim))

        self.attn_layernorm = torch.nn.LayerNorm(emb_dim)
        self.batchnorm1 = torch.nn.BatchNorm1d(emb_dim)
        self.batchnorm2 = torch.nn.BatchNorm1d(emb_dim)

    def forward(self, in_feats, target_idx):
        assert len(in_feats) == len(self.attns)

        # print(in_feats[0].size(), in_feats[1].size())

        norm_feats = []
        for idx in range(len(in_feats)):
            norm_feats.append(self.layernorms[idx](in_feats[idx]))
        attn_outputs = []

        for idx in range(len(in_feats)):
            out_feat, _ = self.attns[idx](query = norm_feats[idx], key = norm_feats[idx], value = norm_feats[target_idx])
            attn_outputs.append(out_feat)

        attn_output_proj = []
        attn_output_proj.append(self.attn_mlp1(attn_outputs[0]))
        attn_output_proj.append(self.attn_mlp2(attn_outputs[1]))

        # print(attn_output_proj[0].size(), attn_output_proj[1].size())
        sum_feat = torch.cat(attn_output_proj, axis=2)
        mlp_out1 = self.mlp1(sum_feat)
        mlp_out1 = mlp_out1 + attn_outputs[target_idx]
        mlp_out1 = self.attn_layernorm(mlp_out1)

        mlp_out2 = self.mlp2(mlp_out1)
        mlp_out2 =mlp_out2 + in_feats[target_idx]


        return mlp_out2


class self_attn(torch.nn.Module):
    def __init__(self, emb_dim=32, num_heads = 2):
        """
        Use self attntion of features and combination of multi features' attention map to gen new features
        """
        super(self_attn, self).__init__()
        self.attns = torch.nn.ModuleList()
        self.attns=MultiheadAttention(emb_dim, num_heads = num_heads, batch_first=True)


        self.mlp1 = torch.nn.Sequential(
            torch.nn.Linear(emb_dim, emb_dim),
            torch.nn.ReLU(),
            torch.nn.Dropout1d(p=0.4),
            torch.nn.Linear(emb_dim, emb_dim)
        )


        self.layer_norm1 = torch.nn.LayerNorm(emb_dim)
        self.layer_norm2 = torch.nn.LayerNorm(emb_dim)
        self.batchnorm1 = torch.nn.BatchNorm1d(emb_dim)
        self.batchnorm2 = torch.nn.BatchNorm1d(emb_dim)



    def forward(self, in_feats):

        in_feats_norm = self.layer_norm1(in_feats)

        atten_out, _ = self.attns(query = in_feats_norm, key = in_feats_norm, value = in_feats_norm)

        atten_feat = in_feats+atten_out
        atten_feat_norm  = self.layer_norm2(atten_feat)
        out_feat = self.mlp1(atten_feat_norm)+atten_feat
        return out_feat


class GNN_node_MTA(torch.nn.Module):
    """
    Output:
        node representations
    """
    def __init__(self, num_layer, emb_dim, num_heads= 2,  drop_ratio = 0.5, JK = "last", residual = False, gnn_type = 'gin'):
        '''
            emb_dim (int): node embedding dimensionality
            num_layer (int): number of GNN message passing layers
        '''

        super(GNN_node_MTA, self).__init__()
        self.num_layer = num_layer
        self.drop_ratio = drop_ratio
        self.JK = JK
        ### add residual connection or not
        self.residual = residual

        if self.num_layer < 2:
            raise ValueError("Number of GNN layers must be greater than 1.")


        self.node_encoder_1 = NodeEncoder(emb_dim)
        self.node_encoder_2 = NodeEncoder(emb_dim)

        ###List of GNNs


        self.conv1 = torch.nn.ModuleList()
        self.batch_norm1 = torch.nn.ModuleList()
        self.conv2 = torch.nn.ModuleList()
        self.batch_norm2 = torch.nn.ModuleList()


        for layer in range(num_layer):    
            self.conv1.append(GINConv(emb_dim))
            self.batch_norm1.append(torch.nn.BatchNorm1d(emb_dim))

            self.conv2.append(GINConv(emb_dim))
            self.batch_norm2.append(torch.nn.BatchNorm1d(emb_dim))


    def forward(self, batched_data):
        x, edge_index, edge_attr, batch = batched_data.x, batched_data.edge_index, batched_data.edge_attr, batched_data.batch

        ### computing input node embedding
        h_1_list = [self.node_encoder_1(x)]
        h_2_list = [self.node_encoder_2(x)]
        for layer in range(self.num_layer):

            h_1 = self.conv1[layer](h_1_list[layer], edge_index, edge_attr)
            h_1 = self.batch_norm1[layer](h_1)

            h_2 = self.conv2[layer](h_2_list[layer], edge_index, edge_attr)
            h_2 = self.batch_norm2[layer](h_2)

            if layer == self.num_layer - 1:
                #remove relu for the last layer

                h_1 = F.dropout(h_1, self.drop_ratio, training = self.training)
                h_2 = F.dropout(h_2, self.drop_ratio, training = self.training)
            else:

                h_1 = F.dropout(F.relu(h_1), self.drop_ratio, training = self.training)
                h_2 = F.dropout(F.relu(h_2), self.drop_ratio, training = self.training)

            if self.residual:
                h_1 += h_1_list[layer]
                h_2 += h_2_list[layer]


            h_1_list.append(h_1)
            h_2_list.append(h_2)

        ### Different implementations of Jk-concat
        if self.JK == "last":
            node_representation1 = h_1_list[-1]
            node_representation2 = h_2_list[-1]
        elif self.JK == "sum":
            node_representation1 = 0
            node_representation2 = 0
            for layer in range(self.num_layer):
                node_representation1 += h_1_list[layer]
                node_representation2 += h_2_list[layer]

        return node_representation1, node_representation2



class GNN_node_Virtualnode(torch.nn.Module):
    """
    Output:
        node representations
    """
    def __init__(self, num_layer, emb_dim, drop_ratio = 0.5, JK = "last", residual = False, gnn_type = 'gin'):
        '''
            emb_dim (int): node embedding dimensionality
        '''
        super(GNN_node_Virtualnode, self).__init__()
        self.num_layer = num_layer
        self.drop_ratio = drop_ratio
        self.JK = JK
        ### add residual connection or not
        self.residual = residual

        if self.num_layer < 2:
            raise ValueError("Number of GNN layers must be greater than 1.")

        self.node_encoder = NodeEncoder(emb_dim)

        ### set the initial virtual node embedding to 0.
        self.virtualnode_embedding = torch.nn.Embedding(1, emb_dim)
        torch.nn.init.constant_(self.virtualnode_embedding.weight.data, 0)

        ### List of GNNs
        self.shared_convs = torch.nn.ModuleList()
        ### batch norms applied to node embeddings
        self.shared_batch_norms = torch.nn.ModuleList()

        ### List of MLPs to transform virtual node at every layer
        self.mlp_virtualnode_list = torch.nn.ModuleList()

        for layer in range(num_layer):
            if gnn_type == 'gin':
                self.shared_convs.append(GINConv(emb_dim))
            elif gnn_type == 'gcn':
                self.shared_convs.append(GCNConv(emb_dim))
            else:
                raise ValueError('Undefined GNN type called {}'.format(gnn_type))

            self.shared_batch_norms.append(torch.nn.BatchNorm1d(emb_dim))

        for layer in range(num_layer - 1):
            self.mlp_virtualnode_list.append(torch.nn.Sequential(torch.nn.Linear(emb_dim, 2*emb_dim), torch.nn.BatchNorm1d(2*emb_dim), torch.nn.ReLU(), \
                                                    torch.nn.Linear(2*emb_dim, emb_dim), torch.nn.BatchNorm1d(emb_dim), torch.nn.ReLU()))


    def forward(self, batched_data):

        x, edge_index, edge_attr, batch = batched_data.x, batched_data.edge_index, batched_data.edge_attr, batched_data.batch

        ### virtual node embeddings for graphs
        virtualnode_embedding = self.virtualnode_embedding(torch.zeros(batch[-1].item() + 1).to(edge_index.dtype).to(edge_index.device))

        h_list = [self.node_encoder(x)]
        for layer in range(self.num_layer):
            ### add message from virtual nodes to graph nodes
            h_list[layer] = h_list[layer] + virtualnode_embedding[batch]

            ### Message passing among graph nodes
            h = self.shared_convs[layer](h_list[layer], edge_index, edge_attr)

            h = self.shared_batch_norms[layer](h)
            if layer == self.num_layer - 1:
                #remove relu for the last layer
                h = F.dropout(h, self.drop_ratio, training = self.training)
            else:
                h = F.dropout(F.relu(h), self.drop_ratio, training = self.training)

            if self.residual:
                h = h + h_list[layer]

            h_list.append(h)

            ### update the virtual nodes
            if layer < self.num_layer - 1:
                ### add message from graph nodes to virtual nodes
                virtualnode_embedding_temp = global_add_pool(h_list[layer], batch) + virtualnode_embedding
                ### transform virtual nodes using MLP

                if self.residual:
                    virtualnode_embedding = virtualnode_embedding + F.dropout(self.mlp_virtualnode_list[layer](virtualnode_embedding_temp), self.drop_ratio, training = self.training)
                else:
                    virtualnode_embedding = F.dropout(self.mlp_virtualnode_list[layer](virtualnode_embedding_temp), self.drop_ratio, training = self.training)

        ### Different implementations of Jk-concat
        if self.JK == "last":
            node_representation = h_list[-1]
        elif self.JK == "sum":
            node_representation = 0
            for layer in range(self.num_layer):
                node_representation += h_list[layer]

        return node_representation

if __name__ == "__main__":
    pass