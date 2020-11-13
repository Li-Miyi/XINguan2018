from django.shortcuts import render, redirect, reverse

# Create your views here.
from django.http import Http404
from django.http import JsonResponse
from django.utils import timezone
import os
from mysite.settings import MEDIA_ROOT
from ..models import yonghu, lifashi, lifadian, wuzi as wz, jiesuandingdan, pingjia, yuyuedingdan, fuwu, jishiqitadizhi, \
    tupian,dizhi as dz
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
import requests
import json


"""理发店"""

def ger_address_info(address):
    req = requests.get("http://api.map.baidu.com/geocoding/v3/?address={}"
                       "&output=json&ak=ZtiExca5mcvFwBEfTL3B8eVg7ATjZb2f&callback=showLocation".format(address))
    dic = json.loads(req.text.replace("showLocation&&showLocation(", "").replace("(", "").replace(")", ""))
    return {"name":address,"lng":dic["result"]["location"]["lng"],"lat":dic["result"]["location"]["lat"],"comprehension":dic["result"]["comprehension"]}


def shouye(request):  # 理发师首页
    if request.method == "GET":
        return render(request, "jianyue/lifadian/index.html")


def zhuce(request):  # 注册验证
    ready = int(request.get_signed_cookie("denglu", 0, "xinguan"))
    if request.method == "GET":
        response = redirect(reverse("jianyue:lifadian_geren", kwargs={"dianzhulianxi": ready}))
        return response
    elif request.method == "POST":
        data_getter = request.POST
        dianzhuming = data_getter.get("dianzhuming")
        shenfenzheng = data_getter.get("shenfenzheng")
        dianzhulianxi = data_getter.get("dianzhulianxi")
        dianming = data_getter.get("dianming")
        dizhi = data_getter.get("dizhi")
        mima = data_getter.get("mima")
        try:
            this = lifadian.objects.create(dianzhuming=dianzhuming, shenfenzheng=shenfenzheng, dianzhulianxi=dianzhulianxi,
                                    dianming=dianming, dizhi=dizhi, mima=mima)
            dizhi.objects.create(lifadian=this,**ger_address_info(dizhi))
            request.session['dianzhulianxi'] = dianzhulianxi
            response = JsonResponse({"status": 1, "msg": "注册成功"})
            response.set_signed_cookie("denglu", dianzhulianxi, "xinguan")
            return response
        except IntegrityError:
            return JsonResponse({"status": 0, "msg": "手机号码或身份证已注册"})
        except:
            return JsonResponse({'status': -1, 'msg': '注册失败'})


