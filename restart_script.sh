#!/bin/sh
job_id=852957
job_name=test2
restart_script_path=/scratch/kvanka/siddharth/restart_script

nohup python -u _restart.py $job_id $job_name $restart_script_path | tee output.log &


