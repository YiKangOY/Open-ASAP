### Libraries
import numpy as np
import argparse
import matplotlib.pyplot as plts
import pandas as pd
import torch

# Preliminaries
# torchtext 0.6.0
from torchtext.data import Field, TabularDataset, BucketIterator
from torch.utils.tensorboard import SummaryWriter

# Models
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import torch.nn.functional as F
from torch.nn import ReLU, Linear, BatchNorm1d, ModuleList


# Training
import torch.optim as optim

# Evaluation
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# graph loading dependency
import sys
sys.path.insert(0, 'utils')
from torch_geometric.data import DataLoader
from dataset_pyg import PygGraphPropPredDataset
from gnn import GNN, GNN_ex, GNN_LL, GNN_Num

### auxillaries
import os
import csv
import re
import joblib

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
    
    def foward(self, combined_emb):
        
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

        
# Hybrid model
class Hybridmodel(nn.Module):
    def __init__(self, input_dim, emb_dim, layers = 2, hidden_dim=64, graph_emb=11):
        super(Hybridmodel, self).__init__()

        self.embedding = nn.Embedding(input_dim, emb_dim)
        self.lstm = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)

        self.gmodel = GNN(gnn_type = 'gin', num_tasks = 1, num_layer = layers, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)

        linear_size = int((((hidden_dim + graph_emb)//100)+1)*100)
        print("Linear layer size:{}".format(linear_size))
        self.MLP_1= PredMLP(hidden_dim+graph_emb, linear_size)
        self.MLP_0_1= PredMLP(hidden_dim+graph_emb, linear_size)
        self.MLP_00_1= PredMLP(hidden_dim+graph_emb, linear_size)
        self.MLP_000_1= PredMLP(hidden_dim+graph_emb, linear_size)
        self.classifier = PredClass(hidden_dim+graph_emb, linear_size)
    def forward(self, text, text_len, graph_batch):

        text_emb = self.embedding(text[:,1:])

        packed_input = pack_padded_sequence(text_emb, text_len-1, batch_first=True, enforce_sorted=False)
        packed_output, _ = self.lstm(packed_input)
        output, _ = pad_packed_sequence(packed_output, batch_first=True)

        out = output[:, -1, :]

        g_emb = self.gmodel(graph_batch)
        combined_emb = torch.cat((out, g_emb[text[:,0]-7]),1)


        out_1 = self.MLP_1(combined_emb)
        out_0_1 = self.MLP_0_1(combined_emb)
        out_00_1 = self.MLP_00_1(combined_emb)
        out_000_1 = self.MLP_000_1(combined_emb)
        
        out_class = self.classifier(combined_emb)
        
        return (out_000_1, out_00_1, out_0_1, out_1), out_class

class Hybridmodel_ex(nn.Module):
    def __init__(self, input_dim, emb_dim, layers = 2, hidden_dim=64, graph_emb=11):
        super(Hybridmodel_ex, self).__init__()

        self.embedding = nn.Embedding(input_dim, emb_dim)
        self.lstm = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)

        self.gmodel = GNN_ex(gnn_type = 'gin', num_tasks = 1, num_layer = layers, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)

        linear_size = int((((hidden_dim + graph_emb)//100)+1)*100)
        print("Linear layer size:{}".format(linear_size))
        self.linear=ModuleList()
        self.linear.append(Linear(hidden_dim + graph_emb, linear_size))
        self.linear.append(Linear(linear_size,linear_size))
        self.linear.append(Linear(linear_size,1))

        self.norm=ModuleList()
        self.norm.append(BatchNorm1d(linear_size))
        self.norm.append(BatchNorm1d(linear_size))


    def forward(self, text, text_len, graph_batch):

        text_emb = self.embedding(text)

        packed_input = pack_padded_sequence(text_emb, text_len, batch_first=True, enforce_sorted=False)
        packed_output, _ = self.lstm(packed_input)
        output, _ = pad_packed_sequence(packed_output, batch_first=True)

        out = output[:, -1, :]

        g_emb = self.gmodel(graph_batch)
        combined_emb = torch.cat((out, g_emb[text[:,0]-7]),1)

        flow_fea=F.relu(self.linear[0](combined_emb))
        flow_fea=self.norm[0](flow_fea)
        flow_fea=F.dropout(flow_fea,p=0.4,training=self.training)

        flow_fea=F.relu(self.linear[1](flow_fea))
        flow_fea=self.norm[1](flow_fea)
        flow_fea=F.dropout(flow_fea,p=0.4,training=self.training)

        flow_out=self.linear[2](flow_fea)
        flow_out = torch.squeeze(flow_out, 1)

        return flow_out

class Hybridmodel_LL(nn.Module):
    def __init__(self, input_dim, emb_dim, layers = 2, hidden_dim=64, graph_emb=11):
        super(Hybridmodel_LL, self).__init__()

        self.embedding = nn.Embedding(input_dim, emb_dim)
        self.lstm = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)

        self.gmodel = GNN_LL(gnn_type = 'gin', num_tasks = 1, num_layer = layers, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)

        linear_size = int((((hidden_dim + graph_emb)//100)+1)*100)
        print("Linear layer size:{}".format(linear_size))
        self.MLP_1= PredMLP(hidden_dim+graph_emb, linear_size)
        self.MLP_0_1= PredMLP(hidden_dim+graph_emb, linear_size)
        self.MLP_00_1= PredMLP(hidden_dim+graph_emb, linear_size)
        self.MLP_000_1= PredMLP(hidden_dim+graph_emb, linear_size)
        self.classifier = PredClass(hidden_dim+graph_emb, linear_size)


    def forward(self, text, text_len, graph_batch):

        text_emb = self.embedding(text[:,1:])

        packed_input = pack_padded_sequence(text_emb, text_len-1, batch_first=True, enforce_sorted=False)
        packed_output, _ = self.lstm(packed_input)
        output, _ = pad_packed_sequence(packed_output, batch_first=True)

        out = output[:, -1, :]

        g_emb = self.gmodel(graph_batch)
        combined_emb = torch.cat((out, g_emb[text[:,0]-7]),1)

        out_1 = self.MLP_1(combined_emb)
        out_0_1 = self.MLP_0_1(combined_emb)
        out_00_1 = self.MLP_00_1(combined_emb)
        out_000_1 = self.MLP_000_1(combined_emb)
        
        out_class = self.classifier(combined_emb)
        
        return (out_000_1, out_00_1, out_0_1, out_1), out_class

class Hybridmodel_Num(nn.Module):
    def __init__(self, input_dim, emb_dim, layers = 2, hidden_dim=64, graph_emb=11):
        super(Hybridmodel_Num, self).__init__()

        self.embedding = nn.Embedding(input_dim, emb_dim)
        self.lstm = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=2,
                            batch_first=True, bidirectional=False)

        self.gmodel = GNN_Num(gnn_type = 'gin', num_tasks = 1, num_layer = layers, emb_dim = graph_emb, drop_ratio = 0.5, virtual_node = False)

        linear_size = int((((hidden_dim + graph_emb)//100)+1)*100)
        print("Linear layer size:{}".format(linear_size))
        self.MLP_1= PredMLP(hidden_dim+graph_emb, linear_size)
        self.MLP_0_1= PredMLP(hidden_dim+graph_emb, linear_size)
        self.MLP_00_1= PredMLP(hidden_dim+graph_emb, linear_size)
        self.MLP_000_1= PredMLP(hidden_dim+graph_emb, linear_size)
        self.classifier = PredClass(hidden_dim+graph_emb, linear_size)


    def forward(self, text, text_len, graph_batch):

        text_emb = self.embedding(text[:,1:])

        packed_input = pack_padded_sequence(text_emb, text_len-1, batch_first=True, enforce_sorted=False)
        packed_output, _ = self.lstm(packed_input)
        output, _ = pad_packed_sequence(packed_output, batch_first=True)

        out = output[:, -1, :]

        g_emb = self.gmodel(graph_batch)
        combined_emb = torch.cat((out, g_emb[text[:,0]-7]),1)

        out_1 = self.MLP_1(combined_emb)
        out_0_1 = self.MLP_0_1(combined_emb)
        out_00_1 = self.MLP_00_1(combined_emb)
        out_000_1 = self.MLP_000_1(combined_emb)
        
        out_class = self.classifier(combined_emb)
        
        return (out_000_1, out_00_1, out_0_1, out_1), out_class
    


# Save Functions
def save_checkpoint(save_path, model, optimizer, valid_loss):

    if save_path == None:
        return
    
    state_dict = {'model_state_dict': model.state_dict(),
                  'optimizer_state_dict': optimizer.state_dict(),
                  'valid_loss': valid_loss}
    
    torch.save(state_dict, save_path)
    print(f'Model saved to ==> {save_path}')


def save_metrics(save_path, train_loss_list, valid_loss_list, global_steps_list):

    if save_path == None:
        return
    
    state_dict = {'train_loss_list': train_loss_list,
                  'valid_loss_list': valid_loss_list,
                  'global_steps_list': global_steps_list}
    
    torch.save(state_dict, save_path)
    print(f'Model saved to ==> {save_path}')

def load_checkpoint(load_path, model, optimizer, device):

    if load_path==None:
        return
    
    state_dict = torch.load(load_path, map_location=device)
    print(f'Model loaded from <== {load_path}')
    
    model.load_state_dict(state_dict['model_state_dict'])
    optimizer.load_state_dict(state_dict['optimizer_state_dict'])
    
    return state_dict['valid_loss']



def loss_ensemble(criterion, pred, labels, class_res, device, range_list=[0.01, 0.1, 1]):
    mask = []
    mask.append(labels<=0.01)
    mask.append((labels>0.01) & (labels<=0.1))
    mask.append((labels>0.1) & (labels<=1))
    mask.append(labels>1)
    
    class_tar = torch.zeros(labels.shape[0], 4).to(device)
    idx = torch.where(labels<=0.01)
    for i in idx[0]:
        class_tar[i][0]=1
    idx = torch.where((labels>0.01) & (labels<=0.1))
    for i in idx[0]:
        class_tar[i][1]=1
    idx = torch.where((labels>0.1) & (labels<=1))
    for i in idx[0]:
        class_tar[i][2]=1
    idx = torch.where(labels>1)
    for i in idx[0]:
        class_tar[i][3]=1

    loss_list = []
    
    criterion_th = nn.CrossEntropyLoss()

    for idx in range(len(pred)):

        in_range_loss = criterion(pred[idx][mask[idx]], labels[mask[idx]])

        out_range_loss = criterion_th(class_res, class_tar)

        loss_list.append(in_range_loss+out_range_loss)
    # print("="*64)
    return loss_list[0], loss_list[1], loss_list[2],loss_list[3]

def pred_ensemble(pred, class_res, device):
    # print(class_res)
    _, class_res = torch.max(class_res, 1)
    # print(class_res)
    pred_out = torch.zeros(pred[0].shape[0]).to(device)
    
    for idx in range(len(pred)):
        mask = torch.where(class_res==idx)
        pred_out[mask] = pred[idx][mask]
    return pred_out
    
    
        
        

def training(model, device,
          optimizer,
          train_loader,
          valid_loader,
          induct_valid_loader,
          graph_loader,
          num_epochs,
          eval_every,
          args,
          tb_writer,
          criterion = nn.MSELoss(),
          best_valid_loss = float("Inf"), best_train_loss = float("Inf"), best_mape = float("Inf"),
          best_induct_valid_loss = float("Inf"), best_induct_mape = float("Inf")
          ):
    
    file_path = args.dest_folder
    # initialize running values
    running_loss = 0.0
    valid_running_loss = 0.0
    global_step = 0
    train_loss_list = []
    valid_loss_list = []
    global_steps_list = []

    # read graphs
    for graph_batch in graph_loader:
        graph_batch = graph_batch.to(device)
    with open(args.dest_folder+'/logs/'+'/validLog.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Epochs", "MAPE", "Loss"])
    with open(args.dest_folder+'/logs/'+'/valid_induct_Log.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Epochs", "MAPE", "Loss"])
    # training loop
    model.train()
    for epoch in range(num_epochs):
        for ((flow, flow_len), labels), _ in train_loader:         
            labels = labels.to(device)
            flow = flow.to(device)
            flow_len = flow_len.to("cpu")
            output, class_res = model(flow, flow_len, graph_batch)

            loss0, loss1, loss2, loss3 = loss_ensemble(criterion, output, labels, class_res, device)
            
            loss = loss0+loss1+loss2+loss3
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
            # update running values
            running_loss += loss.item()
            global_step += 1

            y_pred = []
            y_true = []
            relative_error = []
            flow_l = []
            design = []
            
            # evaluation step
            if global_step % eval_every == 0:
                model.eval()
                with torch.no_grad():                    
                  # validation loop
                  for ((flow, flow_len), labels), _ in valid_loader:
                      labels = labels.to(device)
                      flow = flow.to(device)
                      flow_len = flow_len.to("cpu")
                      output, class_res = model(flow, flow_len, graph_batch)
                      
                      output = pred_ensemble(output, class_res, device)    

                      
                      labels_val = labels.tolist()
                      output_val = output.tolist()

                      y_pred.extend(output_val)
                      y_true.extend(labels_val)

                      rmae = np.abs(np.divide(np.subtract(output_val, labels_val), labels_val))

                      relative_error.extend(rmae)
                      flow_l.extend(flow_len.tolist())
                      design.extend((flow[:,0]-7).tolist())
                      loss = criterion(output, labels)
                      valid_running_loss += loss.item()
                
                
                output = pd.DataFrame({'design_name':design, 'flow_length':flow_l, 'labels': y_true, 'prediction': y_pred, 'relative error': relative_error})
                output.to_csv(file_path+'/logs/'+'/valid_'+'epo'+str(epoch)+'.csv',index=False)
                # evaluation
                mape = np.mean(relative_error)
                average_train_loss = running_loss / eval_every
                average_valid_loss = valid_running_loss / len(valid_loader)
                train_loss_list.append(average_train_loss)
                valid_loss_list.append(average_valid_loss)
                global_steps_list.append(global_step)

                tb_writer.add_scalars(file_path+'/'+'losses'.format(epoch), {'train loss': average_train_loss, 'valid_loss':average_valid_loss}, epoch)
                tb_writer.add_scalar(file_path+'/'+'valid_MAPE', np.mean(relative_error), epoch)
                with open(args.dest_folder+'/logs/'+'/validLog.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([epoch, mape, average_valid_loss])
                # resetting running 
                running_loss = 0.0                
                valid_running_loss = 0.0
                model.train()

                # print progress
                print('Epoch [{}/{}], Step [{}/{}], Train Loss: {:.4f}, Valid Loss: {:.4f}'
                      .format(epoch+1, num_epochs, global_step, num_epochs*len(train_loader),
                              average_train_loss, average_valid_loss))
                
                # checkpoint
                if best_valid_loss + best_train_loss > average_valid_loss + average_train_loss :
                    best_valid_loss = average_valid_loss
                    best_train_loss = average_train_loss
                    save_checkpoint(file_path + '/model_batch_'+str(args.batch_size)+'_epo'+str(epoch)+'.pt', model, optimizer, best_valid_loss)
                    save_metrics(file_path + '/metrics_batch_'+str(args.batch_size)+'.pt', train_loss_list, valid_loss_list, global_steps_list)
                elif best_valid_loss>average_valid_loss:
                    best_valid_loss = average_valid_loss
                    save_checkpoint(file_path + '/model_batch_'+str(args.batch_size)+'_epo'+str(epoch)+'.pt', model, optimizer, best_valid_loss)
                    save_metrics(file_path + '/metrics_batch_'+str(args.batch_size)+'.pt', train_loss_list, valid_loss_list, global_steps_list)
                elif best_mape > mape:
                    best_mape = mape
                    save_checkpoint(file_path + '/model_batch_'+str(args.batch_size)+'_epo'+str(epoch)+'.pt', model, optimizer, best_valid_loss)
                    save_metrics(file_path + '/metrics_batch_'+str(args.batch_size)+'.pt', train_loss_list, valid_loss_list, global_steps_list)


            #induct valid
            
            y_pred = []
            y_true = []
            relative_error = []
            flow_l = []
            design = []             
            induct_valid_running_loss = 0.0
            if global_step % eval_every == 0:
                model.eval()
                with torch.no_grad():                    
                  # validation loop
                  for ((flow, flow_len), labels), _ in induct_valid_loader:
                      labels = labels.to(device)
                      flow = flow.to(device)
                      flow_len = flow_len.to("cpu")
                      output, class_res = model(flow, flow_len, graph_batch)
                      
                      output = pred_ensemble(output, class_res, device)   
                      
                      labels_val = labels.tolist()
                      output_val = output.tolist()
                    #   labels_val = np.power(10,  labels_val)
                    #   output_val = np.power(10,  output_val)
                      y_pred.extend(output_val)
                      y_true.extend(labels_val)

                      rmae = np.abs(np.divide(np.subtract(output_val, labels_val), labels_val))

                      relative_error.extend(rmae)
                      flow_l.extend(flow_len.tolist())
                      design.extend((flow[:,0]-7).tolist())
                      loss = criterion(output, labels)
                      induct_valid_running_loss += loss.item()
                
                
                output = pd.DataFrame({'design_name':design, 'flow_length':flow_l, 'labels': y_true, 'prediction': y_pred, 'relative error': relative_error})
                output.to_csv(file_path+'/logs/'+'/valid_induct_'+'epo'+str(epoch)+'.csv',index=False)
                # evaluation
                mape = np.mean(relative_error)
                average_valid_loss = induct_valid_running_loss / len(induct_valid_loader)
                train_loss_list.append(average_train_loss)
                valid_loss_list.append(average_valid_loss)

                tb_writer.add_scalars(file_path+'/'+'losses'.format(epoch), {'train loss': average_train_loss, 'valid_loss':average_valid_loss}, epoch)
                tb_writer.add_scalar(file_path+'/'+'valid_MAPE', np.mean(relative_error), epoch)
                with open(args.dest_folder+'/logs/'+'/valid_induct_Log.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([epoch, mape, average_valid_loss])
                # resetting running               
                induct_valid_running_loss = 0.0
                model.train()

                # print progress
                print('Epoch [{}/{}], Step [{}/{}], Train Loss: {:.4f}, Valid Loss: {:.4f}'
                      .format(epoch+1, num_epochs, global_step, num_epochs*len(train_loader),
                              average_train_loss, average_valid_loss))
                
                # checkpoint
                if best_induct_mape > mape:
                    best_induct_mape = mape
                    save_checkpoint(file_path + '/model_batch_'+str(args.batch_size)+'_epo'+str(epoch)+'.pt', model, optimizer, best_induct_valid_loss)
                    save_metrics(file_path + '/metrics_batch_'+str(args.batch_size)+'.pt', train_loss_list, valid_loss_list, global_steps_list)

  
    save_metrics(file_path + '/metrics_batch_'+str(args.batch_size)+'.pt', train_loss_list, valid_loss_list, global_steps_list)
    print('Finished Training!')

def testing(model, device,
          optimizer,
          test_loader,
          graph_loader,
          args,
          tb_writer,
          if_std,
          criterion = nn.MSELoss(),
          ):
    
    with open(args.dest_folder+'/logs/'+'/testLog.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Epochs", "MAPE"])
    
    print(if_std)
    if if_std:
        scaler = joblib.load(args.data_folder+'/scaler.save')

    files = os.listdir(args.dest_folder)
    model_files = [f for f in files if f.endswith(".pt") and f.startswith("model")]
    print(model_files)
    model_files = sorted(model_files, key=lambda s: int(re.findall(r'\d+', s)[1]))
    print(model_files)
    global_steps = 0
    for file in model_files:
        load_checkpoint(args.dest_folder + '/'+file, model, optimizer, device)
    

        y_pred = []
        y_true = []
        relative_error = []
        flow_l = []
        design = []

        for graph_batch in graph_loader:
            graph_batch = graph_batch.to(device)

        model.eval()
        with torch.no_grad():
            for ((flow, flow_len), labels), _ in test_loader:     

                labels = labels.to(device)
                flow = flow.to(device)
                flow_len = flow_len.to("cpu")
                output, class_res = model(flow, flow_len, graph_batch)
                
                output = pred_ensemble(output, class_res, device)   
                
                if if_std:
                    output = (output*(scaler.var_[0]**0.5))+scaler.mean_[0]
                labels = labels.tolist()
                output = output.tolist()
                y_pred.extend(output)
                y_true.extend(labels)

                rmae = np.abs(np.divide(np.subtract(output, labels), labels))
                relative_error.extend(rmae)

                flow_l.extend(flow_len.tolist())
                design.extend((flow[:,0]-7).tolist())   
                


        tb_writer.add_scalar(args.dest_folder+"/MAPE", np.mean(relative_error), global_steps)
        output = pd.DataFrame({'design_name':design, 'flow_length':flow_l, 'labels': y_true, 'prediction': y_pred, 'relative error': relative_error})
        output.to_csv(args.dest_folder+'/logs/'+'/infer'+'_'+file+'.csv',index=False)
        with open(args.dest_folder+'/logs/'+'/testLog.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([int(re.findall(r'\d+', file)[1]), np.mean(relative_error)])
        
        global_steps+=1

def testing_inductive(model, device,
          optimizer,
          test_loader,
          graph_loader,
          args,
          tb_writer,
          if_std,
          criterion = nn.MSELoss(),
          ):
    
    with open(args.dest_folder+'/logs/'+'/testLog_inductive.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Epochs", "MAPE"])
    
    print(if_std)
    if if_std:
        scaler = joblib.load(args.data_folder+'/scaler.save')

    files = os.listdir(args.dest_folder)
    model_files = [f for f in files if f.endswith(".pt") and f.startswith("model")]

    model_files = sorted(model_files, key=lambda s: int(re.findall(r'\d+', s)[1]))
    print(model_files)

    global_steps = 0
    for file in model_files:
        load_checkpoint(args.dest_folder + '/'+file, model, optimizer, device)
    
        epoch_num = int(re.findall(r'\d+', file)[1])
        y_pred = []
        y_true = []
        relative_error = []
        flow_l = []
        design = []

        for graph_batch in graph_loader:
            graph_batch = graph_batch.to(device)

        model.eval()
        with torch.no_grad():
            for ((flow, flow_len), labels), _ in test_loader:         
                labels = labels.to(device)
                flow = flow.to(device)
                flow_len = flow_len.to("cpu")
                output, class_res = model(flow, flow_len, graph_batch)
                output = pred_ensemble(output, class_res, device)   
                if if_std:
                    output = (output*scaler.var_[0]**0.5)+scaler.mean_[0]
                    
                labels = labels.tolist()
                output = output.tolist()
                y_pred.extend(output)
                y_true.extend(labels)

                rmae = np.abs(np.divide(np.subtract(output, labels), labels))
                relative_error.extend(rmae)

                flow_l.extend(flow_len.tolist())
                design.extend((flow[:,0]-7).tolist())   
                

        tb_writer.add_scalar(args.dest_folder+"/MAPE_inductive", np.mean(relative_error), global_steps)
        output = pd.DataFrame({'design_name':design, 'flow_length':flow_l, 'labels': y_true, 'prediction': y_pred, 'relative error': relative_error})
        output.to_csv(args.dest_folder+'/logs/'+'/infer'+'_'+file+'_inductive.csv',index=False)
        with open(args.dest_folder+'/logs/'+'/testLog_inductive.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([int(re.findall(r'\d+', file)[1]), np.mean(relative_error)])
        
        global_steps+=1
def main():

    # arguments
    parser = argparse.ArgumentParser(description='Customized model for flow perf prediction')
    parser.add_argument('--device', type=int, default=0, help='which gpu to use if any (default: 0)')
    parser.add_argument('--batch_size', type=int, default=32, help='input batch size for training (default: 32)')
    parser.add_argument('--epochs', type=int, default=1, help='number of epochs to train (default: 300)')
    parser.add_argument('--emb_dim', type=int, default=20, help='dimensionality of input embedding of transformations')
    parser.add_argument('--graph_emb', type=int, default=32, help='dimensionality of hidden units in GNNs')
    parser.add_argument('--layer_num', type=int, default=2, help='Num of layer of GNNs')
    parser.add_argument('--lr', type = float, default=2e-3, help='Learning Rate')
    parser.add_argument('--task', type = str, choices=['delay', 'area'], help='The task')
    parser.add_argument('--mode', type=str, choices=['train', 'test', 'both', 'induct', 'all'], help='If the dataset is standardized')
    parser.add_argument('--model', type=str, choices=['D','EX', 'G', 'old', 'LL', 'Num'], default = 'D', help='If the dataset is standardized')
    parser.add_argument('--dest_folder', type=str)
    parser.add_argument('--data_folder', type=str)
    parser.add_argument('--if_std', type=int, default=0, help='If the dataset is standardized')

    
    args = parser.parse_args()

    data_folder = args.data_folder
    destination_folder = args.dest_folder
    if_std=bool(args.if_std)
    print(if_std)

    #create dest folders
    if os.path.exists(destination_folder):
        pass
    else:
        os.makedirs(destination_folder)
        os.makedirs(destination_folder+'/tb_writer')
        os.makedirs(destination_folder+'/logs')
    
    device = torch.device("cuda:" + str(args.device)) if torch.cuda.is_available() else torch.device("cpu")

    # Load graphs
    pyg_dataset = PygGraphPropPredDataset(root = 'utils/dataset_datapath', name = 'vgraph')
    graph_loader = DataLoader(pyg_dataset, batch_size=80, shuffle=False)

    # Fields
    flow_field = Field(lower=True, include_lengths=True, batch_first=True)
    if args.task == 'delay':
        delay_field = Field(sequential=False, use_vocab=False, batch_first=True, dtype=torch.float)
        fields = [ ('flow', flow_field), ('delay', delay_field)]
    elif args.task == 'area':
        area_field = Field(sequential=False, use_vocab=False, batch_first=True, dtype=torch.float)
        fields = [ ('flow', flow_field), ('area', area_field)]
    else:
        raise ValueError("No such task!")
    
    # TabularDataset
    print('Data loading from: {}'.format(data_folder))
    train, valid, test = TabularDataset.splits(path=data_folder, train='train.csv', validation='valid.csv', test='test.csv',
                                           format='CSV', fields=fields, skip_header=True)
    (index_train,)= TabularDataset.splits(path='data_area_trans_log', train='all_area.csv',
                                           format='CSV', fields=fields, skip_header=True)
    (valid_induct,) = TabularDataset.splits(path=data_folder, train='valid_inductive.csv',
                                           format='CSV', fields=fields, skip_header=True)
    # Iterators
    train_iter = BucketIterator(train, batch_size=args.batch_size, sort_key=lambda x: len(x.flow), device=device, sort=True, sort_within_batch=True)
    valid_iter = BucketIterator(valid, batch_size=128, sort_key=lambda x: len(x.flow), device=device, sort=True, sort_within_batch=True)
    test_iter = BucketIterator(test, batch_size=10000, sort_key=lambda x: len(x.flow), device=device, sort=True, sort_within_batch=True)
    valid_induct_iter = BucketIterator(valid_induct, batch_size=20000, sort_key=lambda x: len(x.flow), device=device, sort=True, sort_within_batch=True)
    # Vocabulary
    flow_field.build_vocab(index_train, min_freq=1, specials_first = False)
    print(vars(flow_field.vocab))

    
    learning_rate=float(args.lr)
    weight_decay=2e-6
    if args.model == 'D':
        model = Hybridmodel(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num).to(device)
    elif args.model == 'EX':
        model = Hybridmodel_ex(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num).to(device)
    elif args.model == 'LL':
        model = Hybridmodel_LL(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num).to(device)
    elif args.model == 'Num':
        model = Hybridmodel_Num(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num).to(device)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    
    #logs 
    tb_writer = SummaryWriter(destination_folder+'/tb_writer')

    if args.mode == 'train' or args.mode == 'both' or args.mode == 'all':
        training(model = model, device = device, optimizer = optimizer, args = args,\
            train_loader = train_iter, valid_loader = valid_iter, induct_valid_loader=valid_induct_iter, graph_loader = graph_loader, eval_every = len(train_iter), \
                num_epochs=args.epochs, tb_writer = tb_writer)
    
    if args.mode == 'test' or args.mode == 'both' or args.mode == 'all':
        testing(model = model, device = device, optimizer = optimizer, args = args,\
            test_loader = test_iter, graph_loader = graph_loader, tb_writer = tb_writer, if_std = if_std)
    
    if args.mode == 'induct' or args.mode =='all':
        (test_induct,)= TabularDataset.splits(path=data_folder, test='test_inductive.csv',
                                           format='CSV', fields=fields, skip_header=True)
        print(test_induct)
        test_induct_iter = BucketIterator(test_induct, batch_size=10000, sort_key=lambda x: len(x.flow), device=device, sort=True, sort_within_batch=True)
        testing_inductive(model = model, device = device, optimizer = optimizer, args = args,\
            test_loader = test_induct_iter, graph_loader = graph_loader, tb_writer = tb_writer, if_std = if_std)
     
    
if __name__ == "__main__":
    main()