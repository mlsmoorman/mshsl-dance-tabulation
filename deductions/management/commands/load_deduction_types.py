from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Load all MSHSL deduction types from fixture"

    def handle(self, *args, **kwargs):
        call_command("loaddata", "deduction_types.json")
        self.stdout.write(self.style.SUCCESS("Deduction types loaded successfully."))
