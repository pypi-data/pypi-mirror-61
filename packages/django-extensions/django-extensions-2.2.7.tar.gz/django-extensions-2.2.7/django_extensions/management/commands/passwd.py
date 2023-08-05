# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import getpass
import warnings

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils.deprecation import RemovedInNextVersionWarning

from django_extensions.management.utils import signalcommand


class Command(BaseCommand):
    help = "Clone of the UNIX program `passwd`, for django.contrib.auth."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?', type=str)

    @signalcommand
    def handle(self, *args, **options):
        warn_msg = "`django_extensions.management.commands.passwd` is deprecated. You should use built-in `changepassword` django command instead"
        print(self.style.ERROR(warn_msg), file=sys.stderr)
        warnings.warn(warn_msg, RemovedInNextVersionWarning, stacklevel=2)

        username = options['username'] or getpass.getuser()

        User = get_user_model()
        try:
            u = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            raise CommandError("user %s does not exist" % username)

        print("Changing password for user: %s" % username)
        p1 = p2 = ""
        while "" in (p1, p2) or p1 != p2:
            p1 = getpass.getpass()
            p2 = getpass.getpass("Password (again): ")
            if p1 != p2:
                print("Passwords do not match, try again")
            elif "" in (p1, p2):
                raise CommandError("aborted")

        u.set_password(p1)
        u.save()

        return "Password changed successfully for user %s\n" % username
