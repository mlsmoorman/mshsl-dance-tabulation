import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from core.models import (
    School,
    Team,
    TeamLevel,
    Role,
    User,
)

from meets.models import (
    Meet,
    TeamEntry,
    Division,
    ClassLevel,
)

from judging.models import JudgeScoreSheet


PASSWORD = "demo1234"


# ---------------------------------------------------------
# Wipe all data
# ---------------------------------------------------------
def wipe_all():
    print("Wiping all data...")

    JudgeScoreSheet.objects.all().delete()
    TeamEntry.objects.all().delete()
    Meet.objects.all().delete()
    Team.objects.all().delete()
    School.objects.all().delete()
    User.objects.all().delete()
    Role.objects.all().delete()

    print("✓ All data wiped.")


# ---------------------------------------------------------
# Seed roles
# ---------------------------------------------------------
def seed_roles():
    print("Seeding base roles...")

    roles = [
        ("JUDGE", "Judge"),
        ("KCT", "KCT Operator"),
        ("TABULATOR", "Tabulator"),
        ("SUPERIOR", "Superior Judge"),
    ]

    for code, name in roles:
        Role.objects.get_or_create(code=code, defaults={"name": name})

    print("✓ Roles seeded.")


# ---------------------------------------------------------
# Seed schools
# ---------------------------------------------------------
def seed_schools():
    print("Creating schools...")

    names = [
        "Wayzata High School",
        "Maple Grove High School",
        "Edina High School",
        "Minnetonka High School",
        "Prior Lake High School",
        "Lakeville North High School",
        "Lakeville South High School",
        "Eden Prairie High School",
        "Blaine High School",
        "Rogers High School",
        "Chaska High School",
        "Chanhassen High School",
    ]

    schools = []
    for name in names:
        school, _ = School.objects.get_or_create(name=name)
        schools.append(school)

    print(f"✓ Created {len(schools)} schools.")
    return schools


# ---------------------------------------------------------
# Seed teams
# ---------------------------------------------------------
def seed_teams(schools, num_teams=12):
    print("Creating teams...")

    levels = [TeamLevel.VARSITY, TeamLevel.JV, TeamLevel.BSQUAD]
    teams = []

    for i in range(num_teams):
        school = random.choice(schools)
        level = random.choice(levels)

        team, _ = Team.objects.get_or_create(
            school=school,
            name="Dance Team",
            defaults={"level": level},
        )
        teams.append(team)

    print(f"✓ Created {len(teams)} teams.")
    return teams


# ---------------------------------------------------------
# Seed users
# ---------------------------------------------------------
def seed_users(num_judges=7, num_kcts=4, num_tabs=2, num_sup=2):
    print("Creating users...")

    judge_role = Role.objects.get(code="JUDGE")
    kct_role = Role.objects.get(code="KCT")
    tab_role = Role.objects.get(code="TABULATOR")
    sup_role = Role.objects.get(code="SUPERIOR")

    judges = []
    for i in range(1, num_judges + 1):
        user, _ = User.objects.get_or_create(
            username=f"judge{i}",
            defaults={"first_name": f"Judge {i}"},
        )
        user.set_password(PASSWORD)
        user.save()
        user.roles.add(judge_role)
        judges.append(user)

    kcts = []
    for i in range(1, num_kcts + 1):
        user, _ = User.objects.get_or_create(
            username=f"kct{i}",
            defaults={"first_name": f"KCT {i}"},
        )
        user.set_password(PASSWORD)
        user.save()
        user.roles.add(kct_role)
        kcts.append(user)

    tabs = []
    for i in range(1, num_tabs + 1):
        user, _ = User.objects.get_or_create(
            username=f"tab{i}",
            defaults={"first_name": f"Tabulator {i}"},
        )
        user.set_password(PASSWORD)
        user.save()
        user.roles.add(tab_role)
        tabs.append(user)

    sups = []
    for i in range(1, num_sup + 1):
        user, _ = User.objects.get_or_create(
            username=f"sup{i}",
            defaults={"first_name": f"Superior {i}"},
        )
        user.set_password(PASSWORD)
        user.save()
        user.roles.add(sup_role)
        sups.append(user)

    print("✓ Users created.")
    return judges, kcts, tabs, sups


