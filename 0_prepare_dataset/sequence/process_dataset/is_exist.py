import os

data_path = '../../abc_synthesized/'
design_list = []

# 读取 design_list 文件中的内容
with open('../../results/designlist.txt', 'r') as f:
    design_list = [line.strip() for line in f]

# 获取 data_path 目录下的所有文件名（不包括路径）
files_in_data_path = os.listdir(data_path)

# 找出 design_list 中不在 data_path 文件名中的元素（即不被包含）
not_in_data_path = []
for design in design_list:
    if not any(design in filename for filename in files_in_data_path):
        not_in_data_path.append(design)

# 打印或处理不在 data_path 中的设计
if not_in_data_path:
    print("以下设计在 data_path 中未找到包含它们的文件:")
    for design in not_in_data_path:
        print(design)
else:
    print("所有设计都在 data_path 中找到对应文件。")
