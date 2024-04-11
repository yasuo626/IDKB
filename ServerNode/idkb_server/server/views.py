import os
import pathlib

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.shortcuts import redirect

from wmc.models import User
from wmc.views import get_url
import datetime
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import JsonResponse

def server_home(request):

    content={}
    content['require_login']="1"
    if request.user.is_authenticated:
        content['is_login']=1
        content['username']=request.user.username
    else:
        content['is_login']="0"
        content['username']="unlogin"
    content['apiurl'] = get_url('idkb')
    template=loader.get_template('server/home.html')
    return HttpResponse(template.render(content,request))

def server_kb(request):
    content={}
    content['require_login']="1"
    if not request.user.is_authenticated:
        return redirect('../idkb/')
    template=loader.get_template('server/kb.html')
    content['username'] = request.user.username
    content['apiurl'] = get_url('idkb')
    return HttpResponse(template.render(content,request))

def server_file(request):
    content={}
    content['require_login']="1"
    if not request.user.is_authenticated:
        return redirect('../idkb/')
    template=loader.get_template('server/file.html')
    content['username'] = request.user.username
    content['apiurl'] = get_url('idkb')
    return HttpResponse(template.render(content,request))
def server_chat(request):
    content={}
    if not request.user.is_authenticated:
        return redirect('../idkb/')
    template=loader.get_template('server/chat.html')
    content['username'] = request.user.username
    content['apiurl'] = get_url('idkb')
    return HttpResponse(template.render(content,request))