# ---------------------------------------------------------
# Seed meets
# ---------------------------------------------------------
def seed_meets(num_meets, judges, kcts):
    print("Creating meets...")

    meets = []
    today = date.today()
    class_levels = [ClassLevel.A, ClassLevel.AA, ClassLevel.AAA, ClassLevel.CONF]

    for i in range(1, num_meets + 1):
        meet_date = today + timedelta(days=7 * i)

        meet, _ = Meet.objects.get_or_create(
            name=f"2026 Invitational #{i}",
            defaults={
                "date": meet_date,
                "site": f"High School Gym #{i}",
                "class_level": random.choice(class_levels),
                "num_finalists": 6,
            },
        )

        for j in judges:
            meet.judges.add(j)

        for k in random.sample(kcts, min(2, len(kcts))):
            meet.kcts.add(k)

        meets.append(meet)

    print(f"✓ Created {len(meets)} meets.")
    return meets


# ---------------------------------------------------------
# Seed team entries
# ---------------------------------------------------------
def seed_team_entries(meets, teams):
    print("Creating team entries...")

    divisions = [Division.JAZZ, Division.KICK]

    for meet in meets:
        order = 1
        for team in teams:
            for div in divisions:
                TeamEntry.objects.get_or_create(
                    meet=meet,
                    team=team,
                    division=div,
                    defaults={"performance_order": order},
                )
                order += 1

    print("✓ Team entries created.")


# ---------------------------------------------------------
# Seed judge score sheets
# ---------------------------------------------------------
def seed_scores(meets):
    print("Creating judge score sheets...")

    for meet in meets:
        entries = TeamEntry.objects.filter(meet=meet)
        judges = meet.judges.all()

        for entry in entries:
            for judge in judges:
                sheet, created = JudgeScoreSheet.objects.get_or_create(
                    judge=judge,
                    team_entry=entry,
                )

                if created:
                    # Shared categories
                    sheet.choreo_creativity = random.randint(7, 10)
                    sheet.choreo_visual_effect = random.randint(7, 10)
                    sheet.diff_routine = random.randint(7, 10)
                    sheet.diff_formations = random.randint(7, 10)
                    sheet.diff_skills_or_kicks = random.randint(7, 10)
                    sheet.exec_placement_control = random.randint(7, 10)
                    sheet.exec_accuracy = random.randint(7, 10)
                    sheet.routine_effectiveness = random.randint(7, 10)

                    # Division-specific
                    if entry.division == Division.JAZZ:
                        sheet.skills_turns = random.randint(7, 10)
                        sheet.skills_leaps_jumps = random.randint(7, 10)
                    else:
                        sheet.kicks_technique = random.randint(7, 10)
                        sheet.kicks_height = random.randint(7, 10)

                    sheet.time_deduction = 0
                    sheet.kick_deduction = 0
                    sheet.other_deduction = 0

                    sheet.save()

    print("✓ Judge score sheets created.")


# ---------------------------------------------------------
# Command
# ---------------------------------------------------------
class Command(BaseCommand):
    help = "Load demo data for the dance scoring system"

    def add_arguments(self, parser):
        parser.add_argument("--wipe", action="store_true")
        parser.add_argument("--teams", type=int, default=12)
        parser.add_argument("--judges", type=int, default=7)
        parser.add_argument("--meets", type=int, default=6)
        parser.add_argument("--scores", action="store_true")

    def handle(self, *args, **options):
        if options["wipe"]:
            wipe_all()

        seed_roles()
        schools = seed_schools()
        teams = seed_teams(schools, num_teams=options["teams"])
        judges, kcts, tabs, sups = seed_users(num_judges=options["judges"])
        meets = seed_meets(options["meets"], judges, kcts)
        seed_team_entries(meets, teams)

        if options["scores"]:
            seed_scores(meets)

        self.stdout.write(self.style.SUCCESS("Demo data loaded successfully."))

