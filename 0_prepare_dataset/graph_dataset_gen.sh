1. v2json
cd ./graph/v2json
python ./process_design.py
python ./graph_gen.py
Output: ./graph/results/new_graph_json

# 2. json2csv
cd ../../
cd ./graph/json2csv
python ./features.py
Output: ./graph/results/new_graph_dataset/vgraph

# 3. csv2pyg
cd ../../
cd ./graph/csv2pyg
python ./dataset_pyg.py
Output: ./graph/results/new_graph_dataset/vgraph/processed

