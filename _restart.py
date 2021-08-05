import subprocess
from subprocess import PIPE
import os
import time
import sys


def qFlag(job_name):
  q_flag='not_defined'
  p=subprocess.Popen(['qstat'],stdout=PIPE,stderr=PIPE)
  output=p.communicate()[0]
  if job_id in output.split():
    q_flag='running'
  else:
    q_flag='not_running'
  return q_flag

def jobDirFlag(job_dir_path,job_id):
  if not os.path.isdir(job_dir_path):
    return 'dir_not_present'
  if not os.listdir(job_dir_path):
    return 'dir_empty'
  dscf_file_path=os.path.join(job_dir_path,'dscf.out')
  if not os.path.isfile(dscf_file_path):
    return None
  else:
    if '****  dscf : all done  ****' in open(dscf_file_path,'r').read():
      return 'converged'
    else:
      stderr_flag=stderrFlag(job_id)
      return stderr_flag
  return 'job_dir_flag_not_defined'

def stderrFlag(job_id):
  stderr_file_path='../sp_slurm_script.e{0}'.format(job_id)
  stderr_file=open(stderr_file_path,'r')
  stderr=stderr_file.read()
  stderr_file.close()
  if 'DUE TO TIME LIMIT' in stderr:
    return 'running'
  else:
    return 'failed'

def restartJob(restart_script_name):
  restart_script_path='../{0}'.format(restart_script_name)
  subprocess.Popen(['qsub',restart_script_path])

def checkJob(job_name,job_dir_path,restart_script_name,job_id):
  stop_flag=False
  q_flag=qFlag(job_name)
  job_dir_flag=jobDirFlag(job_dir_path,job_id)
  print 'Job:{0} is {1} dscf.out {2}'.format(job_name,q_flag,job_dir_flag)
  if q_flag=='not_running':
    stop_flag=True
    if job_dir_flag=='dir_not_present':
      print 'job directory: {0} is not present'.format(job_dir_path)
    elif job_dir_flag=='dir_empty':
      print 'job directory: {0} is empty'.format(job_dir_path)
    elif job_dir_flag is None:
      print 'File dscf.out is not present'
    elif job_dir_flag.lower()=='running':
      print 'RESTARTING THE JOB'
      restartJob(restart_script_name)
      stop_flag=False
    elif job_dir_flag.lower()=='converged':
      print 'JOB FINISHED'
    elif job_dir_flag.lower()=='failed':
      print 'JOB ERROR: please check input and output files and resubmit'
    else:
      print 'unknown job_dir_flag {0}'.format(job_dir_flag)
  elif q_flag=='running':
    stop_flag=False
    """
    if job_dir_flag=='dir_not_present':
      print 'search directory: {0} is not present'.format(job_dir_path)
    elif job_dir_flag=='dir_empty':
      print 'job directory: {0} is empty'.format(job_dir_path)
    elif job_dir_flag is None:
      print 'File dscf.out is not present'
    elif job_dir_flag.lower()=='running':
      pass
    elif job_dir_flag.lower()=='converged':
      print 'JOB FINISHED'
      stop_flag=True
    elif job_dir_flag.lower()=='failed':
      print 'JOB ERROR: please check input and output files and resubmit'
      stop_flag=True
    else:
      print 'unknown job_dir_flag {}'.format(job_dir_flag)
    """
  return stop_flag

start_time=time.time()
print(sys.argv)
job_id=sys.argv[1]
job_name=sys.argv[2]
job_dir_path='../tmp/{0}'.format(job_name)
restart_script_name=sys.argv[3]
interval=1
stop_flag=False
while not stop_flag:
  time.sleep(interval)
  elapsed_time=round(time.time()-start_time,2)
  print 'Time elapsed {0} seconds'.format(elapsed_time)
  stop_flag=checkJob(job_name,job_dir_path,restart_script_name,job_id)
  if stop_flag:
    print('Terminating the programme')

