import scheduler as sc
import pytest
import subprocess

def test_init():
    new_sched = sc.Scheduler(10)
    assert new_sched.minute == 10
    subprocess.run(["crontab", "-l",">>","sched_time.txt"]).stdout == " */5 * * * * DISPLAY:=0 && Python3 scraper.py"

    subprocess.run(['crontab','-r'])
def test_changeMin():
    new_sched_2 = sc.Scheduler(10)
    new_sched_2.ChangeMinutes(5)
    assert new_sched_2.minute == 5
    subprocess.run(['crontab', '-r'])


