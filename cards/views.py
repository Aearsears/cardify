from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.cache import caches
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .translator import get_questions
import json
import re

# Create your views here.

cache = caches['default']


def index(request):
    return HttpResponse("<p>Qa are you doing here?</p>")


def qa(request):
    if request.method == 'POST':
        text = json.loads(request.body)
        get_questions(text)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)


def qareceive(request):
    # if request.method != 'POST' or request.method != 'GET':
    #     return HttpResponse(status=404)
    # else:
    if request.method == 'POST':
        # put into redis cache and issue a message to the MQ.
        # the body will be an array of dict {question:str, answer:str}
        # need to parse the question of what is the id? Then, put into cache: id:Qand A
        # Then, when issuing a message to the MQ, issue the id
        text = json.loads(request.body)
        print("Here is response qareceive :"+text)
        print("here is its type :" + type(text))
        reqID, qa = find_id(text)
        cache.set(reqID, qa)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'cards',
            {'type': 'chat_message', 'message': reqID}
        )
        return HttpResponse(status=200)
    elif request.method == 'GET':
        params = request.GET
        qa = cache.get(params.get("id"), "None")
        return JsonResponse(qa, safe=False)
    else:
        return HttpResponse(status=404)


def find_id(qa):
    """takes in a list of dict {question:str,answer:str}, finds the dict that has the question of"what is the request id?", and returns a tuple (request id, modified dict without this request question) """
    p = re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$", re.IGNORECASE)
    for index, pair in enumerate(qa):
        if(p.match(pair["answer"])):
            reqID = pair["answer"]
            del qa[index]
    return (reqID, qa)
