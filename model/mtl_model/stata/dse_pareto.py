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
    
def main(path, idx, if_debug = False):
    # if if_debug:
    #     print(path, idx)
    try:
        
        infer_f = pd.read_csv(path+'/logs/'+'infer_epo{}.csv'.format(idx))    
        induct_f = pd.read_csv(path+'/logs/'+'infer_indctive_epo{}.csv'.format(idx)) 
    except:
        return None, None
    
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

    pareto_delay_dict = {}
    pareto_area_dict = {}

    for k in delay_dict.keys():
        value_d = delay_dict[k]
        value_a  = area_dict[k]
        pred_d = np.array(value_d)[:,1]
        pred_a = np.array(value_a)[:,1]
        label_d = np.array(value_d)[:,0]
        label_a = np.array(value_a)[:,0]
        costs = np.dstack((pred_d, pred_a))
        costs = costs[0]
        pareto_delay_dict[k] = []
        pareto_area_dict[k] = []
        pareto_list_idx = is_pareto_efficient_dumb(costs)
        mask = np.where(pareto_list_idx==True)
        for p_idx in mask:
            pareto_delay_dict[k].append(label_d[p_idx])
            pareto_area_dict[k].append(label_a[p_idx])

    group_pareto = pareto_in_design_group(pareto_delay_dict, pareto_area_dict)

    hyperv= hyper_v_group(group_pareto)
    return group_pareto, hyperv

            


def is_pareto_efficient_dumb(costs, return_mask = True):

    """
    Find the pareto-efficient points
    :param costs: An (n_points, n_costs) array
    :param return_mask: True to return a mask
    :return: An array of indices of pareto-efficient points.
        If return_mask is True, this will be an (n_points, ) boolean array
        Otherwise it will be a (n_efficient_points, ) integer array of indices.
    """
    is_efficient = np.arange(costs.shape[0])
    n_points = costs.shape[0]
    next_point_index = 0  # Next index in the is_efficient array to search for
    while next_point_index<len(costs):
        nondominated_point_mask = np.any(costs<costs[next_point_index], axis=1)
        nondominated_point_mask[next_point_index] = True
        is_efficient = is_efficient[nondominated_point_mask]  # Remove dominated points
        costs = costs[nondominated_point_mask]
        next_point_index = np.sum(nondominated_point_mask[:next_point_index])+1
    if return_mask:
        is_efficient_mask = np.zeros(n_points, dtype = bool)
        is_efficient_mask[is_efficient] = True
        return is_efficient_mask
    else:
        return is_efficient

def pareto_in_design_group(pareto_delay_dict, pareto_area_dict):

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

            group_delay = np.concatenate((group_delay, pareto_delay_dict[idx][0]))
            group_area = np.concatenate((group_area, pareto_area_dict[idx][0]))
        cost_in_group = np.dstack((group_delay, group_area))
        cost_in_group = cost_in_group[0]
        group_pareto_idx = is_pareto_efficient_dumb(cost_in_group)
        group_pareto_idx = np.where(group_pareto_idx==True)
        
        group_pareto[group_counter] = []
        for p_idx in group_pareto_idx:
            group_pareto[group_counter].append([group_delay[p_idx], group_area[p_idx]])
        
        group_counter+=1
    return group_pareto

def hyper_v_group(group_pareto):
    hyper_v = {}
    with open('pareto_ref.pkl', 'rb') as f:
        ref_dict = pickle.load(f)
    for k in group_pareto.keys():
        # print(group_pareto[k])
        delay_list = group_pareto[k][0][0]
        area_list = group_pareto[k][0][1]
        
        p = np.argsort(delay_list)
        delay_list = delay_list[p]
        area_list = area_list[p]
        ref_d = ref_dict[k][0]
        ref_a = ref_dict[k][2]
        delay_list = np.insert(delay_list, 0, delay_list[0])
        area_list = np.insert(area_list, 0, ref_a)
        
        delay_list=np.append(delay_list, ref_d)
        area_list=np.append(area_list, area_list[-1])

        area = 0
        for idx in range(len(delay_list)-1):
            area+= np.abs(delay_list[idx]-delay_list[idx+1])*np.abs(ref_a-area_list[idx+1])
        area = area/(ref_a*ref_d)
        hyper_v[k] = area

    return hyper_v


def run_all(epo_idx):

    cross, hv_cross = main(path = '../model_output/', idx=epo_idx)

    self_attn, hv_self = main(path= '../model_output/', idx=epo_idx)

    lostin, hv_los = main(path = '../model_output/', idx=epo_idx)

    Two_E, hv_2E = main(path = '../model_output/', idx=epo_idx)

    proposed, hv_proposed = main(path = '../model_output/', idx =epo_idx, if_debug=True)
    
    save_path = './dse_pareto'
    pareto_list = [lostin,Two_E, self_attn, cross,proposed]
    hv_list = [hv_los, hv_2E, hv_self,   hv_cross, hv_proposed]
    name_list = ['lostin', '2E', 'self', 'cross','proposed']
    # print(hv_list)
    for idx in range(0,11):
            for method_idx in range(len(pareto_list)):
                if pareto_list[method_idx] is not None:
                    delay_points = pareto_list[method_idx][idx][0][0]
                    area_points = pareto_list[method_idx][idx][0][1]
                    np.save('{}/{}_{}_delay_epo{}'.format(save_path,name_list[method_idx], idx, epo_idx), delay_points)
                    np.save('{}/{}_{}_area_epo{}'.format(save_path,name_list[method_idx], idx, epo_idx), area_points)
                
    for method_idx in range(len(hv_list)):
        if hv_list[method_idx] is not None:
            with open('{}/{}_hyperv_epo{}.pkl'.format(save_path,name_list[method_idx], epo_idx ), 'wb') as f:
                pickle.dump(hv_list[method_idx],f)
            
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