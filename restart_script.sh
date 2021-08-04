#!/bin/sh
job_name='a3_1'
restart_script_path='/scratch/kvanka/siddharth/restart_script'

nohup python -u _restart.py $job_name $restart_script_path | tee output.log &


