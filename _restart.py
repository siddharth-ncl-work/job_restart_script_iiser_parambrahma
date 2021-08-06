import subprocess
from subprocess import PIPE
import os
import time
import sys


def qFlag():
  q_flag='not_defined'
  p=subprocess.Popen(['qstat'],stdout=PIPE,stderr=PIPE)
  output=p.communicate()[0]
  if job_id in output.split():
    q_flag='running'
  else:
    q_flag='not_running'
  return q_flag

def jobDirFlag():
  dscf_file_path=os.path.join(job_dir_path,'dscf.out')
  if os.path.isfile(dscf_file_path):
    if '****  dscf : all done  ****' in open(dscf_file_path,'r').read():
      return 'converged'
  
  stderr_flag=stderrFlag()
  return stderr_flag

def stderrFlag():
  stderr_file_name=None
  for file_name in os.listdir(stderr_dir_path):
    if 'e{0}'.format(job_id) in file_name:
      stderr_file_name=file_name
  if stderr_file_name is None:
    return 'failed'
  stderr_file_path='{0}/{1}'.format(stderr_dir_path,stderr_file_name)
  stderr_file=open(stderr_file_path,'r')
  stderr=stderr_file.read()
  stderr_file.close()
  if 'DUE TO TIME LIMIT' in stderr:
    return 'need_restart'
  else:
    return 'failed'

def restartJob():
  #restart_script_path='../{0}'.format(restart_script_name)
  p=subprocess.Popen(['qsub',restart_script_name],cwd='..',stdout=PIPE,stderr=PIPE)
  output=p.communicate()[0]
  return output  

def checkJob():
  global job_name,job_dir_path,restart_script_name,job_id,stderr_dir_path,max_restart_limit,curr_restart_count,pid
  stop_flag=False
  q_flag=qFlag()
  job_dir_flag=jobDirFlag()
  if q_flag=='not_running':
    print '[{4}] Job:{0}-{1} is {2} dscf.out {3}'.format(job_name,job_id,q_flag,job_dir_flag,pid)
    stop_flag=True
    if job_dir_flag.lower()=='need_restart':
      if curr_restart_count<max_restart_limit:
        print 'RESTARTING THE JOB - {0}'.format(curr_restart_count)
        output=restartJob()
        print output
        #job_id=output.strip().split('\n')[0]
        print '[{3}] job_id={0}, stderr_dir_path={1}'.format(job_id,stderr_dir_path,pid)
        stop_flag=False
        curr_restart_count+=1
      else:
        print 'restart limit reached {0}={1}'.format(curr_restart_count,max_restart_limit)
        stop_flag=True
    elif job_dir_flag.lower()=='converged':
      print 'JOB FINISHED'
    elif job_dir_flag.lower()=='failed':
      print 'JOB ERROR: please check input and output files and resubmit'
    else:
      print 'unknown job_dir_flag {0}'.format(job_dir_flag)
  elif q_flag=='running':
    stop_flag=False
    print '[3] Job:{0}-{1} is {2}'.format(job_name,job_id,q_flag,pid)
    if job_dir_flag.lower()=='converged':
      print 'JOB FINISHED'
      stop_flag=True
  return stop_flag

start_time=time.time()
print(sys.argv)
job_id=sys.argv[1]
job_name=sys.argv[2]
job_dir_path='../{0}'.format(job_name)
restart_script_name=sys.argv[3]
max_restart_limit=int(sys.argv[4])
stderr_dir_path='..'
interval=1
curr_restart_count=0
pid=os.getpid()
stop_flag=False
while not stop_flag:
  time.sleep(interval)
  elapsed_time=round(time.time()-start_time,2)
  print 'Time elapsed {0} seconds'.format(elapsed_time)
  stop_flag=checkJob()
  if stop_flag:
    print('Terminating the programme')

