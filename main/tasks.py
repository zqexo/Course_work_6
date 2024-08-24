import pytz

from django.conf import settings
from django.core.mail import send_mail
from main.models import Mailing, TryMailing
from datetime import datetime, timedelta

import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def send_mailing():
    logger.info("Starting mailing process")
    # Определяем текущую дату и время в заданной временной зоне
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    # Фильтруем рассылки, которые должны быть отправлены
    mailings = Mailing.objects.filter(send_date__lte=current_datetime).filter(
        status__in=["created", "started"]
    )

    logger.info(f"Found {mailings.count()} mailings to process")

    for mailing in mailings:
        last_try = (
            TryMailing.objects.filter(mailing=mailing).order_by("-last_try").first()
        )
        interval_mapping = {
            "once a minute": timedelta(minutes=1),
            "once a day": timedelta(days=1),
            "once a week": timedelta(weeks=1),
            "once a month": timedelta(
                days=30
            ),  # или используйте библиотеку dateutil для точного подсчета
        }

        if (
            last_try is None
            or (current_datetime - last_try.last_try)
            >= interval_mapping[mailing.interval]
        ):
            # Отправляем письма клиентам
            recipients = [client.email for client in mailing.email.all()]
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=recipients,
                )
                status = "success"
                response = "Emails sent successfully"
                logger.info("Emails sent successfully")
            except Exception as e:
                status = "failure"
                response = str(e)
                logger.error(f"Error sending emails: {response}")

            # Сохраняем результат попытки
            TryMailing.objects.create(mailing=mailing, status=status, response=response)

            # Обновляем статус рассылки, если это была последняя отправка
            if status == "success":
                mailing.status = "completed"
                mailing.save()
    logger.info("Mailing process completed")
