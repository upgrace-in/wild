from apscheduler.schedulers.background import BackgroundScheduler
import automate
from fire_alert import settings

if settings.DEBUG == True:
    automate.start()
else:
    scheduler = BackgroundScheduler()
    scheduler.add_job(automate.start, 'interval', minutes=30)
    scheduler.start()
