import sys
from subprocess import run
import os



def process_design(design_path, file):
    design_path = design_path

    design_path = os.path.abspath(design_path)
    #read all files in filelist.f
    if design_path[len(design_path)-1] != '/':
        design_path = design_path+'/'

    try:
        run(['mkdir', 'yosys'], cwd=design_path)
    except:
        pass

    with open(design_path+'yosys/yosys.ys', 'w') as ys:

        ys.write('read_verilog '+design_path+file+'\n')

        ys.write('hierarchy -auto-top '+'\n')
        ys.write('flatten \n')
        
        ys.write('aigmap\n')
        ys.write('clean \n')
        ys.write('splitcells\n')
        ys.write('splitnets -ports \n')
        ys.write('aigmap\n')
        ys.write('clean \n')
        

        ys.write('write_json {}.json\n'.format(file.split('.')[0]))
        ys.write('write_aiger  {}.aig\n'.format(file.split('.')[0]))
        ys.write('write_verilog -noattr   {}_re.v\n'.format(file.split('.')[0]))
        
    #run yosys
    my_output = open(design_path+'yosys/'+file.split('.')[0]+'.yosyslog', 'w')
    run(['yosys', 'yosys.ys'], cwd=design_path+'yosys', stdout=my_output)


if __name__ == "__main__":
    path = '../../designs/'
    files = os.listdir(path)
    files = [f for f in files if f.endswith('.v')]
    for f in files:
        process_design(path, f)
