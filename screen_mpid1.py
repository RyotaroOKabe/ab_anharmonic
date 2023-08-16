from utils.screen import *
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
generate_scripts=False
jobdir_run = jobdir2
all_jobdirs = [jobdir2]  #, jobdir2]
# the mpids which has already run in ryotaro's account. We exclude these from job lists. 
skips = [22895, 22913]

# prepare mpids to run
with open(mpids_file, 'r') as f:
    mpids = f.readlines()
mpids = sorted([int(mpid[:-1]) for mpid in mpids])
print(mpids)
print('mpid: ', len(mpids))
# mpids = sorted([int(mpid) for mpid in mpids if mpid <= get_median(mpids)])  # split the job into half for ryotaro and qcsong account. 
mpids = [mpid for mpid in mpids if int(mpid) not in skips]
print(mpids)
print('mpid: ', len(mpids))

if generate_scripts:
    get_scripts(mpids,subid,nomaddir,jobdir_run,psdir,ndim,N,n,queue,screen=screen,njob=1,cluster=cluster)
screen_mpids(mpids, maxdisps, maxjobs, skips, jobdir_run, logs_dir, screen, queue, other_screens, all_jobdirs)
