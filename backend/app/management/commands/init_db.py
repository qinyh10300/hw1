from django.core.management.base import BaseCommand

from user.controllers import create_user
from utils.jwt import encrypt_password


class Command(BaseCommand):
    help = "Initialize Database with test data"

    def handle(self, *args, **options):
        # Initalize the database
        create_user(
            username="test_thss",
            password=encrypt_password(str("test_thss")),
            nickname="test_thss",
            url="https://baidu.com",
            mobile="+86.123456789012",
            magic_number=0,
        )
