from crontab import CronTab

class Scheduler:
    def __init__(self,minutes):
        self.minute=minutes
        self.cron = CronTab(user=True)
        self.job = self.cron.new(command = 'export DISPLAY=:0 && cd ~/Desktop/GPUHUNTER/ && ls -l && python3 ~/Desktop/GPU>
 #       self.job = self.cron.new(command = 'echo "Eat" >> diditgo.txt') #This is a test-line for the jobs.
        self.job.minute.every(self.minute)
        print(self.cron.write())
    def ChangeMinutes(min):
        self.minutes=min
    def check():
        for jobs in self.cron:
            print(jobs)
sc = Scheduler(1)
sc.check

