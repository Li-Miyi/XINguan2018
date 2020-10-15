from django.shortcuts import render, redirect,reverse

# Create your views here.
from django.http import Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import jianyue
from ..models import yonghu,lifashi,lifadian
from django.db.utils import IntegrityError
from django.shortcuts import render,get_object_or_404

"""用户与理发师"""
def zhuce(request):
    if request.method == "POST":
        data_getter = request.POST
    elif request.method == "GET":
        data_getter = request.GET
    else:
        return JsonResponse({"success":0,"msg":"注册失败"})


    xingming = data_getter.get('xingming')
    mima = data_getter.get('mima')
    lianxifangshi = data_getter.get('lianxifangshi')
    xingbie = data_getter.get('xingbie')
    shenfen = data_getter.get('shenfen')
    yonghuming = data_getter.get('yonghuming')
    try:
        if shenfen == 'lifashi':
            lifashi.objects.create(xingming=xingming,yonghuming=yonghuming,  mima=mima, lianxidianhua=lianxifangshi,
                                  xingbie=xingbie)
        elif shenfen == 'yonghu':
            yonghu.objects.create( xingming=xingming, yonghuming=yonghuming,mima=mima, lianxidianhua=lianxifangshi,
                                  xingbie=xingbie)
        else:
            return JsonResponse({"success":0,"msg":"身份错误"})
        return JsonResponse({"status":1,"msg":"注册成功"})
    except IntegrityError:
        return JsonResponse({"success":0,"msg":"手机号码已注册："+lianxifangshi})

def denglu(request):
    if request.method =="POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    lianxifangshi = datagetter.get("lianxifangshi")
    mima = datagetter.get("mima")
    shenfen = datagetter.get("shenfen")
    if shenfen == "lifashi":
        the_shenfen = lifashi
    elif shenfen == "yonghu":
        the_shenfen = yonghu
    else:
        return JsonResponse({'status':3,'msg':"身份错误"})
    try:
        this = the_shenfen.objects.get(lianxidianhua=lianxifangshi)
    except yonghu.DoesNotExist:
        return JsonResponse({'status':0,'msg':"此用户不存在"})
    except lifashi.DoesNotExist:
        return JsonResponse({'status':0,'msg':"此用户不存在"})
    if this.mima != mima:
        return JsonResponse({'status':1,'msg':"密码错误"})
    else:
        return JsonResponse({'status':2,'msg':'登录成功'})


def xiugai(request):
    if request.method == "POST":
        data_getter = request.POST
    elif request.method == "GET":
        data_getter = request.GET
    else:
        return JsonResponse({"success":0,"msg":"访问方法错误"})
    ziduan = data_getter.get("ziduan")
    lianxifangshi = data_getter.get("lianxifangshi")
    neirong = data_getter.get("neirong")
    the_yonghu = yonghu.objects.filter(lianxidianhua=lianxifangshi)
    data = {ziduan:neirong}
    try:
        the_yonghu.update(**data)
    except TypeError:
        return JsonResponse({"status":0,"msg":"字段错误"})
    except IntegrityError:
        return JsonResponse({"status": 2, "msg": "字段内容已被注册"})
    return JsonResponse({"status":1,"msg":"修改成功"})
