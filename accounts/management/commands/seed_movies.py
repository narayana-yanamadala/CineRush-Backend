from django.core.management.base import BaseCommand
from django.core.management import call_command
from accounts.models import Movie


class Command(BaseCommand):
    help = "Load movies if database is empty"

    def handle(self, *args, **kwargs):
        if Movie.objects.count() == 0:
            call_command("loaddata", "movies.json")
            self.stdout.write(
                self.style.SUCCESS("Movies loaded successfully")
            )
        else:
            self.stdout.write("Movies already exist")