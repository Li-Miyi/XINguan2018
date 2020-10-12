from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import yonghu,lifashi
from django.db.utils import IntegrityError
#http://127.0.0.1:8000/jianyue/zhuce?yonghuming=wqe&xingming=qwe&mima=qq&mima2=qq&lianxifangshi=qwewqe&xingbie=1
#http://121.196.213.151:8000/jianyue/zhuce/?shenfeng=lifashi&lianxifangshi=84848484&xingming=%E6%9D%8E%E5%9B%9B&yonghuming=%E6%9D%A5%E4%B8%8A%E7%BD%91%E7%9A%84&xingbie=1&mima=111qqq%2F%2F%2F
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
        return JsonResponse({"success":0,"msg":"手机号码已注册"})

