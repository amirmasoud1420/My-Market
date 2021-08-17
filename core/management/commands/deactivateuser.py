from ._active import *


class Command(MyCommand):
    def handle(self, *args, **options):
        phone = options['phone_number']
        try:
            user = User.objects.get(phone=phone)
            user.is_active = False
            user.save()
            print("user" + "(" + self.style.WARNING(phone) + ")" + self.style.SUCCESS("deactivated!!!"))
        except Exception as e:
            raise CommandError(e)

# from argparse import ArgumentParser
#
# from django.core.management.base import BaseCommand, CommandError
# from core.models import User

# class Command(BaseCommand):
#
#     def add_arguments(self, parser: ArgumentParser):
#         parser.add_argument('phone_number',
#                             metavar='PHONE_NUMBER',
#                             help="phone number of the user",
#                             )
#
#     def handle(self, *args, **options):
#         phone = options['phone_number']
#         try:
#             user = User.objects.get(phone=phone)
#             user.is_active = False
#             user.save()
#             print("user" + "(" + self.style.WARNING(phone) + ")" + self.style.SUCCESS("deactived!!!"))
#         except Exception as e:
#             raise CommandError(e)
