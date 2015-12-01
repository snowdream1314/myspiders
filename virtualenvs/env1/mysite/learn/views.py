# -*- coding: UTF-8 -*- 
#-------------------------------------
# Name: 
# Purpose: learn django
# Author:
# Date: 2015-11-19
#-------------------------------------

# from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext

from learn.models import smzdm_fx


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

def show(request):
    
    #使用paginator实现分页
    limit = 10  #限制每页显示的记录数
    items = smzdm_fx.objects(itemid__gt=705000).limit(30)
    paginator = Paginator(items, limit) #实例化一个分页对象
    page = request.GET.get('page')  #获取页码
    try:
        items = paginator.page(page)    #获取某页对应的记录
    except PageNotAnInteger :   #如果页码不是整数
        items = paginator.page(1)   #取第一页的数据
    except EmptyPage:   #如果页码太大， 没有相应记录
        items = paginator.page(paginator.num_pages) #取最后一页的记录
        
    after_range_num = 5     #页码范围
    before_range_num = 6   
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+before_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+before_range_num]  
#     num = items.count()
    return render_to_response('item.html', {'items':items, 'num':paginator.count, 'page_range':page_range}, context_instance=RequestContext(request))