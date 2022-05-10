from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.cache import caches
from .translator import get_questions
import json

# Create your views here.


def index(request):
    return HttpResponse("<p>Qa are you doing here?</p>")


def qa(request):
    if request.method == 'POST':
        # put into redis cache and issue a message to the MQ.
        text = json.loads(request.body)
        get_questions(text)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)


def qareceive(request):
    # if request.method != 'POST' or request.method != 'GET':
    #     return HttpResponse(status=404)
    # else:
    cache = caches['default']
    if request.method == 'POST':
        # put into redis cache and issue a message to the MQ.
        # the body will be an array of dict {question:str, answer:str}
        # need to parse the question of what is the id? Then, put into cache: id:Qand A
        # Then, when issuing a message to the MQ, issue the id
        text = json.loads(request.body)
        reqID, qa = find_id(text)
        cache.set(reqID, qa)
        return HttpResponse(status=200)
    elif request.method == 'GET':
        qa = cache.get("10023")
        return HttpResponse(qa, "None")


def find_id(qa):
    """takes in a list of dict {question:str,answer:str}, finds the dict that has the question of"what is the request id?", and returns a tuple (request id, modified dict without this request question) """
    for index, pair in enumerate(qa):
        if(pair["question"] == "What is the request id?"):
            reqID = pair["answer"]
            del qa[index]
    return (reqID, qa)
