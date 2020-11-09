import os

from django.shortcuts import render, redirect,reverse

# Create your views here.
from django.http import Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import jianyue
from mysite.settings import MEDIA_ROOT
from .models import yonghu,lifashi,lifadian,tupian as tp
from django.db.utils import IntegrityError
from django.shortcuts import render,get_object_or_404
def index(request):   #没用的首页
    return render(request, 'index.html')

def app_index(request):#没用的首页
    return render(request,'jianyue/index.html')

def tupian_add(request,tupianleixing,tupianlaiyuan_id):
    src = request.FILES.get("src")
    the_tupian = tp.objects.create(tupianlaiyuan_id=tupianlaiyuan_id, src=src, tupianleixing=tupianleixing)
    return JsonResponse({"status":"1","msg":the_tupian.src.name})

def tupian_show(request,tupianlaiyuan_id,tupianleixing):
    the_tupians = tp.objects.filter(tupianlaiyuan_id=tupianlaiyuan_id, tupianleixing=tupianleixing)
    data =[]
    for tupian in the_tupians:
        info = {"tupianlaiyuan_id":tupian.tupianlaiyuan_id,"src":tupian.src.name}
        data.append(info)
    return JsonResponse({"status":"1","data":data})

def tupian_delete(request,tupianlujing):
    try:
        tp.objects.get(src=tupianlujing).delete()
        file_full_path = os.path.join(MEDIA_ROOT, tupianlujing)
        os.remove(file_full_path)
        return JsonResponse({"status":"1","msg":"删除成功"})
    except ObjectDoesNotExist:
        return JsonResponse({"status":"0","msg":"删除失败"})
