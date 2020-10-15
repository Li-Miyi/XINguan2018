from django.shortcuts import render, redirect,reverse

# Create your views here.
from django.http import Http404
from django.http import JsonResponse
import jianyue
from ..models import yonghu,lifashi,lifadian,wuzi as wz
from django.db.utils import IntegrityError
from django.shortcuts import render,get_object_or_404
import re

"""理发店"""
def shouye(request): #理发师首页
    if request.method == "GET":
        return render(request,"jianyue/lifadian/index.html")

def zhuce(request): #注册验证
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

            lifadian.objects.create(dianzhuming=dianzhuming ,shenfenzheng=shenfenzheng,dianzhulianxi=dianzhulianxi,
                                   dianming=dianming,dizhi=dizhi,mima=mima)
            request.session['dianzhulianxi'] = dianzhulianxi
            response = JsonResponse({"status": 1, "msg": "注册成功"})
            response.set_signed_cookie("denglu",dianzhulianxi,"xinguan")
            return response
        except IntegrityError:
            return JsonResponse({"status": 0, "msg": "手机号码或身份证已注册"})
        except:
            return JsonResponse({'status': -1, 'msg': '注册失败'})

def denglu(request):
    if request.method =="POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    dianzhulianxi = datagetter.get("dianzhulianxi")
    mima = datagetter.get("mima")
    try:
        this = lifadian.objects.get(dianzhulianxi=dianzhulianxi)

    except lifadian.DoesNotExist:
        return JsonResponse({'status':0,'msg':"此用户不存在"})
    if this.mima != mima:
        return JsonResponse({'status':1,'msg':"密码错误"})
    else:
        request.session['dianzhulianxi'] = dianzhulianxi
        response = redirect(reverse("jianyue:lifadian_geren",kwargs={"dianzhulianxi":dianzhulianxi}))
        response.set_signed_cookie("denglu",value=dianzhulianxi,salt="xinguan")
        return response

def xiugai(request):
    dianzhulianxi = request.session['dianzhulianxi']
    ziduan = request.POST.get("ziduan")
    neirong = request.POST.get("neirong")

    the_lifadian = lifadian.objects.filter(dianzhulianxi=dianzhulianxi)
    data = {ziduan:neirong}
    try:
        the_lifadian.update(**data)
    except TypeError:
        return JsonResponse({"status":0,"msg":"字段错误"})
    except IntegrityError:
        return JsonResponse({"status": 2, "msg": "字段内容已被注册"})
    except:
        return JsonResponse({"status":-1,"msg":"修改失败"})
    return JsonResponse({"status":1,"msg":"修改成功"})

#个人
def geren(request,dianzhulianxi):
    denglu = request.get_signed_cookie(key="denglu",default=0,salt="xinguan")
    this = lifadian.objects.get(dianzhulianxi=dianzhulianxi)
    context = {
        "shenfenzheng":this.shenfenzheng,
        "dianzhuming":this.dianzhuming,
        "dianzhulianxi":this.dianzhulianxi,
        "dianming":this.dianzhuming,
        "dizhi":this.dizhi,
        "mima":this.mima
    }
    if int(denglu) ==  dianzhulianxi:
        response = render(request,"jianyue/lifadian/geren/index.html",{"context":context})
        return response
    else:
        # response = JsonResponse({"fuck":str(dianzhulianxi)})
        response = redirect("jianyue:lifadian_shouye")
        return  response



def wuzi(request,dianzhulianxi):
    the_wuzis = wz.objects.filter(lifadian__dianzhulianxi=dianzhulianxi)
    return render(request,"jianyue/lifadian/geren/wuzi/index.html",{"dianzhulianxi":dianzhulianxi,"data":the_wuzis})

def wuzi_zengjia(request,dianzhulianxi):
    if request.method == "GET":
        return render(request,"jianyue/lifadian/geren/wuzi/zengjia.html",{"dianzhulianxi":dianzhulianxi})
    else:
        data_getter = request.POST
        wuziming = data_getter.get('wuziming')
        wuzileixing = data_getter.get('wuzileixing')
        shengyuliang = data_getter.get('shengyuliang')
        jinhuoshijian = data_getter.get('jinhuoshijian')
        the_lifadian = lifadian.objects.get(dianzhulianxi=dianzhulianxi)
        try:
            wz.objects.create(lifadian=the_lifadian,wuziming=wuziming,wuzileixing=wuzileixing,shengyuliang=shengyuliang,
                          jinhuoshijian=jinhuoshijian)
            return JsonResponse({"status": 1, "msg": "添加成功"})
        except IntegrityError:
            _wz = wz.objects.get(lifadian=the_lifadian,wuziming=wuziming,wuzileixing=wuzileixing)
            _wz.jinhuoshijian = jinhuoshijian
            _wz.shengyuliang = _wz.shengyuliang + int(shengyuliang)
            _wz.save()
            return JsonResponse({"status": 0, "msg": "更新成功"})
        except:
            return JsonResponse({"status": -1, "msg": wuziming})

def wuzi_shanchu(request,dianzhulianxi):
    wuziming = request.GET.get("wuziming",0)
    wuzileixing = request.GET.get("wuzileixing",0)
    this = wz.objects.get(lifadian__dianzhulianxi=dianzhulianxi,wuziming=wuziming,wuzileixing=wuzileixing)
    this.delete()
    return JsonResponse({"status":1,"msg":"删除成功"})

def wuzi_xiaohao(request,dianzhulianxi):
    wuziming = request.GET.get("wuziming", 0)
    wuzileixing = request.GET.get("wuzileixing", 0)
    xiaohaoliang = request.GET.get("xiaohaoliang",0)
    this = wz.objects.get(lifadian__dianzhulianxi=dianzhulianxi, wuziming=wuziming, wuzileixing=wuzileixing)

    this.shengyuliang = this.shengyuliang - int(xiaohaoliang)
    if this.shengyuliang <0:
        return JsonResponse({"status":2,"msg":"消耗过大"})
    elif this.shengyuliang == 0:
        this.delete()
        this.save()
        return JsonResponse({"status":3,"msg":"已消耗完"})
    else:
        this.save()
        return JsonResponse({"status": 1, "msg": "消耗成功","number":this.shengyuliang})