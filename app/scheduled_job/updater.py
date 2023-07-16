from apscheduler.schedulers.background import BackgroundScheduler
from app.scheduled_job import *

class jobs:
    scheduler = BackgroundScheduler(timezone='Asia/Tashkent')
    # scheduler.add_job(, 'interval', minutes=5)