def denglu(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    dianzhulianxi = datagetter.get("dianzhulianxi")
    mima = datagetter.get("mima")
    try:
        this = lifadian.objects.get(dianzhulianxi=dianzhulianxi)
    except lifadian.DoesNotExist:
        return JsonResponse({'status': 0, 'msg': "此用户不存在"})
    if this.mima != mima:
        return JsonResponse({'status': 1, 'msg': "密码错误"})
    else:
        request.session['dianzhulianxi'] = dianzhulianxi
        response = redirect(reverse("jianyue:lifadian_geren", kwargs={"dianzhulianxi": dianzhulianxi}))
        response.set_signed_cookie("denglu", value=dianzhulianxi, salt="xinguan")
        return response


def xiugai(request):
    dianzhulianxi = request.session['dianzhulianxi']
    ziduan = request.POST.get("ziduan")
    neirong = request.POST.get("neirong")

    the_lifadian = lifadian.objects.get(dianzhulianxi=dianzhulianxi)
    data = {ziduan: neirong}
    try:
        if ziduan == "dizhi":
            dz.objects.update_or_create(lifadian=the_lifadian,**ger_address_info(data[ziduan]))
        else:
            the_lifadian.update(**data)
    except TypeError:
        return JsonResponse({"status": 0, "msg": "字段错误"})
    except IntegrityError:
        return JsonResponse({"status": 2, "msg": "字段内容已被注册"})
    # except:
    #     return JsonResponse({"status": -1, "msg": "修改失败"})
    return JsonResponse({"status": 1, "msg": "修改成功"})


# 个人
def geren(request, dianzhulianxi):
    denglu = request.get_signed_cookie(key="denglu", default=0, salt="xinguan")
    this = lifadian.objects.get(dianzhulianxi=dianzhulianxi)
    try:
        dizhi = dz.objects.get(lifadian__dianzhulianxi=dianzhulianxi).name
    except:
        dizhi =""
    if int(denglu) == dianzhulianxi:
        response = render(request, "jianyue/lifadian/geren/index.html", {"context": this,"dizhi":dizhi})
        return response
    else:
        response = redirect("jianyue:lifadian_shouye")
        return response


def wuzi(request, dianzhulianxi):
    the_wuzis = wz.objects.filter(lifadian__dianzhulianxi=dianzhulianxi)
    return render(request, "jianyue/lifadian/geren/wuzi/index.html",
                  {"dianzhulianxi": dianzhulianxi, "data": the_wuzis})


def wuzi_zengjia(request, dianzhulianxi):
    if request.method == "GET":
        return render(request, "jianyue/lifadian/geren/wuzi/zengjia.html", {"dianzhulianxi": dianzhulianxi})
    else:
        data_getter = request.POST
        wuziming = data_getter.get('wuziming')
        wuzileixing = data_getter.get('wuzileixing')
        shengyuliang = data_getter.get('shengyuliang')
        jinhuoshijian = data_getter.get('jinhuoshijian')
        the_lifadian = lifadian.objects.get(dianzhulianxi=dianzhulianxi)
        try:
            wz.objects.create(lifadian=the_lifadian, wuziming=wuziming, wuzileixing=wuzileixing,
                              shengyuliang=shengyuliang,
                              jinhuoshijian=jinhuoshijian)
            return JsonResponse({"status": 1, "msg": "添加成功"})
        except IntegrityError:
            _wz = wz.objects.get(lifadian=the_lifadian, wuziming=wuziming, wuzileixing=wuzileixing)
            _wz.jinhuoshijian = jinhuoshijian
            _wz.shengyuliang = _wz.shengyuliang + int(shengyuliang)
            _wz.save()
            return JsonResponse({"status": 0, "msg": "更新成功"})
        except:
            return JsonResponse({"status": -1, "msg": wuziming})


def wuzi_shanchu(request, dianzhulianxi):
    wuziming = request.GET.get("wuziming", 0)
    wuzileixing = request.GET.get("wuzileixing", 0)
    this = wz.objects.get(lifadian__dianzhulianxi=dianzhulianxi, wuziming=wuziming, wuzileixing=wuzileixing)
    this.delete()
    return JsonResponse({"status": 1, "msg": "删除成功"})


def wuzi_xiaohao(request, dianzhulianxi):
    wuziming = request.GET.get("wuziming", 0)
    wuzileixing = request.GET.get("wuzileixing", 0)
    xiaohaoliang = request.GET.get("xiaohaoliang", 0)
    this = wz.objects.get(lifadian__dianzhulianxi=dianzhulianxi, wuziming=wuziming, wuzileixing=wuzileixing)

    this.shengyuliang = this.shengyuliang - int(xiaohaoliang)
    if this.shengyuliang < 0:
        return JsonResponse({"status": 2, "msg": "消耗过大"})
    elif this.shengyuliang == 0:
        this.delete()
        return JsonResponse({"status": 3, "msg": "已消耗完"})
    else:
        this.save()
        return JsonResponse({"status": 1, "msg": "消耗成功", "number": this.shengyuliang})


def jixiao(request, dianzhulianxi):
    result = []
    lifashis = lifashi.objects.filter(lifadian__dianzhulianxi=dianzhulianxi)
    for i in list(lifashis.all()):
        data = {'xingming': i.xingming}
        lifashi_dianhua = i.lianxidianhua
        dingdans = jiesuandingdan.objects.filter(lifashi__lianxidianhua=lifashi_dianhua)
        xiaofei = 0
        pingfen = 0
        pingfen_count = 0
        for j in list(dingdans.all()):
            xiaofei += j.shijifeiyong
            try:
                the_pingjias = pingjia.objects.filter(dingdan=j)
                for i_pingjia in the_pingjias:
                    pingfen += i_pingjia.pingfen
            except ObjectDoesNotExist:
                pingfen += 5
            pingfen_count += 1
        data['id'] = i.id
        data['xiaofei'] = xiaofei
        data['zongheping'] = pingfen / pingfen_count if pingfen_count != 0 else 0
        result.append(data)
    return render(request, "jianyue/lifadian/geren/lifashi/jixiao.html",
                  context={'data': result, 'dianzhulianxi': dianzhulianxi})


def anpai(request, dianzhulianxi):
    if request.method == "POST":
        datagetter = request.POST
        yonghu_id = datagetter.get("yonghu_id")
        lifashi_id = datagetter.get("lifashi_id")
        fuwu_id = datagetter.get("fuwu_id")
        yuyueriqi = datagetter.get("yuyueriqi")
        yuyueshijian = datagetter.get("yuyueshijian")
        yuyuexiaohao = datagetter.get("yuyuexiaohao")
        yuyuekaishi = yuyueriqi + ' ' + yuyueshijian
        try:
            theyonghu = yonghu.objects.get(id=yonghu_id)
        except ObjectDoesNotExist:
            return JsonResponse({"status": "0", "msg": "不存在这个用户"})
        try:
            the_fuwu = fuwu.objects.get(id=fuwu_id)
        except ObjectDoesNotExist:
            return JsonResponse({"status": "0", "msg": "不存在这个服务"})
        if the_fuwu.lifashi_id != int(lifashi_id):
            return JsonResponse({"status": "-1", "msg": "服务与理发师不对应"})
        try:
            yuyuedingdan.objects.create(lifashi_id=lifashi_id,
                                        lifadian=lifadian.objects.get(dianzhulianxi=dianzhulianxi), yonghu=theyonghu,
                                        fuwuxiang_id=fuwu_id, yuyuekaishi=yuyuekaishi,
                                        yuyuexiaohao=yuyuexiaohao,yijieshou=0)
            return JsonResponse({"status": "1", "msg": "订单安排成功"})
        except IntegrityError:
            return JsonResponse({"status": "-2", "msg": "订单不可以重复安排"})
    if request.method == "GET":
        lifashis = lifashi.objects.filter(lifadian__dianzhulianxi=dianzhulianxi)
        result = []
        for i in lifashis:
            kongxian = True
            info = {"id": i.id, "xingming": i.xingming}
            try:
                the_latest_dingdan = yuyuedingdan.objects.filter(lifashi=i, yuyuekaishi__lt=timezone.now()).latest(
                    "yuyuekaishi")
                deadline = the_latest_dingdan.yuyuekaishi + timezone.timedelta(
                    hours=the_latest_dingdan.yuyuexiaohao.hour,
                    minutes=the_latest_dingdan.yuyuexiaohao.minute,
                    seconds=the_latest_dingdan.yuyuexiaohao.second)
                if deadline > timezone.now() > the_latest_dingdan.yuyuekaishi:
                    info["zhuangtai"] = "有客"
                    info["shijian"] = deadline
                    kongxian = False
            except:
                pass
            if kongxian:
                info["zhuangtai"] = "空闲"
                info["shijian"] = ""
            try:
                the_earliest_dingdan = \
                    yuyuedingdan.objects.filter(lifashi=i, yuyuekaishi__gt=timezone.now()).order_by('yuyuekaishi')[
                        0]
                if kongxian:
                    info["shijian"] = the_earliest_dingdan.yuyuekaishi
            except IndexError:
                pass
            result.append(info)
        return render(request, "jianyue/lifadian/geren/lifashi/anpai.html",
                      context={"data": result, "dianzhulianxi": dianzhulianxi})


def dizhi(request, dianzhulianxi, zhuangtai):
    data = []
    if zhuangtai == "yipizhun":
        zhuangtai_ = '1'
        template = "jianyue/lifadian/geren/dizhi/index.html"
    elif zhuangtai == "weipizhun":
        zhuangtai_ = '0'
        template = "jianyue/lifadian/geren/dizhi/weipizhun.html"
    else:
        return Http404("请不要乱输入网址")
    for i_dizhi in jishiqitadizhi.objects.filter(lifadian__dianzhulianxi=dianzhulianxi, zhuangtai=zhuangtai_):
        the_lifashi = i_dizhi.lifashi
        info = {'id': the_lifashi.id, 'xingming': the_lifashi.xingming, "lifadian": the_lifashi.lifadian.id,
                "shenqingshijian": i_dizhi.shenqingshijian}
        data.append(info)
    return render(request, template_name=template, context={"data": data, 'dianzhulianxi': dianzhulianxi})


def dizhi_chexiao(request, dianzhulianxi):
    lifashi_id = request.GET.get('lifashi_id')

    jishiqitadizhi.objects.filter(lifashi_id=lifashi_id, lifadian__dianzhulianxi=dianzhulianxi).delete()
    return JsonResponse({"status": "1", "msg": "撤销成功"})


def dizhi_fankui(request, dianzhulianxi):
    lifashi_id = request.GET.get('lifashi_id')
    fankui = request.GET.get('fankui')
    if fankui == "jieshou":
        jishiqitadizhi.objects.filter(lifashi_id=lifashi_id, lifadian__dianzhulianxi=dianzhulianxi).update(
            zhuangtai="1")
    elif fankui == "jujue":
        jishiqitadizhi.objects.filter(lifashi_id=lifashi_id, lifadian__dianzhulianxi=dianzhulianxi).delete()
    else:
        return JsonResponse({'status': 0, "msg": "操作失败"})
    return JsonResponse({'status': 1, "msg": "操作成功"})


def xiangce(request, dianzhulianxi):
    lifadian_id = lifadian.objects.get(dianzhulianxi=dianzhulianxi).id

    if request.method == "POST":
        shanchu = request.POST.get("shanchu")
        if shanchu == '1':
            file_name = request.POST.get("filename")
            tupian.objects.get(tupianlaiyuan_id=lifadian_id ,src=file_name, tupianleixing='0').delete()
            file_full_path = os.path.join(MEDIA_ROOT, file_name)
            os.remove(file_full_path)
            return JsonResponse({"status":"2","msg":"删除成功"})
        else:
            src = request.FILES.get("src")
            the_tupian = tupian.objects.create(tupianlaiyuan_id=lifadian_id, src=src,tupianleixing='0')
            return JsonResponse({"status":"1","msg":the_tupian.src.name})
    else:
        the_tupians = tupian.objects.filter(tupianlaiyuan_id=lifadian_id, tupianleixing='0')
        return render(request, 'jianyue/lifadian/geren/xiangce/index.html',
                      context={"imgs": the_tupians, "dianzhulianxi": dianzhulianxi})


def dingdan_getter(request,dianzhulianxi):
    data = yuyuedingdan.objects.filter(lifadian__dianzhulianxi=dianzhulianxi,yijieshou = 1)
    print(data[0].fuwuxiang.jiage)
    return render(request,"jianyue/lifadian/geren/lifashi/yuyuedingdan.html",context={"data":data,"dianzhulianxi":dianzhulianxi})


def fuwu_getter(request,dianzhulianxi):
    data = fuwu.objects.filter(lifashi__lifadian__dianzhulianxi=dianzhulianxi)
    return render(request,"jianyue/lifadian/geren/lifashi/fuwu.html",context={"data":data,"dianzhulianxi":dianzhulianxi})
