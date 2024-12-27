import json
import os
import sys
import pathpy as pp
import networkx as nx
import pickle

input_num_list = []
output_num_list = []
# Graph class
class Graph:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._num_ANDs = 0
        self._num_NOTs = 0
        self._num_INPUT = 0
        self._num_OUTPUT = 0

    def create_node(self, node_name, node_type):
        node_dict = {
            'node_type': node_type, 
            'neighbors': []
        }
        self._graph.add_node(node_name, node_attributes=node_dict)

    def remove_node(self, node_name):
        self._graph.remove_node(node_name)

    # Assume unweighted edge at the moment...
    def connect(self, node_l, node_r):
        self._graph.add_edge(v=node_l, w=node_r)

    def disconnect(self, node_l, node_r):
        self._graph.remove_edge(v=node_l, w=node_r)
        
    def _get_operater_node(self, oper_type):
        if oper_type == '$_AND_':
            node_type = f'&_{self._num_ANDs}'
            self._num_ANDs += 1
        elif oper_type == '$_NOT_':
            node_type = f'~_{self._num_NOTs}'
            self._num_NOTs += 1
        else:
            raise NotImplementedError

        return node_type
    
    def generate_verilog_graph(self, name, port_dict, cell_dict, nets_dict):
        self._name = name

        for k,v in port_dict.items():
            if v['direction'] == 'input':
                self._graph.add_node(k, type= 'input')
                if len(v['bits'])>1:
                    raise ValueError("Number of connecting bits >1", k, v)
                self._graph.add_node('wire_'+str(v['bits'][0]), type= 'inter')
                self._graph.add_edge(k, 'wire_'+str(v['bits'][0]))
            elif v['direction'] == 'output' :
                if len(v['bits'])>1:
                    raise ValueError("Number of connecting bits >1", k, v)
                self._graph.add_node(k, type= 'output')
                self._graph.add_node('wire_'+str(v['bits'][0]), type= 'inter')
                self._graph.add_edge('wire_'+str(v['bits'][0]), k)
            else:
                raise ValueError("Invalid io def", v)
                
        for k,v in cell_dict.items():

            node_type= self._get_operater_node(v['type'])
            self._graph.add_node(node_type, type= v['type'])
            for conn, wire_num in v['connections'].items():
                if conn == 'Y':
                    #output port, the edge goes from node to wire

                    self._graph.add_node('wire_'+str(wire_num[0]), type= 'inter')
                    self._graph.add_edge(node_type, 'wire_'+str(wire_num[0]))
                elif conn == 'A' or conn == 'B':

                    self._graph.add_node('wire_'+str(wire_num[0]), type= 'inter')
                    self._graph.add_edge('wire_'+str(wire_num[0]), node_type)
                else: 
                    raise ValueError("Undefined conn in cells")            
        #optimize graph
        wire_nodes = []
        for n in self._graph.nodes():
            if 'wire_' in n:
                wire_nodes.append(n)

                in_edge = self._graph.in_edges(n)
                
                for e in in_edge:
                    source_node = e[0]
                out_edge = self._graph.out_edges(n)
                target_node = []
                for e in out_edge:
                    target_node.append(e[1])
                    
                for target in target_node:
                    self._graph.add_edges_from([(source_node, target)])
                
                
        for n in wire_nodes:
            self._graph.remove_node(n)
            
        num_and = 0
        num_not = 0
        num_i = 0
        num_o = 0
        for n in self._graph.nodes():
            if self._graph.nodes[n]['type'] == '$_NOT_':
                num_not+=1
            elif self._graph.nodes[n]['type'] == '$_AND_':
                num_and+=1
            elif self._graph.nodes[n]['type'] == 'input':
                num_i+=1
            elif self._graph.nodes[n]['type'] == 'output':
                num_o+=1
            else:
                raise ValueError("Undefined node type, {}, {}".format(n, self._graph.nodes[n]['type']))
        
        input_num_list.append(num_i)
        output_num_list.append(num_o)
        return self._graph
        

    

def parse_json(design_path, filename, dest_path):
    G_Process = Graph()
    with open(design_path+filename, 'r') as f:
        json_dict = json.load(f)                    #keys: dict_keys(['creator', 'modules'])
        json_modules = json_dict['modules']         #keys: dict_keys(['test'])
        top_key = list(json_modules.keys())

        top_dict = json_modules[top_key[0]]      #keys: dict_keys(['attributes', 'ports', 'cells', 'netnames'])

        ports_dict = top_dict['ports']         #keys: port names, eg: dict_keys(['clk', 'data_1', 'data_2', 'res_add', 'res_sub'])
        cells_dict = top_dict['cells']         #keys: cell names, eg: dict_keys(['_4_', '_5_', '_6_', '_7_'])
        nets_dict = top_dict['netnames']       #keys: net names, eg: dict_keys(['_0_', '_1_', '_2_', '_3_', 'clk', 'data_1', 'data_2', 'res_add', 'res_sub'])

        # print(ports_dict)
        G = G_Process.generate_verilog_graph(top_key, ports_dict, cells_dict, nets_dict)

        f = open(dest_path + '/{}.json'.format(filename.split('.')[0]), 'w')
        G_dict = dict(nodes=[[n, G.nodes[n]] for n in G.nodes()], \
                    edges=[(e[0], e[1], G.edges[e]) for e in G.edges()])
        json.dump(G_dict, f)
        f.close()
        
    return ports_dict, cells_dict, nets_dict


if __name__ == '__main__':
    path = '../../designs/yosys/' 
    files = os.listdir(path)
    dest_path = '../results/new_graph_json'

    os.makedirs(dest_path, exist_ok=True)


    files = [f for f in files if f.endswith('.json')]
    
    for filename in files:
        parse_json(path, filename, dest_path)
    

    with open('../results/io.txt', 'w') as f:
        print(input_num_list, file=f)
        print(output_num_list, file=f)