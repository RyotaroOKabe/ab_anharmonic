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


def tdep_cell(mpid, idx, dims, temp, max_freq, jobdir):
    jdir = join(jobdir,str(mpid))
    nx,ny,nz = dims
    os.system(f'cd {jdir}: generate_structure --dimensions {nx} {ny} {nz} --output_format 2')
    os.rename(join(jdir,'outfile.ssposcar'), join(jobdir,'infile.ssposcar'))
    os.system(f'cd {jdir}: canonical_configuration --quantum --maximum_frequency {max_freq} --temperature {temp} -n 1 --output_format 2')
    os.rename(join(jdir,'outfile.ssposcar'), join(jobdir,'infile.ssposcar'))
    os.rename(join(jdir,'abinput_conf0001'), join(jobdir,f'supercell-{idx:0{5}d}.in'))


def tdep_next_cell(mpid, dims, temp, max_freq, jobdir, stdep=False):
    idx = count_files(jobdir, 'supercell-') + 1
    if stdep:
        pass
    else:
        tdep_cell(mpid, idx, dims, temp, max_freq, jobdir)


def tdep_complete_cells(mpid, n_td, dims, temp, max_freq, jobdir, stdep=False):
    for i in range(n_td):
        tdep_next_cell(mpid, dims, temp, max_freq, jobdir, stdep)


def tdep_cells_all(mpids, r_ss, dims, temp, max_freq, jobdir, stdep=False):
    for mpid in mpids:
        n_p3 = count_files(jobdir, 'supercell-')
        n_td = int(n_p3 * r_ss)
        tdep_complete_cells(mpid, n_td, dims, temp, max_freq, jobdir, stdep)
