import os, sys
from crontab import CronTab

class Scheduler:
    def __init__(self,minutes):
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
        self.minutes=min


if __name__ == "__main__":
    cron = CronTab(user = True)

    sc = Scheduler(sys.argv[1])
    exit()
