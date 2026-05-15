#from django.shortcuts import get_object_or_404
#from django.template.loader import render_to_string
#from django.http import HttpResponse
#from tabulation.models import FinalResult
#from meets.models.meet import Meet
#from weasyprint import HTML
#
#def public_results_pdf(request, meet_id):
#    meet = get_object_or_404(Meet, id=meet_id)
#    results = FinalResult.objects.filter(meet=meet).order_by("final_rank")
#
#    # Group by division
#    divisions = {}
#    for r in results:
#        div = r.entry.division
#        divisions.setdefault(div, []).append(r)
#
#    html_string = render_to_string("tabulation/public_results_pdf.html", {
#        "meet": meet,
#        "divisions": divisions,
#    })
#
#    pdf = HTML(string=html_string).write_pdf()
#
#    response = HttpResponse(pdf, content_type="application/pdf")
#    response["Content-Disposition"] = f"inline; filename={meet.name}_results.pdf"
#    return response


from django.http import HttpResponse

def public_results_pdf(request, meet_id):
    return HttpResponse("PDF export temporarily disabled.")
