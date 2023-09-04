#%%
from utils.screen import *
from utils.tdep import *
from dirs import *

subid = '1'
ndim = 2
njob = 1    # number of parallel jobs
N=1
n=32
cluster='ornl'
queue='skylake'
maxdisps = None	# 3    # stop running job if certain number of disp-*abo are completed.
maxjobs = 5    # max number of jobs to submit at one time. 
screen='_'
other_screens = ['X']
run_phohno3py=False
run_tdep_init=True
jobdir_run = jobdir2
all_jobdirs = [jobdir2]  #, jobdir2]
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

if run_phohno3py:
    get_scripts(mpids,subid,nomaddir,jobdir_run,psdir,ndim,N,n,queue,screen=screen,njob=1,cluster=cluster)
if run_tdep_init:
    use_tdep_all()
    
screen_mpids(mpids, maxdisps, maxjobs, skips, jobdir_run, logs_dir, screen, queue, other_screens, all_jobdirs)

#%%
