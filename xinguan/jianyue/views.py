import os

from django.shortcuts import render, redirect,reverse

# Create your views here.
from django.http import Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import jianyue
from mysite.settings import MEDIA_ROOT
from django.views.decorators.csrf import csrf_exempt
from .models import yonghu,lifashi,lifadian,tupian as tp
from django.db.utils import IntegrityError
from django.shortcuts import render,get_object_or_404
def index(request):   #没用的首页
    return render(request, 'index.html')

def app_index(request):#没用的首页
    return render(request,'jianyue/index.html')

@csrf_exempt
def tupian_add(request,tupianleixing,tupianlaiyuan_id):
    if request.method == "POST":
        src = request.FILES.get("src")
        the_tupian = tp.objects.create(tupianlaiyuan_id=tupianlaiyuan_id, src=src, tupianleixing=tupianleixing)
        return JsonResponse({"status":"1","msg":the_tupian.src.name})

@csrf_exempt
def tupian_show(request,tupianlaiyuan_id,tupianleixing):
    try:
        the_tupians = tp.objects.filter(tupianlaiyuan_id=tupianlaiyuan_id, tupianleixing=tupianleixing)
        data =[]
        for tupian in the_tupians:
            if "http" in tupian.src.name:
                info = {"tupianlaiyuan_id":tupian.tupianlaiyuan_id,"src":tupian.src.name,'lujing':tupian.src.name}
            else:
                info = {"tupianlaiyuan_id":tupian.tupianlaiyuan_id,"src":'http://127.0.0.1:8000/media/'+tupian.src.name,'lujing': tupian.src.name}
            data.append(info)
        if len(data)==0:
            return JsonResponse({"status": 0})
        else:
            return JsonResponse({"status": "1", "data": data})
    except:
        return JsonResponse({"status": 0,"msg":str(Exception)})

@csrf_exempt
def tupian_delete(request,tupianlujing):
    try:
        tp.objects.get(src=tupianlujing).delete()
        file_full_path = os.path.join(MEDIA_ROOT, tupianlujing)
        file_full_path.replace('\\\\','/')
        os.remove(file_full_path)
        return JsonResponse({"status":"1","msg":"删除成功"})
    except ObjectDoesNotExist:
        return JsonResponse({"status":"0","msg":"删除失败"})

@csrf_exempt
def touxiang_update(request,tupianleixing,tupianlaiyuan_id,tupianlujing):
    if request.method == "POST":
        if('https' in tupianlujing ):
            try:
                #删除原图片
                tp.objects.get(tupianleixing=tupianleixing,tupianlaiyuan_id=tupianlaiyuan_id).delete()
                #创建新头像
                src = request.FILES.get("src")
                the_tupian = tp.objects.create(tupianlaiyuan_id=tupianlaiyuan_id, src=src, tupianleixing=tupianleixing)
                return JsonResponse({"status": "1", "msg": "更换头像成功"})
            except:
                return JsonResponse({"status": 0, "msg": str(Exception)})
        else:
            try:
                #删除原图片
                tp.objects.get(tupianleixing=tupianleixing,tupianlaiyuan_id=tupianlaiyuan_id).delete()
                file_full_path = os.path.join(MEDIA_ROOT, tupianlujing)
                file_full_path.replace('\\\\','/')
                print(file_full_path)
                os.remove(file_full_path)
                #创建新头像
                src = request.FILES.get("src")
                the_tupian = tp.objects.create(tupianlaiyuan_id=tupianlaiyuan_id, src=src, tupianleixing=tupianleixing)
                new_tupian = tp.objects.get(tupianlaiyuan_id=tupianlaiyuan_id,tupianleixing=tupianleixing)
                return JsonResponse({"status": "1", "msg": "更换头像成功"})
            except:
                return JsonResponse({"status": 0,"msg": str(Exception)})
