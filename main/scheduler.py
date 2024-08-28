from datetime import timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from django.conf import settings
from main.tasks import send_mailing
from main.models import Mailing
import logging

logger = logging.getLogger(__name__)


def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)

    # Автоматический запуск запланированных рассылок
    mailings = Mailing.objects.filter(status="created", send_date__lte=timezone.now())
    for mailing in mailings:
        interval_mapping = {
            "once a minute": timedelta(minutes=1),
            "once a day": timedelta(days=1),
            "once a week": timedelta(weeks=1),
            "once a month": timedelta(days=30),
        }
        interval = interval_mapping.get(
            mailing.interval, timedelta(minutes=1)
        )  # Default to 1 minute if interval is not found

        scheduler.add_job(
            send_mailing,
            "interval",
            minutes=interval.total_seconds() / 60,  # Convert timedelta to minutes
            start_date=mailing.send_date,
            kwargs={"mailing_id": mailing.id},
        )
        logger.info(
            f"Scheduled job for mailing {mailing.id} every {mailing.interval} starting at {mailing.send_date}"
        )

    scheduler.start()
