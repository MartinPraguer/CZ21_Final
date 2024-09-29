from django.shortcuts import render
from django.http import HttpResponse


def hello(request, s):
    return HttpResponse(f'AHOJ {s}')

# Create your views here.
def base(request):
    return render(
        request,
        "base.html",
        context={}
    )