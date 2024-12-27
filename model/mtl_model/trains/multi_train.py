### Libraries
import numpy as np
import argparse
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
import torch

# Preliminaries
import sys
sys.path.insert(0, 'utils')

# torchtext 0.6.0
from torchtext.data import Field, TabularDataset, BucketIterator
from torch.utils.tensorboard import SummaryWriter  
# Models
import torch.nn as nn

# Training
import torch.optim as optim

# graph loading dependency
from torch_geometric.loader import DataLoader
from dataset_pyg import PygGraphPropPredDataset
from gnn_cross import Hybridmodel_Cross, Hybridmodel_MTAN, Hybridmodel_Cross_Sep, Hybridmodel_MTA, Hybridmodel_MTA_sep, Hybridmodel_MTA_sep_EX, Hybridmodel_MTA_sep_ExProj, Hybridmodel_MTA_sep_ExEmb, Hybridmodel_MTA_sep_Ex_SinEMB
from gnn_cross import Hybridmodel_MTA_sep_ExLin, MTFormer_MLP, MTL_MLP, MTFormer_SELF, MTFormer_MLP_2

### aux
import os
import datetime
import joblib
import csv
import re

import random

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

def testing(model, device,
          optimizer,
          test_loader,
          graph_loader,
          args,
          tb_writer,
          if_std,
          criterion = nn.MSELoss(),
          best_valid_loss = float("Inf"), best_train_loss = float("Inf")):
    dest_files = os.listdir(args.dest_folder)
    model_files = [f for f in dest_files if f.endswith(".pt") and f.startswith("model")]
    model_files = sorted(model_files, key=lambda s: int(re.findall(r'\d+', s)[1]))

    infer_f = os.listdir(args.dest_folder+'/logs/')
    infer_f = [v for v in infer_f if v.endswith('.csv') and v.startswith('infer')]
    infer_f = sorted(infer_f, key=lambda s: int(re.findall(r'\d+', s)[0]))

    #remove infer files not belong to this run
    model_indices = [int(re.findall(r'\d+', f)[1]) for f in model_files]
    infer_f_indices = [int(re.findall(r'\d+', f)[0]) for f in infer_f]
    for idx in infer_f_indices:
        if idx not in model_indices:
            os.remove(args.dest_folder+'/logs/'+infer_f[idx])

    if len(infer_f) > 0:
        infer_idx = int(re.findall(r'\d+', infer_f[-1])[0])
        max_idx = 0
        for idx in range(len(model_files)):
            epoch_idx = int(re.findall(r'\d+', model_files[idx])[1])
            if epoch_idx > max_idx:
                max_idx = epoch_idx +1
        model_files = model_files[max_idx:len(model_files)]
    else:
        with open(args.dest_folder+'/logs/'+'/testLog.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["Epochs", "MAPE delay", "MAPE area"])
    
    if if_std:
        scaler_area = joblib.load(args.data_folder+'/scaler_area.save')
        scaler_delay = joblib.load(args.data_folder+'/scaler_delay.save')

    for file in model_files:
        load_checkpoint(args.dest_folder + '/'+file, model, optimizer, device)
        y_pred_a = []
        y_true_a = []
        relative_error_a = []
        y_pred_d = []
        y_true_d = []
        relative_error_d = []
        flow_l = []
        design = []

        for graph_batch in graph_loader:
            graph_batch = graph_batch.to(device)
        global_steps= 0
        model.eval()
        with torch.no_grad():
            for ((flow, flow_len), label_d, label_a), _ in test_loader:
                label_d = label_d.to(device)
                label_a= label_a.to(device)

                graph_lable=flow[:,0].to(device)
                flow = flow[:, 1:].to(device)
                flow_len = (flow_len-1).to("cpu")

                output_d, output_a, text_emb= model(flow, graph_lable, graph_batch)
                
                output_d = pred_func(output_d)   
                output_a = pred_func(output_a)   

                if if_std:
                    output_d = (output_d*(scaler_delay.var_[0]**0.5))+scaler_delay.mean_[0]
                    output_a = (output_a*(scaler_area.var_[0]**0.5))+scaler_area.mean_[0]

                output_d = output_d.tolist()
                output_a = output_a.tolist()
                
                label_d = label_d.tolist()
                label_a = label_a.tolist()
                y_pred_a.extend(output_a)
                y_true_a.extend(label_a)
                rmae_a = np.abs(np.subtract(output_a, label_a))
                relative_error_a.extend(rmae_a)
                
                y_pred_d.extend(output_d)
                y_true_d.extend(label_d)
                rmae_d = np.abs(np.subtract(output_d, label_d))
                relative_error_d.extend(rmae_d)

                flow_l.extend(flow_len.tolist())
                design.extend((graph_lable-7).tolist())
            global_steps+=1
        tb_writer.add_scalars(args.dest_folder+"/test_MAPE", {'MAPE delay': np.mean(relative_error_d), 'MAPE area': np.mean(relative_error_a)}, global_steps)
        output = pd.DataFrame({'design_name':design, 'flow_length':flow_l, 'label_d': y_true_d, 'prediction_d': y_pred_d, 'relative error delay': relative_error_d, 'label_a': y_true_a, 'prediction_a': y_pred_a, 'relative error area': relative_error_a})
        output.to_csv(args.dest_folder+'/logs/'+'infer_epo'+str(int(re.findall(r'\d+', file)[1]))+'.csv',index=False)
        print('relative error delay', np.mean(relative_error_d), 'relative error area', np.mean(relative_error_a))
        with open(args.dest_folder+'/logs/'+'/testLog.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([int(re.findall(r'\d+', file)[1]), np.mean(relative_error_d), np.mean(relative_error_a)])

def loss_func(criterion, pred, labels):
    loss = criterion(pred, labels)
    return loss

def pred_func(pred):
    return pred
    
def training(model, device,
          optimizer,
          train_loader,
          valid_loader,
          graph_loader,
          num_epochs,
          eval_every,
          if_std,
          args,
          tb_writer,
          criterion = nn.MSELoss(),
          best_valid_loss = float("Inf"), best_train_loss = float("Inf"),
          best_induct_valid_loss = float("Inf"), best_induct_mape_a = float('inf'), best_induct_mape_d = float('inf')
          ):
    
    # initialize running logs
    running_loss = 0.0
    running_loss_delay = 0.0
    running_loss_area = 0.0
    valid_running_loss = 0.0
    valid_running_loss_delay = 0.0
    valid_running_loss_area = 0.0
    global_step = 0
    train_loss_list = []
    valid_loss_list = []
    global_steps_list = []
    best_mape_a = float("Inf")
    best_mape_d = float("Inf")

    if if_std:
        scaler_area = joblib.load(args.data_folder+'/scaler_area.save')
        scaler_delay = joblib.load(args.data_folder+'/scaler_delay.save')
        
    #check if trained:
    models_f = os.listdir(args.dest_folder)
    models_f = [v for v in models_f if v.endswith('.pt') and v.startswith('model')]
    models_f = sorted(models_f, key=lambda s: int(re.findall(r'\d+', s)[1]))
    if len(models_f) > 0:
        start_epoch = int(re.findall(r'\d+', models_f[-1])[1]) + 1
        model.load_state_dict(torch.load(args.dest_folder+'/'+models_f[-1])['model_state_dict'])
        optimizer.load_state_dict(torch.load(args.dest_folder+'/'+models_f[-1])['optimizer_state_dict'])
    else:
        start_epoch = 0
        with open(args.dest_folder+'/logs/'+'/validLog.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["Epochs", "MAPE delay", "Loss delay", "MAPE area", "Loss area", "All loss"])
        with open(args.dest_folder+'/logs/'+'/valid_induct_Log.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["Epochs", "MAPE delay", "Loss delay", "MAPE area", "Loss area", "All loss"])

    # read graphs
    for graph_batch in graph_loader:
        graph_batch = graph_batch.to(device)
        
    model.train()
    print("Starting epoch: {}".format(start_epoch))
    for epoch in range(start_epoch, num_epochs):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('Train one epoch begins at: {}'.format(now))
        for ((flow, flow_len), label_d, label_a), _ in train_loader:         
            label_d = label_d.to(device)
            label_a= label_a.to(device)

            graph_lable=flow[:,0].to(device)
            flow = flow[:, 1:].to(device)
            flow_len = (flow_len-1).to("cpu")
            
            output_d, output_a, text_emb = model(flow, graph_lable, graph_batch)

            loss0_d = loss_func(criterion, output_d, label_d)
            loss0_a = loss_func(criterion, output_a, label_a)

            loss_d = loss0_d
            loss_a = loss0_a

            loss = loss_a + loss_d 

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
            # update running values
            running_loss += loss.item()
            running_loss_delay += loss_d.item()
            running_loss_area += loss_a.item()
            global_step += 1

        train_loss_list.append(loss.item())
        save_checkpoint(args.dest_folder + '/model_batch_'+str(args.batch_size)+'_epo'+str(epoch)+'.pt', model, optimizer, best_induct_valid_loss)        
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('Train one epoch ends at: {}'.format(now))
    save_metrics(args.dest_folder + '/metrics_batch_'+str(args.batch_size)+'.pt', train_loss_list, valid_loss_list, global_steps_list)
    print('Finished Training!')
    
def testing_inductive(model, device,
          optimizer,
          test_loader,
          graph_loader,
          args,
          tb_writer,
          if_std,
          criterion = nn.MSELoss(),
          best_valid_loss = float("Inf"), best_train_loss = float("Inf")):
    dest_files = os.listdir(args.dest_folder)
    model_files = [f for f in dest_files if f.endswith(".pt") and f.startswith("model")]
    model_files = sorted(model_files, key=lambda s: int(re.findall(r'\d+', s)[1]))
    print(model_files)

    induct_mask = np.load(args.data_folder+'/induct_mask.npy')
    induct_mask = torch.tensor(induct_mask)
    induct_mask = induct_mask.to(device)
    
    with open(args.dest_folder+'/logs/'+'/testLog_inductive.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Epochs", "MAPE delay", "MAPE area"])

    if if_std:
        scaler_area = joblib.load(args.data_folder+'/scaler_area.save')
        scaler_delay = joblib.load(args.data_folder+'/scaler_delay.save')
        
    global_steps = 0

    
    for file in model_files:
        load_checkpoint(args.dest_folder + '/'+file, model, optimizer, device)
        y_pred_a = []
        y_true_a = []
        relative_error_a = []
        y_pred_d = []
        y_true_d = []
        relative_error_d = []
        flow_l = []
        design = []

        for graph_batch in graph_loader:
            graph_batch = graph_batch.to(device)
        model.eval()
        with torch.no_grad():
            for ((flow, flow_len), label_d, label_a), _ in test_loader:
                label_d = label_d.to(device)
                label_a= label_a.to(device)
                graph_lable=flow[:,0].to(device)
                flow = flow[:, 1:].to(device)
                flow_len = (flow_len-1).to("cpu")

                output_d, output_a, text_emb = model(flow, flow_len, graph_batch)

                if if_std:
                    output_d = (output_d*(scaler_delay.var_[0]**0.5))+scaler_delay.mean_[0]
                    output_a = (output_a*(scaler_area.var_[0]**0.5))+scaler_area.mean_[0]


                output_d = output_d.tolist()
                output_a = output_a.tolist()
                label_d = label_d.tolist()
                label_a = label_a.tolist()

        
                y_pred_a.extend(output_a)
                y_true_a.extend(label_a)
                rmae_a = np.abs(np.divide(np.subtract(output_a, label_a), label_a))
                relative_error_a.extend(rmae_a)
                
                y_pred_d.extend(output_d)
                y_true_d.extend(label_d)
                rmae_d = np.abs(np.divide(np.subtract(output_d, label_d), label_d))
                relative_error_d.extend(rmae_d)


                flow_l.extend(flow_len.tolist())
                design.extend((graph_lable-7).tolist())

        output = pd.DataFrame({'design_name':design, 'flow_length':flow_l, 'label_d': y_true_d, 'prediction_d': y_pred_d, 'relative error delay': relative_error_d, 'label_a': y_true_a, 'prediction_a': y_pred_a, 'relative error area': relative_error_a})
        output.to_csv(args.dest_folder+'/logs/'+'infer_indctive_epo'+str(int(re.findall(r'\d+', file)[1]))+'.csv',index=False)
        print('relative error delay', np.mean(relative_error_d), 'relative error area', np.mean(relative_error_a))
        with open(args.dest_folder+'/logs/'+'/testLog_inductive.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([int(re.findall(r'\d+', file)[1]), np.mean(relative_error_d), np.mean(relative_error_a)])
        global_steps+=1
   
 


def main():

    # arguments
    parser = argparse.ArgumentParser(description='Customized model for flow perf prediction')
    parser.add_argument('--device', type=int, default=0, help='which gpu to use if any (default: 0)')
    parser.add_argument('--batch_size', type=int, default=32, help='input batch size for training (default: 32)')
    parser.add_argument('--epochs', type=int, default=1, help='number of epochs to train (default: 300)')
    parser.add_argument('--emb_dim', type=int, default=20, help='dimensionality of input embedding of transformations')
    parser.add_argument('--graph_emb', type=int, default=32, help='dimensionality of hidden units in GNNs')
    parser.add_argument('-l', '--layer_num', type=int, default=2, help='Num of layer of GNNs')
    parser.add_argument('--model', type=str, choices=['cross', 'cross_sep', 'mta_sep', "mta_sep_g", 'mta_sep_ex', 'mta_sep_ex_proj', 'mta_sep_ex_emb', 'mta_sep_ex_sinemb', 'mta_exlin', "MTF", "MTF_SELF", "MLP","MTF_WITHOUT_GNN_ATTN_CLASS","MTF_2","MTF_2_WITHOUT_GNN"], help='Num of layer of GNNs')
    parser.add_argument('--lr', type = float, default=2e-3, help='Learning Rate')
    parser.add_argument('--mode', type=str, choices=['train', 'test', 'both', 'induct', 'all'], help='If the dataset is standardized')
    parser.add_argument('--weight', type=str, choices=['None', 'dwa'], default = 'None', help='weight averaging')
    parser.add_argument('--dest_folder', type=str)
    parser.add_argument('--data_folder', type=str)
    parser.add_argument('--graph_folder', type=str)
    parser.add_argument( '-std' ,'--if_std', type=int, default=0, help='If the dataset is standardized')
    parser.add_argument('-pre','--pretrain_dir', nargs='+', required=False,  help='The pretrain model for mtl model')
    parser.add_argument('-i', '--init_cross', nargs='+', required=False, help='The initailization of cross model')
    parser.add_argument('--cross_lr', type=int, required=False, help='The learning rate for cross unit')
    parser.add_argument('--num_heads', type=int, default=2, help="Num heads in mta")
    parser.add_argument('--seed', type=int, help="random seed")

    args = parser.parse_args()

    data_folder = args.data_folder
    destination_folder = args.dest_folder
    graph_folder=args.graph_folder
    if_std = int(args.if_std)
    if_std=bool(if_std)
    print("If std:", if_std)

    if args.seed is not None:
        set_seed(args.seed)

    #create dest folders
    if os.path.exists(destination_folder):
        pass
    else:
        os.makedirs(destination_folder)
        os.makedirs(destination_folder+'/tb_writer')
        os.makedirs(destination_folder+'/logs')
    
    device = torch.device("cuda:" + str(args.device)) if torch.cuda.is_available() else torch.device("cpu")

    print(graph_folder)
    pyg_dataset = PygGraphPropPredDataset(root = graph_folder, name = 'vgraph')

    train_loader = DataLoader(pyg_dataset, batch_size=80, shuffle=False)

    
    # Fields
    area_field = Field(sequential=False, use_vocab=False, batch_first=True, dtype=torch.float, fix_length = 26)
    delay_field = Field(sequential=False, use_vocab=False, batch_first=True, dtype=torch.float, fix_length = 26)
    flow_field = Field(lower=True, include_lengths=True, batch_first=True, fix_length = 26)
    fields = [ ('flow', flow_field), ('delay', delay_field), ('area', area_field)]
    

    if not args.mode == 'induct':
        train, valid, test = TabularDataset.splits(path=data_folder, train='train.csv', validation='valid.csv', test='test.csv',
         format='CSV', fields=fields, skip_header=True)
        
    (index_train,) = TabularDataset.splits(path=data_folder, train='all_multi.csv', 
                                           format='CSV', fields=fields, skip_header=True)

    if not args.mode == 'induct':
        train_iter = BucketIterator(train, batch_size=args.batch_size, device=device, sort=False,shuffle=True)
        valid_iter = BucketIterator(valid, batch_size=args.batch_size, device=device, sort=False,shuffle=True)
        test_iter = BucketIterator(test, batch_size=args.batch_size, device=device, sort=False,shuffle=True)


    flow_field.build_vocab(index_train, min_freq=1, specials_first = False)
 
    learning_rate=float(args.lr)
    weight_decay=2e-6

    if (args.model =='cross' or args.model == 'cross_sep'):
        if args.model =='cross':
            model = Hybridmodel_Cross(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num).to(device)
        elif args.model == 'cross_sep':
            model = Hybridmodel_Cross_Sep(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num).to(device)
        if  args.mode == 'train':
            if args.init_cross is not None:
                assert len(args.init_cross) ==2, "The length of init list should be 2"
                for item in args.init_cross:
                    assert (float(item) <=1.0 and float(item) >=0.0), "The cross value init should between 0.0 and 1.0"
                model.init_cross(float(args.init_cross[0]), float(args.init_cross[1]))
            
            if args.pretrain_dir is not None:
                assert len(args.pretrain_dir) ==2, "The length of init model should be 2"
                model.init_pretrain(args.pretrain_dir[0], args.pretrain_dir[1], device)
        
    elif args.model == 'mtan':
        model = Hybridmodel_MTAN(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num).to(device)
    elif args.model == 'mta':
        model = Hybridmodel_MTA(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num).to(device)
    elif args.model == 'mta_sep':
        model = Hybridmodel_MTA_sep(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num, num_heads=args.num_heads).to(device)
    elif args.model == 'mta_sep_ex':
        model = Hybridmodel_MTA_sep_EX(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num, num_heads=args.num_heads).to(device)
    elif args.model == 'mta_sep_ex_proj':
        model = Hybridmodel_MTA_sep_ExProj(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num, num_heads=args.num_heads).to(device)
    elif args.model == 'mta_sep_ex_emb':
        model = Hybridmodel_MTA_sep_ExEmb(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num, num_heads=args.num_heads).to(device)
    elif args.model == 'mta_sep_ex_sinemb':
        model = Hybridmodel_MTA_sep_Ex_SinEMB(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num, num_heads=args.num_heads).to(device)
    elif args.model == 'mta_exlin':
        model = Hybridmodel_MTA_sep_ExLin(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num, num_heads=args.num_heads).to(device)
    elif args.model == 'MTF':
        model = MTFormer_MLP(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num, num_heads=args.num_heads).to(device)
    elif args.model == 'MLP':
        model = MTL_MLP(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num, num_heads=args.num_heads).to(device)
    elif args.model == 'MTF_SELF':
        model = MTFormer_SELF(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num, num_heads=args.num_heads).to(device)
    elif args.model == 'MTF_WITHOUT_GNN_ATTN_CLASS':
        model = MTFormer_MLP_WITHOUT_GNN_ATTN_CLASS(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, layers = args.layer_num, num_heads=args.num_heads).to(device)
    elif args.model == 'MTF_2':
        model = MTFormer_MLP_2(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num, num_heads=args.num_heads).to(device)
    elif args.model == 'MTF_2_WITHOUT_GNN':
        model = MTFormer_MLP_2_WITHOUT_GNN(input_dim=len(flow_field.vocab), emb_dim=args.emb_dim, graph_emb=args.graph_emb, layers = args.layer_num, num_heads=args.num_heads).to(device)
    
    if (args.model =='cross' or args.model == 'cross_sep') and args.cross_lr != None:
        parameters = []
        # append layer parameters
        for name, param in model.named_parameters():
            if param.requires_grad:
                if 'cross' in name:
                    parameters += [{'params': [p for n, p in model.named_parameters() if n == name and p.requires_grad],'lr': learning_rate*args.cross_lr}]
                else:
                    parameters += [{'params': [p for n, p in model.named_parameters() if n == name and p.requires_grad],'lr': learning_rate}]
        optimizer = optim.Adam(parameters, lr=learning_rate, weight_decay=weight_decay)
    else:
        optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    
    if args.pretrain_dir is not None:
        load_checkpoint(args.pretrain_dir[0],model, optimizer, device)

    #logs 
    tb_writer = SummaryWriter(destination_folder+'/tb_writer')


    if args.mode == 'train' or args.mode == 'both' or args.mode =='all':
        training(model = model, device = device, optimizer = optimizer, args = args,\
            train_loader = train_iter, valid_loader = valid_iter ,graph_loader = train_loader, eval_every = len(train_iter), \
                if_std = if_std, num_epochs=args.epochs, tb_writer = tb_writer)
    
    if args.mode == 'test' or args.mode == 'both' or args.mode =='all' :
        testing(model = model, device = device, optimizer = optimizer, args = args, test_loader = test_iter, graph_loader = train_loader, tb_writer = tb_writer, if_std = if_std)
    if args.mode == 'induct' or args.mode =='all' or args.mode == 'test':
        (test_induct,)= TabularDataset.splits(path=data_folder, test='induct.csv',
                                           format='CSV', fields=fields, skip_header=True)

        test_induct_iter = BucketIterator(test_induct, batch_size=10000, sort_key=lambda x: len(x.flow), device=device, sort=True, sort_within_batch=True)
        testing_inductive(model = model, device = device, optimizer = optimizer, args = args,\
            test_loader = test_induct_iter, graph_loader = train_loader, tb_writer = tb_writer, if_std = if_std)
     
    
if __name__ == "__main__":
    main()