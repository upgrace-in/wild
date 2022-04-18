from apscheduler.schedulers.background import BackgroundScheduler
import automate
#automate.start()
scheduler = BackgroundScheduler()
scheduler.add_job(automate.start, 'interval', minutes=30)
scheduler.start()
