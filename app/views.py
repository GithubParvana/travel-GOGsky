import os
from . forms import LinkForm
from django.shortcuts import render, HttpResponse
from app.utils.parser import parser
from django.conf import settings


def index(request):
    form = LinkForm(request.POST)
    if request.method == 'POST':
        link = request.POST.get('link')
        data = parser(link)

        with open(f"{settings.BASE_DIR}/report.xlsx", "rb") as excel:
            data = excel.read()

            response = HttpResponse(data, content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="report.xlsx"'
            os.remove(f"{settings.BASE_DIR}/report.xlsx")
            return response

    context = {'form': form}
    return render(request, 'index.html', context)
