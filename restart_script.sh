#!/bin/sh
job_id=853162
job_name=test1
restart_script_name=0restart_slurm_script
max_restart_limit=1000

#=================================
nohup python -u _restart.py $job_id $job_name $restart_script_name $max_restart_limit| tee output.log &


