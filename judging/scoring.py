from decimal import Decimal
from .models import JudgeScoreSheet, KCTEntry
from meets.models import Division

KICK_MIN = 35
KICK_MAX = 55

class ScoringEngine:
    @staticmethod
    def compute_kick_deduction(division, team_entry):
        if division != Division.KICK:
            return Decimal("0.0")

        kct = (
            KCTEntry.objects.filter(team_entry=team_entry)
            .order_by("-id")
            .first()
        )
        if not kct or kct.kick_count is None:
            return Decimal("0.0")

        if kct.kick_count < KICK_MIN:
            diff = KICK_MIN - kct.kick_count
        elif kct.kick_count > KICK_MAX:
            diff = kct.kick_count - KICK_MAX
        else:
            diff = 0

        return Decimal(diff)  # 1 point per kick outside range

    @staticmethod
    def compute_time_deduction(team_entry):
        # Placeholder: you can wire exact MSHSL timing rules here.
        # For now, no automatic time deduction.
        return Decimal("0.0")

    @staticmethod
    def apply_to_scoresheet(scoresheet: JudgeScoreSheet):
        # Kick deduction from KCT
        scoresheet.kick_deduction = ScoringEngine.compute_kick_deduction(
            scoresheet.division,
            scoresheet.team_entry,
        )

        # Time deduction (if you want it automatic)
        auto_time = ScoringEngine.compute_time_deduction(scoresheet.team_entry)
        # If you want KCT to enter time_deduction manually, skip this line:
        scoresheet.time_deduction = auto_time

        scoresheet.compute_total()

        