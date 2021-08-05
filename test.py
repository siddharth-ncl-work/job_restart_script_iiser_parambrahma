import subprocess
from subprocess import PIPE
import os
import time
import sys

job_id=850907
p=subprocess.Popen(['qstat','{}'.format(job_id)],stdout=PIPE,stderr=PIPE)
output=p.communicate()
print output
print
print output[0].split('\n')[2].split()[4]
