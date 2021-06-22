from crontab import CronTab
import os.path
class Scheduler:
	def _init_(minutes):
		myCron=CronTab(user = True)
		for job in myCron:
			print(job)
	def removeAllJobs:
		myCron.remove_all()
	def searchItems:
		myCron(
