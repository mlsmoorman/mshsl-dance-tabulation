from django.shortcuts import render
from meets.models.meet import Meet

def tabulator_home(request):
    meets = Meet.objects.all().order_by("date")
    return render(request, "tabulation/home_dashboard.html", {"meets": meets})
