from utils.material import material
from utils.job_manage import managing_job
from utils.read_abo import abo_done
from utils.utilities import *
import os
from os.path  import join
import glob
import subprocess as sp
from collections import defaultdict
import time
import re
from datetime import datetime
import numpy as np
from periodictable import elements



def tdep_cell(mpid, idx, dims, temp, max_freq, jobdir):
    jdir = join(jobdir,str(mpid))
    nx,ny,nz = dims
    content, check_dict, lattice, frac, cart, znucls, typats = read_uc_abinit(jdir)
    write_uc_vasp(lattice, cart, znucls, typats, jdir)
    original_dir = os.getcwd()
    print("directory before tdep:", os.getcwd())
    os.chdir(jdir)
    print("directory for tdep:", os.getcwd())
    os.system(f'generate_structure --dimensions {nx} {ny} {nz}')
    os.system(f'cp outfile.ssposcar infile.ssposcar')
    os.system(f'canonical_configuration --quantum --maximum_frequency {max_freq} --temperature {temp} -n 1 --output_format 2')
    os.system(f'cp abinput_conf0001 supercell-{idx:0{5}d}.in')
    os.chdir(original_dir)
    combine_header_abinput(mpid, idx, jobdir)   #!
    print("directory after tdep:", os.getcwd())


def tdep_next_cell(mpid, dims, temp, max_freq, jobdir, stdep=False):
    jdir = join(jobdir,str(mpid))
    idx = count_files(jdir, 'supercell-') + 1
    if stdep:
        pass
    # TODO: sTDEP
    else:
        tdep_cell(mpid, idx, dims, temp, max_freq, jobdir)


def tdep_complete_cells(mpid, n_td, dims, temp, max_freq, jobdir, stdep=False):
    for i in range(n_td):
        tdep_next_cell(mpid, dims, temp, max_freq, jobdir, stdep)


def tdep_cells_all(mpids, r_ss, dims, temp, max_freq, jobdir, stdep=False):
    for mpid in mpids:
        jdir = join(jobdir,str(mpid))
        original_dir = os.getcwd()
        print("home dir:", os.getcwd())
        os.chdir(jdir)
        print("jdir:", os.getcwd())
        os.system(f'rm ./supercell-*.in')
        os.chdir(original_dir)
        print("home dir:", os.getcwd())
        n_p3 = count_files(join(jobdir, str(mpid), 'phono3py'), 'supercell-')
        n_td = int(n_p3 * r_ss)
        tdep_complete_cells(mpid, n_td, dims, temp, max_freq, jobdir, stdep)

def combine_header_abinput(mpid, idx, jobdir):
    # Define the filenames
    jdir = join(jobdir,str(mpid))
    header_filename = join(jdir, 'header.in') 
    supercell_filename = join(jdir, f'supercell-{idx:0{5}d}.in') 
    output_filename = join(jdir, f'disp-{idx:0{5}d}.in') 

    # Read the contents of the header file
    with open(header_filename, 'r') as header_file:
        header_contents = header_file.readlines()

    # Read the contents of the supercell file and filter out lines starting with 'mode'
    with open(supercell_filename, 'r') as supercell_file:
        supercell_contents = [line for line in supercell_file if not 'mode' in line]

    # Combine the contents
    combined_contents = header_contents + supercell_contents

    # Write the combined contents to the output file
    with open(output_filename, 'w') as output_file:
        output_file.writelines(combined_contents)

    print(f"Combined file saved as {output_filename}.")


