from django.core.management.base import NoArgsCommand
from django.contrib.sites.models import get_current_site
from allauth.socialaccount.models import SocialApp
import webbrowser


class Command(NoArgsCommand):
    help = 'Set up google login'

    def handle(self, **options):
        webbrowser.open_new_tab('https://console.developers.google.com')

        app, app_pre_exists = SocialApp.objects.get_or_create(id=1)

        app.provider = 'google'
        app.name = 'Grading'
        app.client_id = raw_input('Client ID: ')
        app.secret = raw_input('Secret Key: ')

        app.sites.clear()
        site = get_current_site(None)
        domain = raw_input('Domain: ')
        site.name = domain
        site.domain = domain
        site.save()
        app.sites.add(site)

        app.save()
        self.stdout.write('Successfully saved %r.' % app.name)
