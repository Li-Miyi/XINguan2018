from django.shortcuts import render, redirect, reverse

# Create your views here.
from django.http import Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import jianyue
from ..models import yonghu, lifashi, lifadian, fuwu, jiesuandingdan, pingjia,dingdan
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404

"""用户与理发师"""


def zhuce(request):
    if request.method == "POST":
        data_getter = request.POST
    elif request.method == "GET":
        data_getter = request.GET
    else:
        return JsonResponse({"success": 0, "msg": "注册失败"})

    xingming = data_getter.get('xingming')
    mima = data_getter.get('mima')
    lianxifangshi = data_getter.get('lianxifangshi')
    xingbie = data_getter.get('xingbie')
    shenfen = data_getter.get('shenfen')
    yonghuming = data_getter.get('yonghuming')
    try:
        if shenfen == 'lifashi':
            lifashi.objects.create(xingming=xingming, yonghuming=yonghuming, mima=mima, lianxidianhua=lianxifangshi,
                                   xingbie=xingbie)
        elif shenfen == 'yonghu':
            yonghu.objects.create(xingming=xingming, yonghuming=yonghuming, mima=mima, lianxidianhua=lianxifangshi,
                                  xingbie=xingbie)
        else:
            return JsonResponse({"success": 0, "msg": "身份错误"})
        return JsonResponse({"status": 1, "msg": "注册成功"})
    except IntegrityError:
        return JsonResponse({"success": 0, "msg": "手机号码已注册：" + lianxifangshi})


def denglu(request):
    if request.method == "POST":
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
        return JsonResponse({'status': 3, 'msg': "身份错误"})
    try:
        this = the_shenfen.objects.get(lianxidianhua=lianxifangshi)
    except yonghu.DoesNotExist:
        return JsonResponse({'status': 0, 'msg': "此用户不存在"})
    except lifashi.DoesNotExist:
        return JsonResponse({'status': 0, 'msg': "此用户不存在"})
    if this.mima != mima:
        return JsonResponse({'status': 1, 'msg': "密码错误"})
    else:
        return JsonResponse({'status': 2, 'msg': '登录成功'})


def xiugai(request):
    if request.method == "POST":
        data_getter = request.POST
    elif request.method == "GET":
        data_getter = request.GET
    else:
        return JsonResponse({"success": 0, "msg": "访问方法错误"})
    ziduan = data_getter.get("ziduan")
    lianxifangshi = data_getter.get("lianxifangshi")
    neirong = data_getter.get("neirong")
    the_yonghu = yonghu.objects.filter(lianxidianhua=lianxifangshi)
    data = {ziduan: neirong}
    try:
        the_yonghu.update(**data)
    except TypeError:
        return JsonResponse({"status": 0, "msg": "字段错误"})
    except IntegrityError:
        return JsonResponse({"status": 2, "msg": "字段内容已被注册"})
    return JsonResponse({"status": 1, "msg": "修改成功"})


def liebiao(request):
    lifadian_datas = []
    lifashi_datas = []
    for i_lifadian in lifadian.objects.all():
        lifadian_data = {"name": i_lifadian.dianming, "id": i_lifadian.pk}
        i_lifadian_total_pingfen = 0
        i_lifadian_total_jiage = 0
        i_lifadian_count = 0
        for i_lifashi in lifashi.objects.filter(lifadian=i_lifadian):
            lifashi_data = {'id': i_lifashi.id, 'name': i_lifashi.xingming}
            i_lifashi_total_pingfen = 0
            i_lifashi_total_jiage = 0
            i_lifashi_count = 0
            for i_jiesuan in jiesuandingdan.objects.filter(lifashi=i_lifashi):
                i_lifashi_count += 1
                i_lifashi_total_jiage += i_jiesuan.shijifeiyong
                try:
                    for i_pingjia in pingjia.objects.filter(dingdan=i_jiesuan):
                        i_lifashi_total_pingfen += i_pingjia.pingfen

                except ObjectDoesNotExist:
                    i_lifashi_total_pingfen += 5
            try:
                lifashi_data["price"] = i_lifashi_total_jiage / i_lifashi_count
            except:
                lifashi_data["price"] = 0
            try:
                lifashi_data["pingfen"] = i_lifashi_total_pingfen / i_lifashi_count
            except:
                lifashi_data["pingfen"] = 5
            lifashi_datas.append(lifashi_data)
            i_lifadian_total_pingfen += i_lifashi_total_pingfen
            i_lifadian_total_jiage += i_lifashi_total_jiage
            i_lifadian_count = i_lifashi_count
        try:
            lifadian_data["pingfen"] = i_lifadian_total_pingfen / i_lifadian_count
        except:
            lifadian_data["pingfen"] = 5
        try:
            lifadian_data["price"] = i_lifadian_total_jiage / i_lifadian_count
        except:
            lifadian_data["price"] = 0
        lifadian_datas.append(lifadian_data)
    return JsonResponse({"lifashi": lifashi_datas, "lifadian": lifadian_datas})


def lifashi_detail(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    lifashi_id = int(datagetter.get('lifashi_id')[0])
    lifa_fuwu = []
    lifa_fuwu_detail = {}
    lifashi_lifadian = []
    lifashi_pingjia = []
    try:
        i_lifashi = lifashi.objects.get(id=lifashi_id)
    except lifashi.DoesNotExist:
        print(lifashi_id)
        print("m没有找到")
    for i_fuwu in fuwu.objects.filter(lifashi=i_lifashi):
        try:
            lifa_fuwu_detail = {"fuwu_id": i_fuwu.id, "type": i_fuwu.leixing, "fuwu_name": i_fuwu.fuwumingcheng, "price": i_fuwu.jiage}
        except ObjectDoesNotExist:
            print("这里错了")
        lifa_fuwu.append(lifa_fuwu_detail)
    for i_lifadian in lifadian.objects.filter(lifashi=i_lifashi):
        lifadian_detail = {"lifadian_id": i_lifadian.id, "lifadian_name": i_lifadian.dianming, "lifadian_dizhi": i_lifadian.dizhi}
        lifashi_lifadian.append(lifadian_detail)
    for i_dingdan in dingdan.objects.filter(lifashi_id=lifashi_id):
        for i_pingjia in pingjia.objects.filter(dingdan_id=i_dingdan.id):
            lifashi_pingjia_detail = {'id': i_pingjia.id, "pingfen": i_pingjia.pingfen, "pingjia": i_pingjia.pingjia}
            lifashi_pingjia.append(lifashi_pingjia_detail)
    return JsonResponse({"id": i_lifashi.id, "name": i_lifashi.xingming, 'phone': i_lifashi.lianxidianhua, "fuwu":lifa_fuwu, "lifadian":lifashi_lifadian, "pingjia":lifashi_pingjia})
