import json
from django.core.management.base import BaseCommand
from club.models import Music
from drinker.utils import generate_hashid
from hashids import Hashids

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **kwargs):
        with open(kwargs['json_file']) as f:
            data_list = json.load(f)

        for data in data_list:
            Music.objects.get_or_create(genre=data)
            object = Music.objects.latest('id')
            object.slug = generate_hashid(pk=object.pk)
            object.save()