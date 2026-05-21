from django.shortcuts import render
from meets.models.meet import Meet

def kct_home(request):
    meets = Meet.objects.all().order_by("date")
    return render(request, "kct/home_dashboard.html", {"meets": meets})
