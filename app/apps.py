from django.apps import AppConfig
import os
from django.conf import settings

class app(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    path = os.path.join(settings.BASE_DIR, 'app')
    # def ready(self):
    #     run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE')
    #     if run_once is not None:
    #         return
    #     os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True'
    #     from app.scheduled_job.updater import jobs
    #     jobs.scheduler.start()
