import scheduler as sc
import pytest
import os
import subprocess


def test_init():
    new_sched = sc.Scheduler(5)
    assert new_sched.minute == 5

    result = subprocess.run(["crontab", "-l"], capture_output=True)
    stdout_as_str = result.stdout.decode("utf-8")
    assert stdout_as_str == "\n*/5 * * * * export DISPLAY=:0 && cd /home/joel/repos/test_demo && python3 initiator.py # Search for GPU task\n"

    subprocess.run(['crontab','-r'])

def test_change_minutes():
    new_sched_2 = sc.Scheduler(10)
    new_sched_2.change_minutes(5)
    assert subprocess.run(["crontab", "-l"], capture_output=True).stdout.decode("utf-8") == "\n*/5 * * * * export DISPLAY=:0 && cd /home/joel/repos/test_demo && python3 initiator.py # Search for GPU task\n"
    subprocess.run(['crontab', '-r'])

def test_make_cron_job():
    new_sched = sc.Scheduler(5)
    result = subprocess.run(["crontab", "-l"], capture_output=True)
    stdout_as_str = result.stdout.decode("utf-8")
    assert stdout_as_str == "\n*/5 * * * * export DISPLAY=:0 && cd /home/joel/repos/test_demo && python3 initiator.py # Search for GPU task\n"

    subprocess.run(['crontab','-r'])
