from utils.job_manage import managing_job
from utils.read_abo import screen_incomplete
from dirs import *
mpid = '149' #'149'
njob =5
managing_job(jobdir2,mpid,njob)	 
screen_incomplete(jobdir2, f'{mpid}', run_job=True)	# check if all the jobs are completed and re-run if any of them is not perfect. 

