from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse


import requests, json
import random
import time

def index(request):
    content={}
    template=loader.get_template('apidocs/index.html')
    return HttpResponse(template.render(content,request))
