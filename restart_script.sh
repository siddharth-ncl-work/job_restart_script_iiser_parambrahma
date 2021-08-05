#!/bin/sh
job_id=852987
job_name=water
restart_script_name=restart_script

nohup python -u _restart.py $job_id $job_name $restart_script_path | tee output.log &


