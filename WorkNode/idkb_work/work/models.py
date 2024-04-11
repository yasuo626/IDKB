from django.db import models

# Create your models here.
import datetime

from django import forms
import pickle

class FileUploadForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))



class File(models.Model):
    name=models.CharField(max_length=200,primary_key=True)
    type=models.CharField(max_length=30)
    user_name=models.CharField(max_length=100)
    size=models.IntegerField()
    path=models.CharField(max_length=1000)
    api=models.CharField(max_length=100)
    embedding_model=models.CharField(max_length=100)
    embeddings_size=models.IntegerField()
    count=models.IntegerField()
    ctime=models.DateTimeField('ctime',auto_now_add=True)
    utime=models.DateTimeField('utime',auto_now=True)

class KnowledgeBase(models.Model):
    name=models.CharField(max_length=200,primary_key=True)
    user_name=models.CharField(max_length=100)
    api=models.CharField(max_length=100)
    embedding_model=models.CharField(max_length=100)
    llm=models.CharField(max_length=100)
    embeddings_size=models.IntegerField()
    reference=models.IntegerField()
    ctime=models.DateTimeField('ctime',auto_now_add=True)
    utime=models.DateTimeField('utime',auto_now=True)

# name,user_name,history,max_context,chat_template,question_template
class ChatModel(models.Model):
    name=models.CharField(max_length=200,primary_key=True)
    user_name=models.CharField(max_length=100)
    kb_name=models.CharField(max_length=200)
    history=models.BinaryField()
    max_context=models.IntegerField(default=1)
    system_template=models.CharField(max_length=1000)
    question_template=models.CharField(max_length=1000)
    ctime=models.DateTimeField('ctime',auto_now_add=True)
    utime=models.DateTimeField('utime',auto_now=True)

    @classmethod
    def bin2obj(self,bin):
        return pickle.loads(bin)
    @classmethod
    def obj2bin(self,obj):
        return pickle.dumps(obj)
    @classmethod
    def update(self,chat,msg):
        history=ChatModel.bin2obj(chat.history)
        history.append(msg)
        chat.history=ChatModel.obj2bin(history)
        chat.save()
    @classmethod
    def get_history(self,chat):
        return ChatModel.bin2obj(chat.history)



