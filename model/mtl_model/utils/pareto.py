import os
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import argparse
import torch
import numpy as np

def get_hypervolumn(delay_array, area_array):
    max_d = max(delay_array)
    min_d = min(delay_array)
    
    max_a = max(area_array)
    min_a = min(area_array)
    ref_d = 1.0
    ref_a = 1.0
    area = (ref_d-min_d) * (ref_a-min_a)
    if area == 0:
        return 0.0
    sum = 0

    delay_array = np.insert(delay_array,0, min_d)
    delay_array = np.append(delay_array, ref_d)
    area_array = np.insert(area_array,0, ref_a)
    area_array = np.append(area_array, min_a)
    for idx in range(len(delay_array)-1):
        sum+= (abs(area_array[idx+1] - area_array[idx])) * abs(delay_array[idx+1] - ref_d)
    return sum/area

def draw_pareto(path):
    df = pd.read_csv(path+'logs'+'/testLog.csv')
    infer_list = df.values.tolist()
    pareto_list = []
    for idx in range(len(infer_list)):
        cur_delay = infer_list[idx][1]
        cur_area = infer_list[idx][2]
        is_pareto = True
        
        for idx2 in range(len(infer_list)):
            if idx2 == idx:
                continue
            if (infer_list[idx2][1]<cur_delay) and (infer_list[idx2][2]<cur_area):
                is_pareto = False
        
        if is_pareto:
            pareto_list.append(infer_list[idx])
    
    fig, ax = plt.subplots(1,1)
    pareto = np.array(pareto_list)
    delay_array = pareto[:,1]
    area_array = pareto[:,2]
    p = delay_array.argsort()
    delay_array = delay_array[p]
    area_array = area_array[p]
    
    for idx in range(len(delay_array)):
        if delay_array[idx] >= 1.0 or area_array[idx]>=1.0:
            delay_array = np.delete(delay_array, idx)
            area_array = np.delete(area_array, idx)
            
    ax.scatter(delay_array, area_array)
    ax.plot(delay_array, area_array)
    for i,j in zip(delay_array,area_array):
        ax.annotate("Delay: {:.3f}\n".format(i) + "Area: {:.3f}".format(j),xy=(i,j))
    ax.set_ylabel("Area MAPE")
    ax.set_xlabel("Delay MAPE")
    HV = get_hypervolumn(delay_array, area_array)
    ax.set_title(path.split("_")[-1]+"HV: {:.3f}".format(HV))
    fig.savefig(path+'logs'+'/pareto.jpg')
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Customized model for flow perf prediction')
    parser.add_argument('--path', type=str)
    parser.add_argument('--std_path', type=str)
    args = parser.parse_args()
    
    

        
        

        

