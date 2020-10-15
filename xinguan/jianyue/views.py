from django.shortcuts import render, redirect,reverse

# Create your views here.
from django.http import Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import jianyue
from .models import yonghu,lifashi,lifadian
from django.db.utils import IntegrityError
from django.shortcuts import render,get_object_or_404
#http://127.0.0.1/jianyue/zhuce?shenfen=lifashi/yonghuming=wqe&xingming=qwe&mima=qq&mima2=qq&lianxifangshi=qwewqe&xingbie=1
#http://121.196.213.151/jianyue/zhuce/?shenfen=lifashi&lianxifangshi=84848484&xingming=%E6%9D%8E%E5%9B%9B&yonghuming=%E6%9D%A5%E4%B8%8A%E7%BD%91%E7%9A%84&xingbie=1&mima=111qqq%2F%2F%2F

def index(request):   #没用的首页
    return render(request, 'index.html')

def app_index(request):#没用的首页
    return render(request,'jianyue/index.html')


