from django.apps import AppConfig
import os
from django.conf import settings

class bot(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'
    path = os.path.join(settings.BASE_DIR, 'bot')
    def ready(self):
        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE_BOT')
        if run_once is not None:
            return
        os.environ['CMDLINERUNNER_RUN_ONCE_BOT'] = 'True'
        from bot.scheduled_job.updater import jobs
        jobs.scheduler.start()
