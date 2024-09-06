from django.core.management.base import BaseCommand
from certifications.models import CertificationEvent
from django.utils import timezone
import csv

class Command(BaseCommand):
    help = 'Generate periodic certification reports'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        start_date = now - timezone.timedelta(days=30)
        events = CertificationEvent.objects.filter(timestamp__range=[start_date, now])

        report_file = f'reports/certification_report_{now.date()}.csv'
        with open(report_file, 'w', newline='') as csvfile:
            fieldnames = ['certification', 'user', 'event_type', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for event in events:
                writer.writerow({
                    'certification': event.certification.name,
                    'user': event.user.username,
                    'event_type': event.event_type,
                    'timestamp': event.timestamp,
                })

        self.stdout.write(self.style.SUCCESS(f'Report generated: {report_file}'))
