
"""This module priarily contains the Scheduler class, responsible for creating cronjobs. If it is run as a script,
then it will create a cronjob to run initiator.py regularly. The script would need an integer command line argument
to indicate how frequently initiator.py should be run. """

import os
import sys


from crontab import CronTab
import subprocess


class Scheduler:
    """
    Creates a cronjob to run initiator.py regularly, which would check all query sites for availability.
    """

    def __init__(self, minutes):
        """
        Creates a Scheduler object and creates the cron job.
        """
        #        if(cron.find_command() > 0)

        self.minute = minutes
        self.cron = CronTab(user=True)

        basic_iter = self.cron.find_comment('Search for GPU task')
        num = 0
        for item in basic_iter:
            num = num + 1

            self.cron.remove(item)
        curr_dir = str(os.getcwd())
        com = 'export DISPLAY=:0 && cd ' + curr_dir + ' && python3 initiator.py'
        self.job = self.cron.new(command=com)
        self.job.set_comment('Search for GPU task')
        print('CRON-JOB INITIATED FOR ' + str(minutes) + ' MINUTES')
        self.job.minute.every(self.minute)
        self.cron.write()


    def ChangeMinutes(self, minutes):
        """
        Changes the value of minutes by killing the current cronjob and creating a new one with the desired minutes.

        :type min: integer
        :param min: The number of minutes the cron job will wait before calling scraper.py again.
        """
        subprocess.run(["crontab", "-r"])

        self.minute=minutes
        self.cron = CronTab(user=True)
        basicIter = self.cron.find_comment('Search for GPU task')
        num=0
        for item in basicIter:
            num += 1
            self.cron.remove(item)
        currdir=str(os.getcwd())
        com = 'export DISPLAY=:0 && cd ' + currdir + ' && python3 initiator.py'
        self.job = self.cron.new(command = com)
        self.job.set_comment('Search for GPU task')
        print('CRON-JOB INITIATED FOR '+str(minutes)+ ' MINUTES')
        self.job.minute.every(self.minute)
        self.cron.write()



if __name__ == "__main__":
    sc = Scheduler(sys.argv[1])
    exit()
