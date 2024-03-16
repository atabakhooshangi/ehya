from django.core.management.base import BaseCommand, CommandError
import os
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

FIXTURES = BASE_DIR / 'fixtures'

class Command(BaseCommand):
    help = 'تزریق دیتا به دیتابیس'

    def handle(self, *args, **options):
        os.system("python manage.py migrate --traceback")

        if FIXTURES.exists():
            all_fixture = [x for x in FIXTURES.iterdir()]
            all_fixture.sort()
            for fixture in all_fixture:
                print("---------------")
                load = Path(fixture)
                os.system(f"python manage.py loaddata {load}")