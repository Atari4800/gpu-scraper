import scheduler as sc
import pytest
import os
import subprocess


def test_init():
    new_sched = sc.Scheduler(10)
    assert new_sched.minute == 10
    result = subprocess.run(["crontab", "-l"], capture_output=True)
    result = result.stdout.decode("utf-8")
    curr_dir = str(os.getcwd())
    com = "\n*/10 * * * * export DISPLAY=:0 && cd " + curr_dir + " && python3 initiator.py" + " # Search for GPU task\n"
    assert com == result
    print(com + '\n' + result)

    subprocess.run(['crontab', '-r'])


"""def test_changeMin():
    new_sched_2 = sc.Scheduler(10)
    new_sched_2.change_minutes(5)
    assert new_sched_2.minute == 5
    subprocess.run(['crontab', '-r'])
"""