def read_uc_abinit(jdir):
    with open(join(jdir, "pc.in"), "r") as f:
        content = f.readlines()
    content = [c[:-1] if c.endswith('\n') else c for c in content]
    print(content)
    checklist = ['xred', 'rprim', 'typat', 'znucl']
    check_dict = {}
    for c in checklist:
        for i, line in enumerate(content):
            if c in line:
                check_dict[c]=i
    print(check_dict)
    lattice = np.array([[float(item) for item in content[check_dict['rprim']+i+1].split()] for i in range(3)])
    # print('lattice: ', lattice)
    frac =  np.array([[float(item) for item in content[check_dict['xred']+i+1].split()] for i in range(check_dict['rprim']-check_dict['xred']-1)])
    # print('frac: ', frac)
    cart = frac@lattice
    # print('cart: ', cart)
    znucls = [elements[int(item)].symbol for item in content[check_dict['znucl']+1].split()]
    # print('znucls: ', znucls)
    typats = [int(item)-1 for item in content[check_dict['typat']+1].split()]
    # print('typats: ', typats)
    return content, check_dict, lattice, frac, cart, znucls, typats

def write_uc_vasp(lattice, cart, znucls, typats, jdir):
    lines = [" ".join(znucls), '1.000']
    for row in lattice:
        row_str = '    ' + "\t".join(map(str, row))
        lines.append(row_str)
    lines.append(' ' + "   ".join([znucls[i] for i in typats]))
    lines.append('  ' + "   ".join(['1' for i in typats]))
    lines.append('Cartesian')
    for row in cart:
        row_str = '  ' + "\t".join(map(str, row))
        lines.append(row_str)
    
    with open(join(jdir, "infile.ucposcar"), "w") as f:
        for line in lines:
            f.write(line + "\n")


def get_infile_positions(mpid, idx, jobdir):
    jdir = join(jobdir,str(mpid))
    input_filename = join(jdir, f'disp-{idx:0{5}d}.in')
    output_filename = join(jdir, 'infile.positions')
    with open(input_filename, 'r') as input_file:
        lines = input_file.readlines()
    output_lines = []
    found_xred = False
    for line in lines:
        if 'xred' in line:
            found_xred = True
            continue
        if 'vel' in line:
            break
        if found_xred and line.strip() and not line.startswith('#'):
            output_lines.append(line.split('#')[0].strip())
    with open(output_filename, 'w') as output_file:
        output_file.write('\n'.join(output_lines))
        
def get_infile_forces(mpid, idx, jobdir):
    jdir = join(jobdir,str(mpid))
    input_filename = join(jdir, f'disp-{idx:0{5}d}.abo')
    output_filename = join(jdir, 'infile.forces')
    with open(input_filename, 'r') as input_file:
        lines = input_file.readlines()

    output_lines = []
    found_cartesian_forces = False

    check_dict={}
    for i, line in enumerate(lines):
        if 'cartesian_forces' in line:
            check_dict['start']=i+1
        if 'force_length_stats' in line:
            check_dict['end']=i

    print(check_dict)
    for i in range(check_dict['start'], check_dict['end']):
        print(i)
        line = lines[i]
        cleaned_line = line[1:].replace('[', '').replace(']', '').replace(',', '').strip()
        output_lines.append(cleaned_line)
    with open(output_filename, 'w') as output_file:
        output_file.write('\n'.join(output_lines))


def get_infile_meta(mpid, temp, jobdir):
    jdir = join(jobdir,str(mpid))
    input_filename = join(jdir, 'infile.ssposcar')
    output_filename = join(jdir, 'infile.meta')
    num_atoms = 0
    with open(input_filename, 'r') as input_file:
        lines = input_file.readlines()
    lines = [c[:-1] if c.endswith('\n') else c for c in lines]

    for line in lines:
        if line.strip().endswith('coordinates'):
            num_atoms = sum([int(v) for v in lines[lines.index(line) - 1].split()])
            break
    with open(output_filename, 'w') as output_file:
        output_file.write(f"{num_atoms}\t# N atoms\n")
        output_file.write(f"0\t# N timesteps\n")
        output_file.write(f"1.0\t# timestep in fs\n")
        output_file.write(f"{temp}\t# temperature in K\n")


def get_infile_stat(mpid, jobdir):
    jdir = join(jobdir,str(mpid))
    output_filename = join(jdir, 'infile.stat')
    with open(output_filename, 'w') as output_file:
        output_file.write("0 1 1 1 1 1 1 1 1 1 1 1 1\n")
