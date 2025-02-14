import os
import re
import datetime
import numpy as np
from subprocess import check_output


def run_abc(input_file, command):
    abc_binary='abc'
    abc_command='read '+input_file+'; strash; '+command+' read 7nm_lvt_ff.lib; map -v; ps;'
    try:
        proc = check_output([abc_binary, '-c', abc_command])
        return proc
    except Exception as e:
        return None


# parse delay and area from the stats command of ABC
def get_metrics(stats):
    lines = stats.decode("utf-8").split('\n')
    for i in range(len(lines)):
        if 'area' in lines[i] and 'delay' in lines[i] and 'lev' in lines[i]:
            break

    line=lines[i].strip()
    ob = re.search(r'delay *= *[0-9]+.?[0-9]*', line)
    delay = float(ob.group().split('=')[1].strip())
        
    ob = re.search(r'area *= *[0-9]+.?[0-9]*', line)
    area = float(ob.group().split('=')[1].strip())

    return delay, area

# parse delay, area, and more stats from the stats command of ABC
def get_cnn_metrics(stats):
    lines = stats.decode("utf-8").split('\n')
    
    line = lines[-2]

    ob = re.search(r'delay *= *[0-9]+.?[0-9]*', line)
    delay = float(ob.group().split('=')[1].strip())
        
    ob = re.search(r'area *= *[0-9]+.?[0-9]*', line)
    area = float(ob.group().split('=')[1].strip())

    ob = re.search(r'nd *= *[0-9]*', line)
    nd = int(ob.group().split('=')[1].strip())

    ob = re.search(r'edge *= *[0-9]*', line)
    edge = int(ob.group().split('=')[1].strip())

    ob = re.search(r'lev *= *[0-9]*', line)
    lev = int(ob.group().split('=')[1].strip())

    ob = re.search(r'i/o *= *[0-9]* */ *[0-9]*', line)
    io = ob.group().split('=')[1].strip().split('/')
    i = int(io[0])
    o = int(io[1])

    return delay, area, edge, nd, lev, i, o
