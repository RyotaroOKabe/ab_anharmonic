import os
from os.path import join
mpids_file = '/home/ryotaro/phonon/nomad2phono3py/mpid_lists/natm2_scf1.txt'
nomaddir='/home/ryotaro/phonon/scf/'
psdir = "/home/ryotaro/phonon/ONCVPSP-PBEsol-PDv0.3/"
savedir = '/lustre/or-scratch/cades-virtues/proj-shared/phonon'
# savedir = '/home/ryotaro/phonon/'
jobdir=join(savedir, 'jobs/')
jobdir2=join(savedir, 'jobs2/')
logs_dir = join(savedir, 'logs/')
if not os.path.exists(jobdir):
	os.makedirs(jobdir)
if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
