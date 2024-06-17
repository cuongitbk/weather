#!/usr/bin/env python
import logging

from django.core.management.base import BaseCommand

from web.backends.parser import ForcastDataParser

logger = logging.getLogger('backend')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--lat', type=float)
        parser.add_argument('--long', type=float)

    def handle(self, *args, **options):
        logger.info(f'[+] Extracting location information', extra=dict(lat=options['lat'], long=options['long']))
        grid_point_parser = ForcastDataParser()
        grid_point_parser.parse(options['lat'], options['long'])
