from django.core.management.base import NoArgsCommand
from django.contrib.sites.models import get_current_site
from django.contrib.auth.models import User
import getpass


class Command(NoArgsCommand):
    help = 'Creates teacher account with Django staff permissions'

    def handle(self, **options):
        teacher = User(
            username=raw_input('Username: '),
            first_name=raw_input('First Name: '),
            last_name=raw_input('Last Name: '),
            is_staff=True
        )
        teacher.set_password(getpass.getpass())
        teacher.save()

        self.stdout.write('Successfully saved %r.' % teacher.get_full_name())
