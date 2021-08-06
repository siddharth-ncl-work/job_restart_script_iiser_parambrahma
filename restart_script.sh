#!/bin/sh
job_id=853010
job_name=test1
restart_script_name=restart_slurm_script

nohup python -u _restart.py $job_id $job_name $restart_script_name | tee output.log &


