from django.core.management.base import BaseCommand
from deductions.models import DeductionType

class Command(BaseCommand):
    help = "Seed deduction types"

    def handle(self, *args, **options):
        data = [
            ("FALL", "Fall", 1.0),
            ("DANGEROUS_MOVE", "Dangerous Move", 2.0),
            ("ILLEGAL_SKILL", "Illegal Skill", 2.0),
            ("SAFETY", "Safety Violation", 2.0),
            ("TIME", "Time Violation", 2.0),
            ("KICK", "Kick Count Violation", 1.0),
            ("COMPETITOR", "Competitor Count Violation", 2.0),
            ("OTHER", "Other", 0.0),
        ]

        for code, label, points in data:
            DeductionType.objects.update_or_create(
                code=code,
                defaults={"label": label, "points": points},
            )

        self.stdout.write(self.style.SUCCESS("Deduction types seeded."))
