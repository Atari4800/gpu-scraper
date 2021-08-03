
"""This module priarily contains the Scheduler class, responsible for creating cronjobs. If it is run as a script,
then it will create a cronjob to run initiator.py regularly. The script would need an integer command line argument
to indicate how frequently initiator.py should be run. """

import os
import sys


from crontab import CronTab
import subprocess


def make_cron_job(minutes):
    """
    Creates a Scheduler object and creates the cron job for the gpu-hunter application.
    """
    minute = minutes
    cron = CronTab(user=True)
    halt_cron()
    currdir=str(os.getcwd())
    com = f'export DISPLAY=:0 && cd {currdir} && python3 initiator.py'
    job = cron.new(command = com)
    job.set_comment('Search for GPU task')
    print(f'CRON-JOB INITIATED FOR {minutes} MINUTES')
    job.minute.every(minute)
    cron.write()

def halt_cron():
    """
    Halts all gpu-hunter cron jobs.

    :return: 1 if a cron-job was found
    :return: 0 if a cron-job was not found.
    """
    cron = CronTab(user=True)
    success = 0
    for job in cron:
        if job.comment == 'Search for GPU task':
            cron.remove(job)
            cron.write()
            success = 1
    return success

class Scheduler:
    """
    Creates a cronjob to run initiator.py regularly, which would check all query sites for availability.
    """

    def __init__(self, minutes):
        """
        Creates a Scheduler object and creates the cron job.
        """
        self.minutes = minutes
        make_cron_job(minutes)

    def change_minutes(self, minutes):
        """
        Changes the value of minutes by killing the current cronjob and creating a new one with the desired minutes.

        :type min: integer
        :param minutes: The number of minutes the cron job will wait before calling scraper.py again.
        """
        subprocess.run(["crontab", "-r"])
        make_cron_job(minutes)



if __name__ == "__main__":
    sc = Scheduler(sys.argv[1])
    exit()
