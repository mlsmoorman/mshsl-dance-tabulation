from decimal import Decimal
from .models import JudgeScoreSheet, KCTEntry
from meets.models import Division

#####  CENTRAL SCORING SERVICE - ALL RULES IN ONE PLACE  #####

#####  KICK COUNT DEDUCTION  #####
KICK_MIN = 35
KICK_MAX = 55
MIN_TIME = 120  # 2:00
MAX_TIME = 150  # 2:30
    
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

#####  TIME DEDUCTION  #####

    @staticmethod
    def compute_time_deduction(team_entry):
        kct = (
            KCTEntry.objects.filter(team_entry-team_entry)
            .order_by("-id")
            .first()
        )

        if not kct:
            return Decimal("0.0")
        
        time = kct.routine_time_seconds
        
        # Under time
        if time < MIN_TIME:
            return Decimal("1.0")
        
        # Over time
        if time > MAX_TIME:
            return Decimal("1.0")
        return Decimal("0.0")

        # Otherwise no deduction
        return Decimal("0.0")
    
    @staticmethod
    def apply_to_scoresheet(scoresheet: JudgeScoreSheet):
        # Kick deduction from KCT
        scoresheet.kick_deduction = ScoringEngine.compute_kick_deduction(
            scoresheet.division,
            scoresheet.team_entry,
        )

        # Time deduction from KCT
        scoresheet.time_deduction = ScoringEngine.compute_time_deduction(
            scoresheet.team_entry
        )

        scoresheet.compute_total()

        