from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps
from core.models import Team, Role, User
from meets.models import Meet, TeamEntry
from judging.models import JudgeScoreSheet
from deductions.models import RoutineDeduction, DeductionType
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = "Loads demo data: teams (with levels), meets, entries, scores, KCT, deductions."
    
    TEAM_LEVELS = ["Varsity", "JV", "B-Squad"]

    def add_arguments(self, parser):
        parser.add_argument("--teams", type=int, default=7)
        parser.add_argument("--judges", type=int, default=5)
        parser.add_argument("--meets", type=int, default=3)
        parser.add_argument("--divisions", type=str, default="JAZZ,KICK")
        parser.add_argument("--finalists", type=int, default=6)
        parser.add_argument("--wipe", action="store_true")
        parser.add_argument("--scores", action="store_true")
        parser.add_argument("--kct", action="store_true")
        parser.add_argument("--deductions", action="store_true")

    def handle(self, *args, **options):
        num_teams = options["teams"]
        num_judges = options["judges"]
        num_meets = options["meets"]
        divisions = [d.strip().upper() for d in options["divisions"].split(",")]
        finalists = options["finalists"]
        wipe = options["wipe"]
        gen_scores = options["scores"]
        gen_kct = options["kct"]
        gen_deductions = options["deductions"]

        # Try to resolve KCTEntry dynamically
        KCTEntry = None
        try:
            KCTEntry = apps.get_model("judging", "KCTEntry")
        except LookupError:
            try:
                KCTEntry = apps.get_model("meets", "KCTEntry")
            except LookupError:
                KCTEntry = None

        # -----------------------------
        # WIPE DATABASE IF REQUESTED
        # -----------------------------
        if wipe:
            self.stdout.write("Wiping all data...")
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM deductions_routinededuction;")
                cursor.execute("DELETE FROM judging_judgescoresheet;")
                if KCTEntry:
                    cursor.execute(f"DELETE FROM {KCTEntry._meta.db_table};")
                cursor.execute("DELETE FROM meets_teamentry;")
                cursor.execute("DELETE FROM meets_meet;")
                cursor.execute("DELETE FROM core_team;")
                cursor.execute("DELETE FROM core_user_roles;")
                cursor.execute("DELETE FROM core_user;")
                cursor.execute("DELETE FROM core_role;")

        # -----------------------------
        # ROLES
        # -----------------------------
        self.stdout.write("Creating roles...")
        roles = ["Judge", "Superior Judge", "Tabulator", "KCT"]
        role_objs = {r: Role.objects.get_or_create(name=r)[0] for r in roles}

        # -----------------------------
        # USERS
        # -----------------------------
        self.stdout.write("Creating users...")

        def create_user(username, role_name):
            user, _ = User.objects.get_or_create(username=username)
            user.set_password("test1234")
            user.save()
            user.roles.add(role_objs[role_name])
            return user

        judges = [create_user(f"judge{i}", "Judge") for i in range(1, num_judges + 1)]
        superior = create_user("superior", "Superior Judge")
        tabulator = create_user("tabulator", "Tabulator")
        kct_user = create_user("kct", "KCT")

        # -----------------------------
        # TEAMS (School = Team.name)
        # -----------------------------
        self.stdout.write("Creating teams (school + level)...")

        base_team_names = [
            "Wayzata", "Eastview", "Maple Grove", "Chaska",
            "Edina", "Lakeville North", "Buffalo", "Minnetonka",
            "Prior Lake", "Eden Prairie", "Rogers", "Shakopee",
        ]

        teams = []
        for i in range(num_teams):
            team_name = base_team_names[i % len(base_team_names)]
            for level in self.TEAM_LEVELS:
                t, _ = Team.objects.get_or_create(name=team_name, level=level)
                teams.append(t)


        # -----------------------------
        # MEETS
        # -----------------------------
        self.stdout.write(f"Creating {num_meets} meets with random dates...")

        season_start = date(2026, 1, 1)
        season_end = date(2026, 3, 15)
        delta_days = (season_end - season_start).days

        for i in range(num_meets):
            meet_date = season_start + timedelta(days=random.randint(0, delta_days))
            meet, _ = Meet.objects.get_or_create(
                name=f"2026 Invitational #{i+1}",
                date=meet_date,
                num_finalists=finalists,
            )
            self.stdout.write(f"  → {meet.name} ({meet.date})")

            # Randomly assign judges to this meet
            meet_judges = random.sample(judges, k=min(len(judges), num_judges))

            # -----------------------------
            # TEAM ENTRIES + SCORES/KCT/DEDUCTIONS
            # -----------------------------
            for division in divisions:
                order = list(range(1, len(teams) + 1))
                random.shuffle(order)

                for team, perf_order in zip(teams, order):
                    entry, _ = TeamEntry.objects.get_or_create(
                        meet=meet,
                        team=team,
                        division=division,
                        performance_order=perf_order,
                    )

                    # KCT entry
                    if gen_kct and KCTEntry:
                        KCTEntry.objects.get_or_create(
                            team_entry=entry,
                            defaults={
                                "kct": kct_user,  # or assign a random KCT user if you prefer
                                "kick_count": random.randint(20, 60),
                                "routine_time_seconds": random.randint(90, 150),
                                "num_competitors": random.randint(10, 25),
                                "jazz_team_turn_performed": True,
                                "jazz_team_leap_jump_performed": True,
                                "falls_observed": False,
                                "dangerous_move_observed": False,
                            },
                        )

                    # Judge score sheets
                    if gen_scores:
                        for judge in meet_judges:
                            sheet, created = JudgeScoreSheet.objects.get_or_create(
                                team_entry=entry,
                                judge=judge,
                                defaults=self._random_scores_for_division(division),
                            )
                            if not created:
                                for field, value in self._random_scores_for_division(division).items():
                                    setattr(sheet, field, value)
                                sheet.save()

                    deduction_types = {dt.code: dt for dt in DeductionType.objects.all()}
                    deduction_codes = list(deduction_types.keys())
                    
                    # Routine-level deductions
                    if gen_deductions and random.random() < 0.2:
                        code = random.choice(deduction_codes)

                        RoutineDeduction.objects.create(
                            team_entry=entry,
                            deduction_type=deduction_types[code],
                            entered_by=random.choice(judges),   # or your Superior Judge user
                            count=1,
                            judges_reporting=1,
                            minor=False,
                            flagrant=False,
                            notes=f"Auto‑generated demo deduction ({code})",
                        )

        self.stdout.write(self.style.SUCCESS("✔ Demo data loaded successfully!"))
        self.stdout.write(self.style.SUCCESS(f"✔ {num_teams} schools * 3 levels = {len(teams)} teams"))
        self.stdout.write(self.style.SUCCESS(f"✔ {num_judges} judges"))
        self.stdout.write(self.style.SUCCESS(f"✔ {num_meets} meets"))
        self.stdout.write(self.style.SUCCESS(f"✔ Divisions: {', '.join(divisions)}"))
        if gen_scores:
            self.stdout.write(self.style.SUCCESS("✔ Random judge scores generated"))
        if gen_kct and KCTEntry:
            self.stdout.write(self.style.SUCCESS("✔ Random KCT entries generated"))
        if gen_deductions:
            self.stdout.write(self.style.SUCCESS("✔ Random routine deductions generated"))

    def _random_scores_for_division(self, division: str) -> dict:
        """
        Build a dict of field -> value for JudgeScoreSheet,
        including category scores and deductions.
        """
        data = {
            "choreo_creativity": random.randint(6, 10),
            "choreo_visual_effect": random.randint(6, 10),
            "diff_routine": random.randint(6, 10),
            "diff_formations": random.randint(6, 10),
            "diff_skills_or_kicks": random.randint(6, 10),
            "exec_placement_control": random.randint(6, 10),
            "exec_accuracy": random.randint(6, 10),
            "routine_effectiveness": random.randint(6, 10),
            "time_deduction": random.choice([0, 0, 0, 1, 2]),
            "kick_deduction": random.choice([0, 0, 0, 1, 2]),
            "other_deduction": random.choice([0, 0, 0, 1, 3]),
        }

        if division == "JAZZ":
            data["skills_turns"] = random.randint(6, 10)
            data["skills_leaps_jumps"] = random.randint(6, 10)
            data["kicks_technique"] = 0
            data["kicks_height"] = 0
        elif division == "KICK":
            data["skills_turns"] = 0
            data["skills_leaps_jumps"] = 0
            data["kicks_technique"] = random.randint(6, 10)
            data["kicks_height"] = random.randint(6, 10)
        else:
            data["skills_turns"] = 0
            data["skills_leaps_jumps"] = 0
            data["kicks_technique"] = 0
            data["kicks_height"] = 0

        return data
