from django.http import HttpResponse
from django.template import loader

def home(request):
    content={}
    template=loader.get_template('wmc/home.html')
    return HttpResponse(template.render(content,request))

def page404(request,e):
    content={}
    template=loader.get_template('wmc/404.html')
    return HttpResponse(template.render(content,request))

def page502(request):
    content={}
    template=loader.get_template('wmc/502.html')
    return HttpResponse(template.render(content,request))
def page403(request,e):
    content={}
    template=loader.get_template('wmc/403.html')
    return HttpResponse(template.render(content,request))















