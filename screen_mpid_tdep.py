#%%
from utils.screen import *
from utils.tdep import *
from dirs import *

subid = '1'
ndim = 2
njob = 1    # number of parallel jobs
N=1
n=32
# cluster='ornl'
# queue='batch'    #'skylake'
maxdisps = None	# 3    # stop running job if certain number of disp-*abo are completed.
maxjobs = 40    # max number of jobs to submit at one time. 
screen='_'
other_screens = ['X']
run_phohno3py=False
run_tdep_init=False
check_progress= True
jobdir_run = jobdir2
all_jobdirs = [jobdir_run]  #, jobdir2]
temp = 300  # ttemperature for TDEP
max_freq = 20   # max frequency for TDEP
r_ss = 0.2  # ratio of the supercell files got by TDEP wrt phono3py
use_stdep=False # Use self-consistency i.e. sTDEP? 
# the mpids which has already run in ryotaro's account. We exclude these from job lists. 
skips = []

# prepare mpids to run
mpids = []
for mpids_f in mpids_files:
    with open(os.path.join(mpids_dir, mpids_f), 'r') as f:
        _mpids = f.readlines()
    mpids += _mpids

#%%
mpids = sorted([int(mpid[:-1]) for mpid in mpids])
print(mpids)
print('mpid: ', len(mpids))
# mpids = sorted([int(mpid) for mpid in mpids if mpid <= get_median(mpids)])  # split the job into half for ryotaro and qcsong account. 
mpids = [mpid for mpid in mpids if int(mpid) not in skips]
print(mpids)
print('mpid: ', len(mpids))
# mpids = mpids[:1]

#%%
if run_phohno3py:
    get_scripts(mpids,subid,nomaddir,jobdir_run,psdir,ndim,N,n,queue,screen=screen,njob=1,cluster=cluster,archive=run_tdep_init)

#%%
if run_tdep_init:
    tdep_cells_all(mpids, r_ss, [ndim,ndim,ndim], temp, max_freq, jobdir_run, stdep=use_stdep)

if check_progress:
    for mpid in mpids:
        counts = {'ss_files': 0, 'd_files': 0}
        jdir = join(jobdir_run, str(mpid))
        
        for file in os.listdir(jdir):
            if os.path.isfile(os.path.join(jdir, file)):
                if file.startswith('supercell-'):
                    counts['ss_files'] += 1
                elif file.startswith('disp-') and file.endswith('abo'):
                    counts['d_files'] += 1
        
        if counts['ss_files']==counts['d_files']:
            status = '--> done'
        else: 
            status = ''
        print(f'[{mpid}]: completed {counts["d_files"]} / {counts["ss_files"]} {status}')

        
        
#%%
screen_mpids(mpids, maxdisps, maxjobs, skips, jobdir_run, logs_dir, screen, queue, other_screens, all_jobdirs)

#%%
