from apscheduler.schedulers.background import BackgroundScheduler
from bot.scheduled_job import mailing

class jobs:
    scheduler = BackgroundScheduler(timezone='Asia/Tashkent')
    scheduler.add_job(mailing.send_message, 'interval', minutes=5)