from __future__ import print_function
import numpy as np
import pandas as pd
import os
import csv
import re
import sys
import pickle
from multiprocessing import Lock, Process, Queue, current_process


def print(*args):
    __builtins__.print(*("%.3f" % a if isinstance(a, float) else a
                         for a in args))
    

def main(path, idx):
    # print('In main')
    infer_f = pd.read_csv(path+'/logs/'+'infer_epo{}.csv'.format(idx))    
    induct_f = pd.read_csv(path+'/logs/'+'infer_indctive_epo{}.csv'.format(idx)) 


    infer_v = np.array(infer_f.values)
    induct_v = np.array(induct_f.values)

    delay_dict = {}
    area_dict = {}
    for item in infer_v:
        design = int(item[0])
        if design not in delay_dict.keys():

            delay_dict[design] = []
            area_dict[design] = []
        else:
            delay_dict[design].append([item[2], item[3]])
            area_dict[design].append([item[5], item[6]])



    for item in induct_v:
        design = int(item[0])
        if design not in delay_dict.keys():
            delay_dict[design] = []
            area_dict[design] = []
        else:
            delay_dict[design].append([item[2], item[3]])
            area_dict[design].append([item[5], item[6]])
        #The 1st is label 2nd is prediction

    pareto_min = {}

    for k in delay_dict.keys():

        value_d = delay_dict[k]
        value_a  = area_dict[k]
        pred_d = np.array(value_d)[:,1]
        pred_a = np.array(value_a)[:,1]
        label_d = np.array(value_d)[:,0]
        label_a = np.array(value_a)[:,0]

        min_pred_d = np.argmin(pred_d)
        min_pred_a = np.argmin(pred_a)
        label_min_d = label_d[min_pred_d]
        label_min_a = label_a[min_pred_a]
        
        pareto_min[k] = [label_min_d, label_min_a]

    res = func_group_min(pareto_min)
    return res, None

def func_group_min(pareto_min):

    adder_group = []
    for i in range(6):
        adder_group.append([j+6*i for j in range(6)])

    mul_group = []
    for i in range(5):
        mul_group.append([j+7*i + 36 for j in range(7)])


    design_group = []
    design_group.extend(adder_group)
    design_group.extend(mul_group)
    group_counter = 0
    group_pareto = {}
    for group in design_group:
        group_delay = np.array([])
        group_area = np.array([])
        
        for idx in group:

            group_delay = np.concatenate((group_delay, [pareto_min[idx][0]]))
            group_area = np.concatenate((group_area, [pareto_min[idx][1]]))
        group_min_d = min(group_delay)
        group_min_a = min(group_area)
        group_pareto[group_counter] = []
        group_pareto[group_counter].append([group_min_d, group_min_a])
        
        group_counter+=1
    return group_pareto
 
 
def run_all(epo_idx):
    try:
        cross, hv_cross = main(path = '../model_output/', idx=epo_idx)
    except:
        cross, hv_cross = None, None
        
    try:
        self_attn, hv_self = main(path= '../model_output/', idx=epo_idx)
    except:
        self_attn, hv_self = None, None
    try:
        lostin, hv_los = main(path = '../model_output/', idx=epo_idx)
    except:
        lostin, hv_los = None, None
    try:
        Two_E, hv_2E = main(path = '../model_output/', idx=epo_idx)
    except:
        Two_E, hv_2E = None, None
    try:
        proposed, hv_proposed = main(path = '../model_output/', idx =epo_idx)
    except:
        proposed, hv_proposed = None, None
    
    save_path = './dse'
    pareto_list = [lostin,Two_E, self_attn, cross,proposed]
    name_list = ['lostin', '2E', 'self', 'cross','proposed']

    for method_idx in range(len(pareto_list)):
        if pareto_list[method_idx] is not None:
            delay_points = pareto_list[method_idx]
            with open('{}/{}_min_epo{}.pkl'.format(save_path,name_list[method_idx], epo_idx), 'wb') as f:
                
                pickle.dump(delay_points, f)

                

if __name__ == '__main__':

    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()
    processes = []
    for idx in range(100):
        p = Process(target=run_all, args = (idx, ))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()