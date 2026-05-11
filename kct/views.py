from django.shortcuts import render, get_object_or_404, redirect
from .models import KCTEntry
from django.contrib import messages
from judging.scoring import ScoringEngine
from meets.models import TeamEntry
from core.permissions import user_is_kct

#####  KCT VIEW  #####
def kct_entry(request, team_entry_id):
    if not user_is_kct(request.user):
        messages.error(request, "You do not have permission to access this page.")
        return redirect("/")
    
    team_entry = get_object_or_404(TeamEntry, id=team_entry_id)
    
    # Get or create the KCT entry
    kct, created = KCTEntry.objects.get_or_create(team_entry=team_entry)
    
    if request.method == "POST":
        kct.kick_count = request.POST.get("kick_count") or None
        kct.routine_time_seconds = request.POST.get("routine_time_seconds") or None
        kct.num_competitors = request.POST.get("num_competitors") or None
        kct.save()
        
        # Recompute auto deductions for all judge sheets
        for sheet in team_entry.judgescoresheet_set.all():
            ScoringEngine.apply_to_scoresheet(sheet, user=request.user)
            
        messages.success(request, "KCT data saved.")
        return redirect("kct_entry", team_entry_id=team_entry_id)
    
    return render(request, "kct/kct_entry.html", {
        "team_entry": team_entry,
        "kct": kct,
    })
