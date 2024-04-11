
from django.conf import settings
from django.conf.urls import static
from django.template.defaulttags import url
from django.urls import path,re_path
from . import views

urlpatterns=[
    path('',views.server_home,name='main'),
    path('kb',views.server_kb,name='kb'),
    path('file',views.server_file,name='file'),
    path('chat',views.server_chat,name='chat'),
]


