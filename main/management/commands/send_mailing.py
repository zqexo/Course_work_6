from django.core.management.base import BaseCommand
from main.tasks import send_mailing


class Command(BaseCommand):
    help = "Send mailings manually"

    def handle(self, *args, **kwargs):
        send_mailing()
        self.stdout.write(self.style.SUCCESS("Successfully sent mailings"))
