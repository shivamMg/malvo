from django.core.management.base import BaseCommand

from teams.models import Team


class Command(BaseCommand):
    help = 'Create admin team'

    def add_arguments(self, parser):
        parser.add_argument('password', nargs=1, type=str)

    def handle(self, *args, **options):
        password = options['password'][0]
        team_name = 'admin'

        self.stdout.write(
            'Creating admin team `{}`...'.format(team_name), ending='')
        if Team.objects.filter(team_name=team_name).exists():
            self.stdout.write(
                self.style.NOTICE('`{}` already exists'.format(team_name)))
            return

        Team.objects.create_superuser(
            team_name=team_name, password=password, lang_pref='C')

        self.stdout.write(self.style.SUCCESS('DONE'))
