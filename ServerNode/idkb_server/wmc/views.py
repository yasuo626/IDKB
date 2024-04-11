from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.shortcuts import redirect
import re
from .models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from idkb_server.settings import BASE_DIR


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    match = re.match(pattern, email)
    if match:
        return True
    else:
        return False
def is_valid_password(password):
    return True

def apiuser(request):
    if request.method == "GET":
        return redirect('../apidocs/')
    response={"state":0,"error_info":""}
    if request.method == "POST":
        method= request.POST.get('method')
        if method == "register":
            username=request.POST.get('username')
            password=request.POST.get('password')
            email=request.POST.get('email')
            if not is_valid_email(email):
                response["state"] = 1
                response["error_info"] = f"email format error"
                return JsonResponse(response)
            if User.objects.filter(username=username).exists():
                response["state"] = 1
                response["error_info"] = f"username exists"
                return JsonResponse(response)
            if not is_valid_password(password):
                response["state"] = 1
                response["error_info"] = f"password error"
                return JsonResponse(response)
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return JsonResponse(response)
        elif method =="logoff":
            try:
                username=request.POST.get('username')
                password=request.POST.get('password')
                email=request.POST.get('email')
                valid_code=request.POST.get('valid_code')
                user=User.objects.get(username=username, password=password, email=email)
                user.delete()
            except:
                user = None
            if user is None:
                response["state"] = 1
                response["error_info"] = f"account vaild error"
            return JsonResponse(response)
        elif method =="login":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is None:
                response["state"] = 1
                response["error_info"] = f"username or password error"
                return JsonResponse(response)
            login(request, user)
            return JsonResponse(response)
        elif method =="logout":
            logout(request)
            return JsonResponse(response)
        elif method =="reset":
            username = request.POST.get('username')
            new_password = request.POST.get('new_password')
            email = request.POST.get('email')
            valid_code = request.POST.get('valid_code')
            user = User.objects.get(username=username)
            if not is_valid_password(new_password):
                response["state"] = 1
                response["error_info"] = f"password error"
            if user is None:
                response["state"] = 1
                response["error_info"] = f"user not exists"
                return JsonResponse(response)
            user.password = make_password(new_password)
            user.save()
            return JsonResponse(response)
        else:
            response["state"] = 1
            response["error_info"] = f"unsupport method:{method}"

    response["state"] = 1
    response["error_info"] = f"request method {request.method}!=POST"
    return JsonResponse(response)

def get_url(module):
    with open(str(BASE_DIR/'wmc/url'/f'{module}.url'), mode='rt') as f:
        url=f.read()
    return url


def save_url(request):
    """
    """
    response={"state":0,"error_info":""}
    if request.method == "POST":
        module = request.POST.get('module')
        url = request.POST.get('url')
        with open(str(BASE_DIR/'wmc/url'/f'{module}.url'), mode='wt') as f:
            f.write(url)
        return JsonResponse(response)
    response["state"]=1
    response["error_info"]=f"request method {request.method}!=POST"
    return JsonResponse(response)

def get_module_url(request):
    if request.method == "GET":
        return redirect('../apidocs/')

    response={"state":0,"error_info":""}
    if request.method == "POST":
        module= request.POST.get('module')
        response['url']=get_url(module)
        return JsonResponse(response)
    else:
        response["state"]=1
        response["error_info"]=f"request method {request.method}!=POST"
    return JsonResponse(response)


def home(request):
    content={}
    content['require_login']="1"
    if request.user.is_authenticated and request.user.is_superuser:
        content['is_login']=1
        content['username']=request.user.username
    else:
        content['is_login']="0"
        content['username']="unlogin"
    template=loader.get_template('wmc/home.html')
    return HttpResponse(template.render(content,request))