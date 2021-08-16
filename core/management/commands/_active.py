from argparse import ArgumentParser

from django.core.management.base import BaseCommand, CommandError
from core.models import User


class MyCommand(BaseCommand):

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('phone_number',
                            metavar='PHONE_NUMBER',
                            help="phone number of the user",
                            )
