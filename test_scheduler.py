import scheduler
import pytest
import os

cron = CronTab(user = True)

def test_init():
    new_sched = Scheduler(10)
    assert new_sched.minutes == 10
    assert os.subprocess.run(crontab -l) == " */5 * * * * DISPLAY:=0 && Python3 scraper.py"

def test_changeMin():
    new_sched_2 = Scheduler(10)
    new_sched_2.ChangeMinutes(5)
    assert new_sched_2.minutes == 5


