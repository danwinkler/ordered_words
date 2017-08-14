from django.core.management.base import BaseCommand

from learn.language import update_data

class Command(BaseCommand):
    help = 'Updates database with hardcoded values'

    def handle( self, *args, **options ):
        update_data()
