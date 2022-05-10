from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .translator import get_questions
import json

# Create your views here.


def index(request):
    return HttpResponse("<p>Hello</p>")


def qa(request):
    if request.method == 'POST':
        # put into redis cache and issue a message to the MQ.
        request.body
        return HttpResponse(status=200)
    else:
        return HttpResponse("<p>Qa are you doing here?</p>")
