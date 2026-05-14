from django.shortcuts import render, redirect
from meets.models.meet import Meet
from meets.forms import MeetForm

def meet_setup(request):
    meets = Meet.objects.all().order_by("-date")

    if request.method == "POST":
        form = MeetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("meet_setup")
    else:
        form = MeetForm()

    return render(request, "meets/meet_setup.html", {
        "form": form,
        "meets": meets,
    })

