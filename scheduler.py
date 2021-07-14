"""
This module priarily contains the Scheduler class, responsible for creating cronjobs. If it is run as a script, then it will create a cronjob to run initiator.py regularly. The script would need an integer command line argument to indicate how frequently initiator.py should be run.
"""

import os, sys
from crontab import CronTab

class Scheduler:
    """
    Creates a cronjob to run initiator.py regularly, which would check all query sites for availability.
    """
    def __init__(self,minutes):
        """
        Creates a Scheduler object and creates the cron job.
        """
#        if(cron.find_command() > 0)

        self.minute=minutes
        self.cron = CronTab(user=True)
        basicIter = cron.find_comment('Search for GPU task')
        num=0
        for item in basicIter:
            num=num+1
            self.cron.remove(item)
        currdir=str(os.getcwd())
        com = 'export DISPLAY=:0 && cd ' + currdir + ' && python3 initiator.py'
        self.job = self.cron.new(command = com)
        self.job.set_comment('Search for GPU task')
        print('CRON-JOB INITIATED FOR '+minutes+ ' MINUTES')
        self.job.minute.every(self.minute)
        self.cron.write()
    def ChangeMinutes(min):
        """
        Changes the value of minutes. The thought is that it could change the frequency that initiator.py is run, but calling this method does not currently change the frequency of the existing cron job.

        :type min: integer
        :param min: The number of minutes the cron job will wait before calling scraper.py again.
        """
        self.minutes=min


if __name__ == "__main__":
    cron = CronTab(user = True)

    sc = Scheduler(sys.argv[1])
    exit()
