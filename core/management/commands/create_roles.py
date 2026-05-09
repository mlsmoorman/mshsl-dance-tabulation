from django.core.management.base import BaseCommand
from core.models import Role

class Command(BaseCommand):
    help = "Create default system roles"

    def handle(self, *args, **kwargs):
        roles = ["Judge", "KCT", "Tabulator"]
        for r in roles:
            Role.objects.get_or_create(name=r)
        self.stdout.write(self.style.SUCCESS("Roles created successfully."))
