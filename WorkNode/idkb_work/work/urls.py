
from django.conf import settings
from django.conf.urls import static
from django.template.defaulttags import url
from django.urls import path,re_path
from . import views

urlpatterns=[
    path('file_get',views.file_get,name='file_get'),
    path('file_get_detail',views.file_get_detail,name='file_get_detail'),
    path('file_upload',views.file_upload,name='file_upload'),
    path('file_delete',views.file_delete,name='file_dlelete'),
    path('kb_get',views.kb_get,name='kb_get'),
    path('kb_get_detail',views.kb_get_detail,name='kb_get_detail'),
    path('kb_create',views.kb_create,name='kb_create'),
    path('kb_delete',views.kb_delete,name='kb_delete'),
    path('kb_add_files',views.kb_add_files,name='kb_add_files'),
    path('kb_drop_files',views.kb_drop_files,name='kb_drop_files'),
    path('kb_get_files',views.kb_get_files,name='kb_get_files'),
    path('kb_get_valid_files',views.kb_get_valid_files,name='kb_get_valid_files'),
    # path('search_knowledges',views.search_knowledges,name='search_knowledges'),
    path('chat',views.chat,name='chat'),
    path('module_control',views.module_control,name='module_control'),
]


