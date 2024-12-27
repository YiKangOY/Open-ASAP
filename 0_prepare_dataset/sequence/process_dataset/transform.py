import os
import pandas as pd
import numpy as np
import sys
import json
flow_len = [20]
design_list = []
with open('../../designlist.txt', 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        design_list.append(line.strip())
map_delay_dict = {}
map_area_dict = {}
with open('./abc_output.jsonl') as f:
    lines = f.readlines()
    for line in lines:
        l = json.loads(line)
        map_delay_dict[l['name']] = l['delay']
        map_area_dict[l['name']] = l['area']


print(design_list)
new_name = []
for idx in range(len(design_list)):
    if idx<10:
        new_name.append('a{} '.format(idx%10))
    elif idx <20:
        new_name.append('b{} '.format(idx%10))
    elif idx < 30:
        new_name.append('c{} '.format(idx%10))
    elif idx < 40:
        new_name.append('d{} '.format(idx%10))
    elif idx < 50:
        new_name.append('e{} '.format(idx%10))
    elif idx < 60:
        new_name.append('f{} '.format(idx%10))
    elif idx < 70:
        new_name.append('g{} '.format(idx%10))
    elif idx < 80:
        new_name.append('h{} '.format(idx%10))
print(new_name)

#read flows
num_rows = 20000
flow_list = []
for item in flow_len:
    df = pd.read_csv('../run_abc/flow_{}.csv'.format(item), header=None, nrows=num_rows)
    flow_list.append(df)

flow = []
delay = []
area = []

data_path = '../abc_synthesized/'

train_mask = []
train_idx_list = []
train_mask_idx = 0
induct_mask = []
induct_idx_list = []
induct_mask_idx = 0

all_delay_list = []
all_area_list = []
all_multi_list = []

design_delay_list = []
design_area_list = []
design_multi_list = []

induct_list = [14, 2, 30, 11, 16]  
induct_delay_list = []
induct_area_list = []
induct_multi_list = []
for i in range(len(new_name)):
    design_name = design_list[i]
    # TODO
    print(design_name)
    if design_name=="hyp":
        continue
    design_flow_list = []
    local_delay_list = []
    local_area_list = []
    local_multi_list = []
    name_df = pd.DataFrame([new_name[i] for j in range(num_rows)])
    for idx in range(len(flow_list)):
        local_flow = flow_list[idx]

        ref_delay = map_delay_dict[design_name]
        ref_area = map_area_dict[design_name]
        # print(local_flow)
        local_flow[0] = local_flow[0].str.replace('resub -z','rsz')
        local_flow[0] = local_flow[0].str.replace('resub','rs')
        # print(local_flow)
        local_flow = name_df + local_flow
        # print(local_flow)
        local_area = pd.read_csv(data_path + 'area_ground_truth_' + design_name + '_flow_{}.csv'.format(flow_len[idx]), header = None, nrows=num_rows)
        local_delay = pd.read_csv(data_path + 'delay_ground_truth_' + design_name + '_flow_{}.csv'.format(flow_len[idx]), header = None, nrows=num_rows)
        # print(local_delay)
        # print(local_area)
        local_flow.columns = ['flow']
        local_area.columns = ['area']
        local_delay.columns = ['delay']


        local_delay['delay'] = np.divide(local_delay['delay'], map_delay_dict[design_name])
        local_area['area'] = np.divide(local_area['area'], map_area_dict[design_name])
        
        design_flow_list.append(local_flow)
        local_delay_list.append(local_delay)
        local_area_list.append(local_area)
        

    design_flow_list = pd.concat(design_flow_list)
    local_delay_list = pd.concat(local_delay_list)
    local_area_list = pd.concat(local_area_list)
    
    # print(design_flow_list)
    # print(local_delay_list)
    df_local_delay = pd.concat([design_flow_list, local_delay_list], axis=1)
    df_local_area = pd.concat([design_flow_list, local_area_list], axis=1)
    df_local_multi = pd.concat([design_flow_list, local_delay_list, local_area_list], axis=1)

    if i in induct_list:
        print(design_name)
        induct_delay_list.append(df_local_delay)
        induct_area_list.append(df_local_area)
        induct_multi_list.append(df_local_multi)
        
        induct_mask.append(induct_mask_idx)
        induct_mask_idx+=1
        train_mask.append(999)
        induct_idx_list.append(i)
    else:
        design_delay_list.append(df_local_delay)
        design_area_list.append(df_local_area)
        design_multi_list.append(df_local_multi)
        
        train_mask.append(train_mask_idx)
        train_mask_idx+=1
        induct_mask.append(999)
        train_idx_list.append(i)
    
    all_delay_list.append(df_local_delay)
    all_area_list.append(df_local_area)
    all_multi_list.append(df_local_multi)
        
df_design_delay = pd.concat(design_delay_list)
df_design_area = pd.concat(design_area_list)
df_design_multi = pd.concat(design_multi_list)

if len(induct_list) > 0:
    df_induct_delay=pd.concat(induct_delay_list)
    df_induct_area=pd.concat(induct_area_list)
    df_induct_multi=pd.concat(induct_multi_list)

df_all_delay = pd.concat(all_delay_list)
df_all_area = pd.concat(all_area_list)
df_all_multi = pd.concat(all_multi_list)

df_design_delay.to_csv('delay.csv', index=None)
df_design_area.to_csv('area.csv', index=None)
df_design_multi.to_csv('multi.csv', index=None)

if len(induct_list) > 0:
    df_induct_delay.to_csv('induct_delay.csv', index=None)
    df_induct_area.to_csv('induct_area.csv', index=None)
    df_induct_multi.to_csv('induct_multi.csv', index=None)

df_all_delay.to_csv('all_delay.csv', index=None)
df_all_area.to_csv('all_area.csv', index=None)
df_all_multi.to_csv('all_multi.csv', index=None)
    


destination_folder="temp"
first_n_words = 26
os.makedirs(destination_folder, exist_ok=True)
def trim_string(x):
    x = x.split(';',maxsplit=first_n_words)
    x = ' '.join(x[:first_n_words])
    return x

raw_data_path = 'multi.csv'
df_all = pd.read_csv('all_multi.csv')
df_all['flow'] = df_all['flow'].apply(trim_string)
df_all.to_csv(destination_folder + '/all_'+raw_data_path, index=False)

#process all data, used as index

df_all = pd.read_csv(raw_data_path)
df_all['flow'] = df_all['flow'].apply(trim_string)
# df_all.to_csv(destination_folder + '/all_'+raw_data_path, index=False)

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

train_test_ratio = 0.75
train_valid_ratio = 0.80

df_raw = shuffle(df_all, random_state=0)
# Train-test split
df_full_train, df_test = train_test_split(df_raw, train_size = train_test_ratio, shuffle = False)
print(len(df_full_train),len(df_test))
# Train-valid split
df_train, df_valid = train_test_split(df_full_train, train_size = train_valid_ratio, shuffle = False)
print(len(df_train),len(df_valid))

# Write preprocessed data
df_train.to_csv(destination_folder + '/train.csv', index=False)
df_valid.to_csv(destination_folder + '/valid.csv', index=False)
df_test.to_csv(destination_folder + '/test.csv', index=False)   


df_induct = pd.read_csv('induct_multi.csv')
df_induct['flow'] = df_induct['flow'].apply(trim_string)
df_induct = shuffle(df_induct, random_state=0)
df_induct.to_csv(destination_folder + '/induct.csv', index=False)
print(len(df_induct))

train_mask = np.array(train_mask)
induct_mask = np.array(induct_mask)
train_idx_list = np.array(train_idx_list)
induct_idx_list = np.array(induct_idx_list)

np.save(destination_folder+'/train_mask.npy', train_mask)
np.save(destination_folder+'/train_idx.npy', train_idx_list)
np.save(destination_folder+'/induct_mask.npy', induct_mask)
np.save(destination_folder+'/induct_idx.npy', induct_idx_list)