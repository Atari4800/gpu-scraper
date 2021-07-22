import scheduler as sc
import pytest
import os
import subprocess

def test_init():
    new_sched = sc.Scheduler(10)
    assert new_sched.minutes == 10
    result = subprocess.run(["crontab", "-l"], capture_output=True)
    result = result.stdout.decode("utf-8")
    curr_dir = str(os.getcwd())
    com = "\n*/10 * * * * export DISPLAY=:0 && cd " + curr_dir + " && python3 initiator.py" + " # Search for GPU task\n"
    assert com == result

    subprocess.run(['crontab', '-r'])

def test_change_minutes():
    new_sched_2 = sc.Scheduler(10)
    new_sched_2.change_minutes(5)
    curr_dir = str(os.getcwd())
    result = subprocess.run(["crontab", "-l"], capture_output=True).stdout.decode("utf-8")
    com = "\n*/5 * * * * export DISPLAY=:0 && cd " + curr_dir + " && python3 initiator.py" + " # Search for GPU task\n"
    assert com == result
    subprocess.run(['crontab', '-r'])

def test_make_cron_job():
    new_sched = sc.Scheduler(5)
    result = subprocess.run(["crontab", "-l"], capture_output=True)
    stdout_as_str = result.stdout.decode("utf-8")
    curr_dir = str(os.getcwd())
    assert stdout_as_str == f"\n*/5 * * * * export DISPLAY=:0 && cd {curr_dir} && python3 initiator.py # Search for GPU task\n"

    subprocess.run(['crontab','-r'])
