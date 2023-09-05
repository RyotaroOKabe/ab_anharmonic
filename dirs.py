import os
from os.path import join
# mpids_file = '/home/ryotaro/phonon/ab_anharmonic/mpid_lists/natm2_scf1.txt'
mpids_dir = '/work2/09337/ryotaro/frontera/abinit_ro/ab_anharmonic/mpid_lists'
nomaddir='/work2/09337/ryotaro/frontera/abinit_ro/scf/'
psdir = "/work2/09337/ryotaro/frontera/abinit_ro/ONCVPSP-PBEsol-PDv0.3/"
savedir = '/work2/09337/ryotaro/frontera/abinit_ro/ab_anharmonic'
# savedir = '/home/ryotaro/phonon/'
jobdir=join(savedir, 'jobs_tdep/')
logs_dir = join(savedir, 'logs/')
if not os.path.exists(jobdir):
	os.makedirs(jobdir)
if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
mpids_files = ['natm2_scf1.txt', 'natm3_scf1.txt']






