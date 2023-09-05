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
    print('check2', f'cd {jdir} | cp abinput_conf0001 supercell-{idx:0{5}d}.in')
    os.chdir(original_dir)
    print("directory after tdep:", os.getcwd())

    # os.system(f'cd {jdir} | generate_structure --dimensions {nx} {ny} {nz}')
    # # os.rename(join(jdir,'outfile.ssposcar'), join(jdir,'infile.ssposcar'))
    # os.system(f'cd {jdir} | cp outfile.ssposcar infile.ssposcar')
    # print('check0')
    # os.system(f'cd {jdir} | canonical_configuration --quantum --maximum_frequency {max_freq} --temperature {temp} -n 1 --output_format 2')
    # print('check1', f'cd {jdir} | canonical_configuration --quantum --maximum_frequency {max_freq} --temperature {temp} -n 1 --output_format 2')
    # os.system(f'cd {jdir} | cp abinput_conf0001 supercell-{idx:0{5}d}.in')
    # print('check2', f'cd {jdir} | cp abinput_conf0001 supercell-{idx:0{5}d}.in')

def tdep_next_cell(mpid, dims, temp, max_freq, jobdir, stdep=False):
    jdir = join(jobdir,str(mpid))
    idx = count_files(jdir, 'supercell-') + 1
    if stdep:
        pass
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
