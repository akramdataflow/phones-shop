import os

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import Currency

class Command(BaseCommand):
    help = 'Create sample data'

    def handle(self, *args, **options):
        call_command('migrate')
        if not Currency.objects.count():
            Currency.objects.bulk_create([
                Currency(name='United States Dollar', code='USD', code3='USD', symbol='$', order=1),
                Currency(name='Iraqi Dinar', code='IQD', code3='IQD', symbol='د.ع', order=2),
                Currency(name='Saudi Riyal', code='SAR', code3='SAR', symbol='ر.س', order=3),
            ])

            self.stdout.write(self.style.SUCCESS('Successfully created sample currencies'))

        if not User.objects.count():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')