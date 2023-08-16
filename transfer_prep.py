from utils.screen import *
from dirs import *
import os

delete_heavy = True
jobdir_dict = {'jobs': jobdir, 'jobs2': jobdir2}
keys = list(jobdir_dict.keys())
completed1 = sorted(completed_jobs(jobdir))
print(f'completed in jobs/ ({len(completed1)}):', completed1)
completed2 = sorted(completed_jobs(jobdir2))
print(f'completed in jobs2/ ({len(completed2)}):', completed2)
completed= completed1+completed2
print('total: ', len(completed))

delete_ext = ['*DEN.nc', '*GSR.nc', '*WFK.nc']


if delete_heavy:
    jfolders = sorted(os.listdir(jobdir))
    for jfolder in jfolders:
        jdir = os.path.join(jobdir, jfolder)
        for delt in delete_ext:
            file = os.path.join(jdir, delt)
            print(file)
            os.system(f'rm {file}')
            
    jfolders2 = sorted(os.listdir(jobdir2))
    for jfolder in jfolders2:
        jdir = os.path.join(jobdir2, jfolder)
        for delt in delete_ext:
            file = os.path.join(jdir, delt)
            print(file)
            os.system(f'rm {file}')

