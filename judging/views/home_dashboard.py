from django.shortcuts import render
from meets.models.meet import Meet

def judge_home(request):
    meets = Meet.objects.all().order_by("date")
    return render(request, "judging/home_dashboard.html", {"meets": meets})
