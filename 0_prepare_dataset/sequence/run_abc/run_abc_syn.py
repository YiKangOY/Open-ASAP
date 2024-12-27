import utils
import pandas as pd
import numpy as np
import argparse
import pprint as pp
import os
import sys
from multiprocessing import Lock, Process, Queue, current_process
from tqdm import tqdm



def main(args, len_part, idx):
    if int(args['flow_length'])==10:
        ff=pd.read_csv('flow_10.csv',header=None)
    elif int(args['flow_length'])==15:
        ff=pd.read_csv('flow_15.csv',header=None)
    elif int(args['flow_length'])==20:
        ff=pd.read_csv('flow_20.csv',header=None)
    else:
        ff=pd.read_csv('flow_25.csv',header=None)

    # print(idx)
    ff=np.array(ff)
    length = int(len(ff)/len_part)
    ff = ff[length*idx:length*(idx+1)]
    Delays=[0 for i in range(len(ff))]
    Areas=[0 for i in range(len(ff))]

    e=[]
    for i in tqdm(range(len(ff)), desc=f'Processing flow length {args["flow_length"]}, Part {idx}', unit='item'):
        stat=utils.run_abc(str(args['input']),str(ff[i][0]))
        if stat == None:
            e.append(i)
            continue
        delay, area = utils.get_metrics(stat)
        Delays[i]=delay
        Areas[i]=area

        if np.mod(i,1000)==0:
            print(i)

        if np.mod(i+1,10000)==0 and i!=len(ff):
            result_area=pd.DataFrame(Areas)
            result_delay=pd.DataFrame(Delays)

            filename=str(args['input']).split('/')[-1].split('.')[0]
            filepath = str(args['dest'])
            result_area.to_csv(filepath+'area_ground_truth_'+filename+'_flow_'+str(args['flow_length'])+'_part_'+str(int(i/10000))+'.csv',index=False,header=False)
            result_delay.to_csv(filepath+'delay_ground_truth_'+filename+'_flow_'+str(args['flow_length'])+'_part_'+str(int(i/10000))+'.csv',index=False,header=False)
    
    result_area=pd.DataFrame(Areas)
    result_delay=pd.DataFrame(Delays)

    filename=str(args['input']).split('/')[-1].split('.')[0]
    filepath = str(args['dest'])
    result_area.to_csv(filepath+'area_ground_truth_'+filename+'_flow_'+str(args['flow_length'])+'_idx_'+str(idx)+'.csv',index=False,header=False)
    result_delay.to_csv(filepath+'delay_ground_truth_'+filename+'_flow_'+str(args['flow_length'])+'_idx_'+str(idx)+'.csv',index=False,header=False)
    if len(e)>0:
        error=pd.DataFrame(e)
        error.to_csv('failures_'+filename+'_flow_'+str(args['flow_length'])+'.csv',index=False,header=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='provide arguments for the actor critic')

    parser.add_argument('--flow-length', help='the number of optimizations in each synthesis flow', default=10)
    parser.add_argument('--input', help='the name of input verilog file', default='FFTRocket/IBuf.aig')
    parser.add_argument('--dest', help='destination of syntesized data', default='../abc_synthesized/')
    
    flow_len = [20]
    src_files = os.listdir('mul/yosys/')
    files = [f for f in src_files if f.endswith('.aig')]
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()
    processes = []
    
    len_part = 10
    idx = 0
    for f in files:
        for flow in flow_len:
            for idx in range(len_part):
                args = vars(parser.parse_args())
                args['flow_length'] = flow
                args['input']='../../designs/yosys/' + f
                p = Process(target=main, args = (args, len_part, idx))
                processes.append(p)
                p.start()
    for p in processes:
        p.join()
