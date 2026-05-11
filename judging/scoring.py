from decimal import Decimal
from .models import JudgeScoreSheet
from kct.models import KCTEntry
from meets.models import Division
from deductions.models import RoutineDeduction, DeductionType

#####  CENTRAL SCORING SERVICE - ALL RULES IN ONE PLACE  #####

#####  KICK COUNT DEDUCTION  #####
KICK_MIN = 35
KICK_MAX = 55
MIN_TIME = 120  # 2:00
MAX_TIME = 150  # 2:30
    
class ScoringEngine:
    
    #####  KICK DEDUCTION  #####
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

    #####  KICK DEDUCTION - APPLY DEDUCTION  #####
    @staticmethod    
    def apply_kick_deduction(scoresheet, user):
        #only applies to High Kick
        if scoresheet.division != Division.KICK:
            RoutineDeduction.objects.filter(
                team_entry=scoresheet.team_entry,
                deduction_type__code="KICK REQUIREMENTS"
            ).delete()
            return
        kct = KCTEntry.objects.filter(team_entry=scoresheet.team_entry).order_by("-id").first()
        if not kct or kct.kick_count is None:
            return
        
        # Compute how many kicks off
        if kct.kick_count < KICK_MIN:
            diff = KICK_MIN - kct.kick_count
        elif kct.kick_count > KICK_MAX:
            diff = kct.kick_count - KICK_MAX
        else: 
            # No violation -> remove any existing deduction
            RoutineDeduction.objects.filter(
                team_entry=scoresheet.team_entry,
                deduction_type__code="KICK REQUIREMENTS"
            ).delete()
            
        # Cap at 10 points
        points = min(diff, 10)
        
        rule = DeductionType.objects.get(code="KICK REQUIREMENTS")
        
        RoutineDeduction.objects.update_or_create(
            team_entry=scoresheet.team_entry,
            deduction_type=rule,
            default={
                "entered_by": user,
                "count": diff,
                "judges_reporting": 1,
                "minor": False,
                "flagrant": False,
                "notes": f"{diff} kicks outside allowed range"
            }
        )
    
    #####  TIME DEDUCTION - COMPUTES # SECONDS OFF  #####
    @staticmethod
    def get_seconds_off(scoresheet):
        kct = scoresheet.team_entry.kctentry_set.order_by("-id").first()
        if not kct:
            return 0
        
        actual = kct.routine_time_seconds
        
        if scoresheet.division == "JAZZ":
            min_time = 120    # 2:00
            max_time = 150    # 2:30
        else:
            min_time = 135    # 2:15
            max_time = 165    # 2:45
        
        if actual < min_time:
            return min_time - actual
        if actual > max_time:
            return actual - max_time
        
        return 0   
    
    #####  TIME DEDUCTION - CALCULATES THE PENALTY  ######
    @staticmethod
    def compute_time_deduction(seconds_off: int) -> Decimal:
        if seconds_off <= 0:
            return Decimal("0.0")
        if seconds_off <= 10:
            return Decimal("1.0")
        if seconds_off <= 20:
            return Decimal("2.0")
        if seconds_off <= 30:
            return Decimal("3.0")
        return Decimal("5.0")
    
    #####  TIME DEDUCTION - APPLIES THE DEDUCTION  #####
    @staticmethod
    def apply_time_deduction(scoresheet, user):
        seconds_off = ScoringEngine.get_seconds_off(scoresheet)
        points = ScoringEngine.compute_time_deduction(seconds_off)

        # No violation → remove any existing time deductions
        if points == 0:
            RoutineDeduction.objects.filter(
                team_entry=scoresheet.team_entry,
                deduction_type__code="TIME_REQUIREMENTS"
            ).delete()
            return

        rule = DeductionType.objects.get(code="TIME_REQUIREMENTS")

        RoutineDeduction.objects.update_or_create(
            team_entry=scoresheet.team_entry,
            deduction_type=rule,
            defaults={
                "entered_by": user,
                "count": 1,
                "judges_reporting": 1,
                "minor": False,
                "flagrant": False,
                "notes": f"{seconds_off} seconds outside allowed range",
            }
        )
        
    #####  COMPUTES TOTAL DEDUCTIONS  #####
    @staticmethod
    def compute_deductions_for_scoresheet(scoresheet):
        deductions = RoutineDeduction.objects.filter(team_entry=scoresheet.team_entry)

        total = Decimal("0.0")

        for d in deductions:
            rule = d.deduction_type

            if rule.penalty_type == "DQ":
                return "DQ"

            pts = d.compute_points_for_one_judge()

            if rule.per_judge:
                pts *= 1  # each judge applies individually

            total += pts

        return total
    
    #####  APPLIES DEDUCTIONS TO SCORESHEET  #####
    @staticmethod
    def apply_to_scoresheet(scoresheet: JudgeScoreSheet, user=None):
        # 1. Auto-apply time deduction (creates/updates RoutineDeduction)
        ScoringEngine.apply_time_deduction(scoresheet, user)

        # 2. Auto-apply kick deduction (creates/updates RoutineDeduction
        ScoringEngine.apply_kick_deduction(scoresheet, user)

        # 3. Compute Subtotal
        subtotal = scoresheet.compute_subtotal()
        
        # 4. Compute all deductions (including time + kick)
        deduction_total = ScoringEngine.compute_deductions_for_scoresheet(scoresheet)

        # 5. Handle DQ
        if deduction_total == "DQ":
            scoresheet.total_score = "DQ"
        else:
            scoresheet.total_score = subtotal - deduction_total

        scoresheet.save()

