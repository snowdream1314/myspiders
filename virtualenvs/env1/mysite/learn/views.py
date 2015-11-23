# -*- coding: UTF-8 -*- 
#-------------------------------------
# Name: 
# Purpose: learn django
# Author:
# Date: 2015-11-19
#-------------------------------------

# from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
# def index(request):
#     return HttpResponse(u'你好，世界')
# 
# 
# def add(request):
#     a = request.GET['a']
#     b = request.GET['b']
#     c = int(a) + int(b)
#     return HttpResponse(str(c))
# 
# def add2(request,a,b):
#     c = int(a) + int(b)
#     return HttpResponse("<a href="/add/4/5/">link</a>")

def home(request):
    return render(request, 'home.html')
