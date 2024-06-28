from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Request recieved in the app1 index view.")