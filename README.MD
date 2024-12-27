# ASAP: Accurate Synthesis Analysis and Prediction with Multi-Task Learning
Yikang Ouyang, Sicheng Li, Dongsheng Zuo, Hanwei Fan, Yuzhe Ma. In  2023 ACM/IEEE 5th Workshop on Machine Learning for CAD (MLCAD), [paper](https://ieeexplore.ieee.org/abstract/document/10299840).

Contact: youyang929 [ $\alpha$ $\tau$ ] connect.hkust-gz.edu.cn (for anti-spam purpose, sorry for the inconvenience)

## Benchmarks
1. EPFL 15 benchmark [EPFL15](https://github.com/lsils/benchmarks)
2. ISCAS 85 Dataset [ISCAS85](https://web.eecs.umich.edu/~jhayes/iscas.restore/benchmark.html)
3. Online adder generator [Adder](https://github.com/IamFlea/AdderCircuitGenerator)
4. In-house multipliers with compressor trees.

## Environment
The required python environment is shown in `requirements.txt`, the python version is 3.9.16. Some packages are out-of-dated so you may install them mannually.
For GPU support, please refer to official channel of PyG and PyTorch and download the version that suits your CUDA version; [PyG](https://anaconda.org/pyg/pyg), [PyTorch](https://anaconda.org/pytorch/pytorch)
CUDA must be install in your computer for GPU support, our cuda version is cuda 11.7.

Opensource EDA tools needed: [yosys](https://github.com/YosysHQ/yosys), [abc](https://github.com/berkeley-abc/abc).


## Code Structure
1. Preprocessing RTL into graphs
    ```
    cd 0_prepare_dataset
    ./graph_dataset_gen.sh
    ```
    This will generate graph data for MAPE evaluation, the designs are listed in `0_prepare_dataset/designlist.txt`
    
    For datapath designs, please modify paths in python scripts executed in `graph_dataset_gen.sh` and change `designs` to `datapath`, `designlist.txt` to `datapah_list.txt`.
2. Synthesizing sequences 

    You may synthesize sequences to obtain delay and area by your own, or you can directly use our synthesized sequence dataset.
    The library for synthesizing can be found in <https://github.com/scale-lab/DRiLLS/issues/10> or [LOSTIN](https://github.com/lydiawunan/LOSTIN).
    Synthesizing sequence (**This requries many cores and much time**): 
    ```
    cd 0_prepare_dataset/sequence/run_abc
    python run_abc_syn.py
    #After synthesizing with those sequences, you may merge results for each design into a single csv file
    0_prepare_dataset/sequence/process_dataset/collect_design.ipynb
    ```
    
    Alternatively, you can directly use the synthesized sequence with delay and area labels.
    ```
    tar -zxvf abc_synthesized.tar.gz # The 39 designs for MAPE evaluation
    tar -zxvf datapath_synthesized.tar.gz # The 35 adders and 36 multipliers for design space exploration.
    ```
    After obtaining the raw dataset, there are some preprocessing, like the split of train/valid/test sets.
    This can be found in `0_prepare_dataset/sequence/process_dataset/transform.py`, you can directly execute it, the generated dataset will be stored in `temp` dir.

## Multi-task Learning Model Training and inference.
1. Training  and inference:
    ```
    cd model/mtl_model
    ./train_mtl.sh
    ```
    If the "mode" in `train_mtl.sh` is set to `both`, it will do training and transductive testing, if set to `all`, it will do training, transductive testing, and inductive testing.
2. Models

    Models are defined in  `model/mtl_model/utils/gnn_cross.py`. For baseline models, please refer to [LOSTIN](https://github.com/lydiawunan/LOSTIN).

## DSE evaluation
This path contains scripts for computing hypervolumn for evaluating design space exploration results.  
In `model/mtl_model/stata/dse_pareto.py`, fill the model output log csv files and it can compute pareto frontier based on model prediction.

## Citation
If you find our work helpful, please consider cite our work:
```
@INPROCEEDINGS{Ouyang2023ASAP,
  author={Ouyang, Yikang and Li, Sicheng and Zuo, Dongsheng and Fan, Hanwei and Ma, Yuzhe},
  booktitle={2023 ACM/IEEE 5th Workshop on Machine Learning for CAD (MLCAD)}, 
  title={ASAP: Accurate Synthesis Analysis and Prediction with Multi-Task Learning}, 
  year={2023},
  pages={1-6},
  }
```