from __future__ import unicode_literals

import sys

from django.contrib.auth.models import User
from django.core.management import execute_from_command_line
from django.core.management.base import BaseCommand
from djblets.extensions.models import RegisteredExtension


class Command(BaseCommand):
    help = 'Dumps the contents of the demo server for use in resets.'

    EXCLUDE_APPS = [
        'accounts.reviewrequestvisit',
        'admin.logentry',
        'auth.permission',
        'contenttypes',
        'django_evolution',
        'sessions',
        'djblets_siteconfig',
    ]

    ALLOWED_EXTENSIONS = [
        'rbdemo.extension.DemoExtension',
        'rbmotd.extension.MotdExtension',
        'rbpowerpack.extension.PowerPackExtension',
    ]

    def handle(self, **options):
        # Clean up anything in the database that we don't want.
        User.objects.filter(username__startswith='guest').delete()
        RegisteredExtension.objects.exclude(
            class_name__in=self.ALLOWED_EXTENSIONS).delete()

        # Dump the database.
        cmd = [sys.argv[0], 'dumpdata', '--indent=2']

        for app in self.EXCLUDE_APPS:
            cmd += ['-e', app]

        execute_from_command_line(cmd)
