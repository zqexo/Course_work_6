from apscheduler.schedulers.background import BackgroundScheduler

from mailing import settings
from main.tasks import send_mailing


def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_job(send_mailing, "interval", minutes=60)  # Запускать каждые 60 минут
    scheduler.start()
