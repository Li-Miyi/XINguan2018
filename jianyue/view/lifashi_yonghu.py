from django.shortcuts import render, redirect, reverse

# Create your views here.
from django.http import Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import jianyue
<<<<<<< HEAD
from ..models import yonghu, lifashi, lifadian, fuwu, jiesuandingdan, pingjia, dingdan, jishiqitadizhi, faxing, tupian, \
=======
from ..models import yonghu, lifashi, lifadian, fuwu, jiesuandingdan, pingjia, dingdan, jishiqitadizhi, faxing, tupian,\
>>>>>>> cd77e1b... create
    yuyuedingdan, shoucang
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
    shenfen = data_getter.get('shenfen')
    print(shenfen)
    try:
        if shenfen == 'lifashi':
            xingming = data_getter.get('xingming')
            mima = data_getter.get('mima')
            lianxifangshi = data_getter.get('lianxifangshi')
            xingbie = data_getter.get('xingbie')
            yonghuming = data_getter.get('yonghuming')
            lifadian_id = data_getter.get('lifadian_id')
            lifashi.objects.create(xingming=xingming, yonghuming=yonghuming, mima=mima,
<<<<<<< HEAD
                                   lianxidianhua=int(lianxifangshi),xingbie=xingbie, lifadian_id=lifadian_id)
=======
                                   lianxidianhua=int(lianxifangshi), xingbie=xingbie, lifadian_id=lifadian_id)
>>>>>>> cd77e1b... create
        elif shenfen == 'yonghu':
            xingming = data_getter.get('xingming')
            mima = data_getter.get('mima')
            lianxifangshi = data_getter.get('lianxifangshi')
            xingbie = data_getter.get('xingbie')
            yonghuming = data_getter.get('yonghuming')
            yonghu.objects.create(xingming=xingming, yonghuming=yonghuming, mima=mima, lianxidianhua=lianxifangshi,
<<<<<<< HEAD
                                      xingbie=xingbie)
=======
                                  xingbie=xingbie)
>>>>>>> cd77e1b... create
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
<<<<<<< HEAD
        request.session['is_login'] = True # 登录状态
        request.session["tel"] = lianxifangshi
        request.session.set_expiry(14*24*3600)
=======
        request.session['is_login'] = True  # 登录状态
        request.session["tel"] = lianxifangshi
        request.session.set_expiry(14 * 24 * 3600)
>>>>>>> cd77e1b... create
        print("COOKIES:", request.COOKIES.items())
        print("session:", request.session.items())
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


<<<<<<< HEAD
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


=======
>>>>>>> cd77e1b... create

# 获取理发师详情-用户端
def lifashi_detail(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
<<<<<<< HEAD
    lifashi_id = int(datagetter.get('lifashi_id')[0])
=======
    print(datagetter.get('lifashi_id'))
    print("1")
    lifashi_id = int(datagetter.get('lifashi_id'))
>>>>>>> cd77e1b... create
    lifa_fuwu = []
    lifa_fuwu_detail = {}
    lifashi_lifadian = []
    lifashi_pingjia = []
    try:
        i_lifashi = lifashi.objects.get(id=lifashi_id)
    except lifashi.DoesNotExist:
        print(lifashi_id)
<<<<<<< HEAD
        print("m没有找到")
    for i_fuwu in fuwu.objects.filter(lifashi=i_lifashi):
        try:
            lifa_fuwu_detail = {"fuwu_id": i_fuwu.id, "type": i_fuwu.leixing, "fuwu_name": i_fuwu.fuwumingcheng, "price": i_fuwu.jiage}
=======
        print("没有找到")
    for i_fuwu in fuwu.objects.filter(lifashi=i_lifashi):
        try:
            lifa_fuwu_detail = {"fuwu_id": i_fuwu.id, "type": i_fuwu.leixing, "fuwu_name": i_fuwu.fuwumingcheng,
                                "price": i_fuwu.jiage}
>>>>>>> cd77e1b... create
        except ObjectDoesNotExist:
            print("这里错了")
        lifa_fuwu.append(lifa_fuwu_detail)
    for i_lifadian in lifadian.objects.filter(lifashi=i_lifashi):
<<<<<<< HEAD
        lifadian_detail = {"lifadian_id": i_lifadian.id, "lifadian_name": i_lifadian.dianming, "lifadian_dizhi": i_lifadian.dizhi}
=======
        lifadian_detail = {"lifadian_id": i_lifadian.id, "lifadian_name": i_lifadian.dianming,
                           "lifadian_dizhi": i_lifadian.dizhi}
>>>>>>> cd77e1b... create
        lifashi_lifadian.append(lifadian_detail)
    for i_dingdan in dingdan.objects.filter(lifashi_id=lifashi_id):
        for i_pingjia in pingjia.objects.filter(dingdan_id=i_dingdan.id):
            lifashi_pingjia_detail = {'id': i_pingjia.id, "pingfen": i_pingjia.pingfen, "pingjia": i_pingjia.pingjia}
            lifashi_pingjia.append(lifashi_pingjia_detail)
<<<<<<< HEAD
    return JsonResponse({"id": i_lifashi.id, "name": i_lifashi.xingming, 'phone': i_lifashi.lianxidianhua, "fuwu":lifa_fuwu, "lifadian":lifashi_lifadian, "pingjia":lifashi_pingjia})
=======
    return JsonResponse(
        {"id": i_lifashi.id, "name": i_lifashi.xingming, 'phone': i_lifashi.lianxidianhua, "fuwu": lifa_fuwu,
         "lifadian": lifashi_lifadian, "pingjia": lifashi_pingjia})

>>>>>>> cd77e1b... create

# 获取不同类别的服务——用户端
def FuwuList(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    fuwu_cid = int(datagetter.get("fuwu_cid")[0])
    fuwuList = []
    fuwu_detail = {}
    for i_fuwu in fuwu.objects.filter(leixing=fuwu_cid):
        count = 0
        Allscore = 0
        for i_dingdan in dingdan.objects.filter(fuwuxiang_id=i_fuwu.id):
            count = count + 1
            try:
                i_pingjia = pingjia.objects.get(id=i_dingdan.id)
            except:
                continue
            i_score = i_pingjia.pingfen
            Allscore = Allscore + i_score
        the_score = Allscore / count
        fuwu_detail = {"id": i_fuwu.id, "name": i_fuwu.fuwumingcheng, "price": i_fuwu.jiage, "rate": the_score}
        fuwuList.append(fuwu_detail)
    return JsonResponse(fuwuList, safe=False)

# 返回不同的服务类型——用户端
<<<<<<< HEAD
def fuwuliebiao(request): #服务列表页
=======
def fuwuliebiao(request):  # 服务列表页
>>>>>>> cd77e1b... create
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
<<<<<<< HEAD
    leixing=datagetter.get("leixing")
    fuwuliebiaos=fuwu.objects.filter(leixing=leixing)
    fuwuliebiao=[]
    for fuwu_info in fuwuliebiaos:
        try:
            lifadian_name=fuwu_info.lifashi.lifadian.dianming #店名
            jiage=fuwu_info.jiage #价格
            fuwumingcheng=fuwu_info.fuwumingcheng #服务名称
            dingdan_list=fuwu_info.dingdan_set.all() #反向查询所有的相关订单
            pingfen_sum = 0  # 设定最初总分0
            pingfen_num = 0 # 设定评分数量0
            for dd in dingdan_list:
                pingjia_list=dd.pingjia_set.all()#反向查询每一个订单的相关评价
                for pj in pingjia_list:
                    pingfen_sum=pingfen_sum+pj.pingfen
                    pingfen_num=pingfen_num+1
            pingfen=round(pingfen_sum/pingfen_num,2)
            fuwuliebiao.append({"lifadian_name":lifadian_name,"jiage":jiage,"fuwumingcheng":fuwumingcheng,"leixing":leixing,"pingfen":pingfen})
        except:
            return JsonResponse({"status":0,"msg":"访问错误"})
    if len(fuwuliebiao)==0:
        return JsonResponse({"status":0,"msg":"请指定服务类型"})
    else:
        return JsonResponse(fuwuliebiao,safe=False)
=======
    leixing = datagetter.get("leixing")
    fuwuliebiaos = fuwu.objects.filter(leixing=leixing)
    fuwuliebiao = []
    for fuwu_info in fuwuliebiaos:
        try:
            lifadian_name = fuwu_info.lifashi.lifadian.dianming  # 店名
            jiage = fuwu_info.jiage  # 价格
            fuwumingcheng = fuwu_info.fuwumingcheng  # 服务名称
            dingdan_list = fuwu_info.dingdan_set.all()  # 反向查询所有的相关订单
            pingfen_sum = 0  # 设定最初总分0
            pingfen_num = 0  # 设定评分数量0
            for dd in dingdan_list:
                pingjia_list = dd.pingjia_set.all()  # 反向查询每一个订单的相关评价
                for pj in pingjia_list:
                    pingfen_sum = pingfen_sum + pj.pingfen
                    pingfen_num = pingfen_num + 1
            if pingfen_num == 0 and pingfen_sum == 0:
                pingfen = 'null'
            else:
                pingfen = round(pingfen_sum / pingfen_num, 2)
            fuwuliebiao.append(
                {"lifadian_name": lifadian_name, "jiage": jiage, "fuwumingcheng": fuwumingcheng, "leixing": leixing,
                 "pingfen": pingfen})
        except Exception as e:
            return JsonResponse({"status": 0, "msg": "访问错误"})
    if len(fuwuliebiao) == 0:
        return JsonResponse({"status": 5, "msg": "请指定服务类型"})
    else:
        return JsonResponse(fuwuliebiao, safe=False)

>>>>>>> cd77e1b... create

# 获取理发师详情-用户端
def lifashi_detail(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
<<<<<<< HEAD
    lifashi_id = int(datagetter.get('lifashi_id')[0])
=======
>>>>>>> cd77e1b... create
    lifa_fuwu = []
    lifa_fuwu_detail = {}
    lifashi_lifadian = []
    lifashi_pingjia = []
    faxingList = []
    try:
<<<<<<< HEAD
        i_lifashi = lifashi.objects.get(id=lifashi_id)
    except lifashi.DoesNotExist:
        print(lifashi_id)
=======
        i_lifashi = lifashi.objects.get(id=datagetter.get('lifashi_id'))
    except lifashi.DoesNotExist:
>>>>>>> cd77e1b... create
        print("没有找到")
    for i_fuwu in fuwu.objects.filter(lifashi_id=i_lifashi.id):
        try:
            lifa_fuwu_detail = {"fuwu_id": i_fuwu.id, "type": i_fuwu.leixing, "fuwu_name": i_fuwu.fuwumingcheng,
                                "price": i_fuwu.jiage}
        except ObjectDoesNotExist:
            print("这里错了")
        lifa_fuwu.append(lifa_fuwu_detail)
    for i_lifadian in lifadian.objects.filter(lifashi=i_lifashi):
        lifadian_detail = {"lifadian_id": i_lifadian.id, "lifadian_name": i_lifadian.dianming,
                           "lifadian_dizhi": i_lifadian.dizhi}
        lifashi_lifadian.append(lifadian_detail)
<<<<<<< HEAD
    for i_qitalifadian in jishiqitadizhi.objects.filter(lifashi_id=lifashi_id):
=======
    for i_qitalifadian in jishiqitadizhi.objects.filter(lifashi_id=i_lifashi.id):
>>>>>>> cd77e1b... create
        if i_qitalifadian.zhuangtai == "1":
            i_lifadian = lifadian.objects.get(id=i_qitalifadian.lifadian_id)
            lifadian_detail = {"lifadian_id": i_lifadian.id, "lifadian_name": i_lifadian.dianming,
                               "lifadian_dizhi": i_lifadian.dizhi}
            lifashi_lifadian.append(lifadian_detail)
<<<<<<< HEAD
    for i_dingdan in dingdan.objects.filter(lifashi_id=lifashi_id):
        for i_pingjia in pingjia.objects.filter(dingdan_id=i_dingdan.id):
            lifashi_pingjia_detail = {'id': i_pingjia.id, "pingfen": i_pingjia.pingfen, "pingjia": i_pingjia.pingjia}
            lifashi_pingjia.append(lifashi_pingjia_detail)
    for i_faxing in faxing.objects.filter(lifashi_id=lifashi_id):
=======
    for i_dingdan in dingdan.objects.filter(lifashi_id=i_lifashi.id):
        for i_pingjia in pingjia.objects.filter(dingdan_id=i_dingdan.id):
            lifashi_pingjia_detail = {'id': i_pingjia.id, "pingfen": i_pingjia.pingfen, "pingjia": i_pingjia.pingjia}
            lifashi_pingjia.append(lifashi_pingjia_detail)
    for i_faxing in faxing.objects.filter(lifashi_id=i_lifashi.id):
>>>>>>> cd77e1b... create
        for i_image in tupian.objects.filter(tupianlaiyuan_id=i_faxing.id):
            if (i_image.tupianleixing == "2"):
                faxing_detail = {"f_id": i_faxing.id, "f_name": i_faxing.faxingming, "f_image": str(i_image.src)}
                faxingList.append(faxing_detail)
    return JsonResponse(
<<<<<<< HEAD
        {"id": i_lifashi.id, "name": i_lifashi.xingming, "yonghuming":i_lifashi.yonghuming, 'phone': i_lifashi.lianxidianhua, "fuwu": lifa_fuwu,
=======
        {"id": i_lifashi.id, "name": i_lifashi.xingming, "yonghuming": i_lifashi.yonghuming,
         'phone': i_lifashi.lianxidianhua, "fuwu": lifa_fuwu,
>>>>>>> cd77e1b... create
         "lifadian": lifashi_lifadian, "pingjia": lifashi_pingjia, "faxing": faxingList})


# 获取不同类型的发型库-用户端
def faxingList(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    faxing_c_id = int(datagetter.get('faxing_c_id')[0])
    faxingList = []
    faxing_leixing = {"1": "短发", "2": "烫发", "3": "长发", "4": "染发"}
    for i_faxing in faxing.objects.filter(leixing=faxing_c_id):
        imageList = []
        for i_image in tupian.objects.filter(tupianlaiyuan_id=i_faxing.id):
            if (i_image.tupianleixing == "2"):
                imgae_detail = {"image_id": i_image.id, "image_src": str(i_image.src)}
                imageList.append(imgae_detail)
                faxing_detail = {"id": i_faxing.id, "c_id": i_faxing.leixing,
                                 "c_name": faxing_leixing[i_faxing.leixing], "f_name": i_faxing.faxingming,
                                 "beizhu": i_faxing.beizhu, "image": imageList}
                faxingList.append(faxing_detail)
    return JsonResponse(faxingList, safe=False)


<<<<<<< HEAD


=======
>>>>>>> cd77e1b... create
# 发型详情页面-用户端
def faxingDetail(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    faxing_id = int(datagetter.get('faxing_id')[0])
    imageList = []
    lifadianList = []
    i_faxing = faxing.objects.get(id=faxing_id)
    i_lifashi = lifashi.objects.get(id=i_faxing.lifashi_id)
    lifashi_detail = {"f_id": i_lifashi.id, "f_name": i_lifashi.yonghuming, "phone": i_lifashi.lianxidianhua}
    i_lifadian = lifadian.objects.get(id=i_lifashi.lifadian_id)
    lifadian_detail = {"s_id": i_lifadian.id, "s_name": i_lifadian.dianming, "s_address": i_lifadian.dizhi}
    lifadianList.append(lifadian_detail)
    for i_image in tupian.objects.filter(tupianlaiyuan_id=faxing_id):
        if (i_image.tupianleixing == "2"):
            i_image_src = str(i_image.src)
            imageList.append(i_image_src)
    faxing_detail = {"id": faxing_id, "c_id": i_faxing.leixing, "f_name": i_faxing.faxingming,
                     "beizhu": i_faxing.beizhu, "image": imageList, "lifashi": lifashi_detail, "lifadian": lifadianList}
    return JsonResponse(faxing_detail)

<<<<<<< HEAD
=======

>>>>>>> cd77e1b... create
# 获取用户信息-用户端
def yonghuDetail(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    yonghu_detail = {}
    lianxifangshi = datagetter.get("lianxifangshi")
    i_yonghu = yonghu.objects.get(lianxidianhua=lianxifangshi)
<<<<<<< HEAD
    yonghu_id = i_yonghu.id
    for i_image in tupian.objects.filter(tupianlaiyuan_id=yonghu_id):
        if (i_image.tupianleixing == "3"):
            yonghu_detail = {"id": i_yonghu.id, "lianxifangshi":lianxifangshi,"yonghuming": i_yonghu.yonghuming, "xingming": i_yonghu.xingming,
                                     "sex": i_yonghu.xingbie, "touxiang": str(i_image.src)}
        else:
            yonghu_detail = {"id": i_yonghu.id,"lianxifangshi":lianxifangshi, "yonghuming": i_yonghu.yonghuming, "xingming": i_yonghu.xingming,
                                 "sex": i_yonghu.xingbie, "touxiang": "../../pages/image/默认头像.png"}
    return JsonResponse(yonghu_detail)

=======
    print("这里1")
    yonghu_id = i_yonghu.id
    print(yonghu_id)
    for i_image in tupian.objects.filter(tupianlaiyuan_id=yonghu_id):
        print(i_image.tupianleixing)
        try:
            if (i_image.tupianleixing == "3"):
                yonghu_detail = {"id": i_yonghu.id, "yonghuming": i_yonghu.yonghuming, "xingming": i_yonghu.xingming,
                                 "sex": i_yonghu.xingbie, "touxiang": str(i_image.src)}
        except:
            yonghu_detail = {"id": i_yonghu.id, "yonghuming": i_yonghu.yonghuming, "xingming": i_yonghu.xingming,
                             "sex": i_yonghu.xingbie, "touxiang": "../../pages/image/默认头像.png"}
    return JsonResponse(yonghu_detail)


>>>>>>> cd77e1b... create
# 理发师注册页面获取理发店名-理发师端
def getLifadianName(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    lifadianList = []
    for i_lifadian in lifadian.objects.all():
        i_lifadian_name = i_lifadian.dianming
        i_lifadian_id = i_lifadian.id
        s_lifadian = {"i_name": i_lifadian_name, "id": i_lifadian_id}
        lifadianList.append(s_lifadian)
    return JsonResponse(lifadianList, safe=False)

<<<<<<< HEAD
# 理发师获取首页获取已各种烦订单订单-理发师端
=======
# 获取理发师信息——理发师端
def lifashiDetail(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    lianxifangshi = datagetter.get("lianxifangshi")
    the_lifashi = lifashi.objects.get(lianxidianhua=lianxifangshi)
    the_detail = {"id":the_lifashi.id, "name": the_lifashi.xingming, "yonghuming": the_lifashi.yonghuming, "phone": the_lifashi.lianxidianhua}
    return JsonResponse(the_detail)

# 理发师获取首页获取订单-理发师端
>>>>>>> cd77e1b... create
def getOKDingdan(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
<<<<<<< HEAD
    lifashi_id = int(datagetter.get('lifashi_id')[0])
    zhuangtai_id = int(datagetter.get('zhuangtai_id')[0])
    dingdanList = []
    for i_dingdan in dingdan.objects.filter(lifashi_id=lifashi_id):
            if zhuangtai_id==1 or zhuangtai_id==0:
                for i_jiesuan in jiesuandingdan.objects.filter(dingdan_ptr_id=i_dingdan.id):
                    if i_jiesuan.shifouzhifu == zhuangtai_id:
                        try:
                            i_fuwu = fuwu.objects.get(id=i_dingdan.fuwuxiang_id)
                            print(i_fuwu.jiage)
                            dingdan_detail = {"dingdan_id": i_dingdan.id, "fuwu_name": i_fuwu.fuwumingcheng, "price": i_fuwu.jiage,"jiesuanshijian": i_jiesuan.jieshushijian}
                            dingdanList.append(dingdan_detail)
                        except:
                            return JsonResponse({"status": 0, "msg": "您还没有已完成的订单"})
            else:
                try:
                    for i_yuyue in yuyuedingdan.objects.filter(dingdan_ptr_id=i_dingdan.id):
                        i_fuwu = fuwu.objects.get(id=i_dingdan.fuwuxiang_id)
                        dingdan_detail = {"yueyu_id": i_dingdan.id, "yuyue_start": i_yuyue.yuyuekaishi,
                                          "yuyue_xiaohao": i_yuyue.yuyuexiaohao, "fuwu_name": i_fuwu.fuwumingcheng,"price": i_yuyue.gujifeiyong}
                        dingdanList.append(dingdan_detail)
                except:
                    return JsonResponse({"status":1, "msg": "您还没有预约订单"})
=======
    the_lifashi = lifashi.objects.get(id=datagetter.get('lifashi_id'))
    zhuangtai_id = int(datagetter.get('zhuangtai_id'))
    dingdanList = []
    for i_dingdan in dingdan.objects.filter(lifashi_id=the_lifashi.id):
        if zhuangtai_id == 1 or zhuangtai_id == 0:
            for i_jiesuan in jiesuandingdan.objects.filter(dingdan_ptr_id=i_dingdan.id):
                if i_jiesuan.shifouzhifu == zhuangtai_id:
                    try:
                        i_fuwu = fuwu.objects.get(id=i_dingdan.fuwuxiang_id)
                        print(i_fuwu.jiage)
                        dingdan_detail = {"dingdan_id": i_dingdan.id, "fuwu_name": i_fuwu.fuwumingcheng,
                                          "price": i_fuwu.jiage, "jiesuanshijian": i_jiesuan.jieshushijian}
                        dingdanList.append(dingdan_detail)
                    except:
                        return JsonResponse({"status": 0, "msg": "您还没有已完成的订单"})
        else:
                for i_yuyue in yuyuedingdan.objects.filter(dingdan_ptr_id=i_dingdan.id):
                    i_fuwu = fuwu.objects.get(id=i_dingdan.fuwuxiang_id)
                    dingdan_detail = {"yueyu_id": i_dingdan.id, "is_ok":i_yuyue.yijieshou,"yuyue_start": i_yuyue.yuyuekaishi,
                                      "yuyue_xiaohao": i_yuyue.yuyuexiaohao, "fuwu_name": i_fuwu.fuwumingcheng,
                                      "price": i_fuwu.jiage}
                    dingdanList.append(dingdan_detail)
>>>>>>> cd77e1b... create
    return JsonResponse(dingdanList, safe=False)


# 用户提交预约订单——用户端
def getYuyueOrder(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
<<<<<<< HEAD
    yonghu_phone = datagetter.get('yonghu_phone')
    lifashi_id = datagetter.get('lifashi_id')
    fuwu_id = datagetter.get('fuwu_id')
    yuyuekaishi = datagetter.get('select_time')
    i_lifadian = lifadian.objects.get(datagetter.get('lifadian_id'))
    i_yonghu = yonghu.objects.get(lianxidianhua=yonghu_phone)
    yonghu_id = i_yonghu.id
    yuyuedingdan.objects.create(yuyuekaishi=yuyuekaishi, lifadian=i_lifadian, yonghu=yonghu_id
                                ,lifashi=lifashi_id,fuwuxiang=fuwu_id)

#用户收藏 0-理发店 1-理发师 2-服务——用户端
=======
    yonghudianhua = datagetter.get('yonghu_phone')
    lifashi_id = datagetter.get('lifashi_id')
    fuwu_id = datagetter.get('fuwu_id')
    yuyuekaishi = datagetter.get('select_time')
    lifadian_id = datagetter.get('lifadian_id')
    the_yonghu = yonghu.objects.get(lianxidianhua=yonghudianhua)
    yuyuedingdan.objects.create(yuyuekaishi=yuyuekaishi, lifadian_id=lifadian_id, yonghu=the_yonghu,
                                lifashi_id=lifashi_id, fuwuxiang_id=fuwu_id, yijieshou=0)
    return JsonResponse({"status":"1", "data": "添加成功"})

# 得到用户所有订单——用户端(0-未支付， 1-已支付，2 -预约）
def getYonghuDingdan(request, zhuangtai_id):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    the_yonghu = yonghu.objects.get(id=datagetter.get('yonghu_id'))
    yonghu_id = the_yonghu.id
    dingdanList = []
    print(yonghu_id)
    for i_dingdan in dingdan.objects.filter(yonghu_id=yonghu_id):
        if zhuangtai_id == 1 or zhuangtai_id == 0:
            for i_jiesuan in jiesuandingdan.objects.filter(dingdan_ptr_id=i_dingdan.id):
                if i_jiesuan.shifouzhifu == zhuangtai_id:
                    try:
                        i_fuwu = fuwu.objects.get(id=i_dingdan.fuwuxiang_id)
                        dingdan_detail = {"dingdan_id": i_dingdan.id, "fuwu_name": i_fuwu.fuwumingcheng,
                                          "price": i_fuwu.jiage, "jiesuanshijian": i_jiesuan.jieshushijian}
                        dingdanList.append(dingdan_detail)
                    except:
                        return JsonResponse({"status": 0, "msg": "您还没有已完成的订单"})
        if zhuangtai_id == 2:
                for i_yuyue in yuyuedingdan.objects.filter(dingdan_ptr_id=i_dingdan.id):
                    print(i_dingdan.id)
                    i_fuwu = fuwu.objects.get(id=i_dingdan.fuwuxiang_id)
                    dingdan_detail = {"yueyu_id": i_dingdan.id, "yuyue_start": i_yuyue.yuyuekaishi,
                                      "yuyue_xiaohao": i_yuyue.yuyuexiaohao, "fuwu_name": i_fuwu.fuwumingcheng,"price": i_fuwu.jiage}
                    dingdanList.append(dingdan_detail)
    return JsonResponse(dingdanList, safe=False)

# 用户收藏 0-理发店 1-理发师 2-服务——用户端
>>>>>>> cd77e1b... create
def yonghu_shoucang_add(request, shoucangleixing):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    shoucang_id = datagetter.get('shoucang_id')
    i_yonghu = yonghu.objects.get(id=datagetter.get('yonghu_id'))
    shoucang.objects.create(beishoucang_id=shoucang_id, yonghu=i_yonghu, tupianleixing=shoucangleixing)
    return JsonResponse({"status": '1', "msg": "收藏成功"})


<<<<<<< HEAD
#用户取消收藏 0-理发店 1-理发师 2-服务——用户端
=======
# 用户取消收藏 0-理发店 1-理发师 2-服务——用户端
>>>>>>> cd77e1b... create
def yonghu_shoucang_delete(request, shoucangleixing):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    shoucang_id = datagetter.get('shoucang_id')
    i_yonghu = yonghu.objects.get(id=datagetter.get('yonghu_id'))
    print(shoucangleixing)
    try:
        for i_shoucang in shoucang.objects.filter(yonghu=i_yonghu):
<<<<<<< HEAD
            if int(i_shoucang.tupianleixing)==int(shoucangleixing) and i_shoucang.beishoucang_id==shoucang_id:
                i_shoucang.delete()
                return JsonResponse({"status":"1", "msg": "删除成功"})
    except ObjectDoesNotExist:
        return JsonResponse({"status":"0", "msg": "删除失败1"})
    return JsonResponse({"status":"0", "msg": "删除失败"})

#用户展示收藏 0-理发店 1-理发师 2-服务——用户端
=======
            if int(i_shoucang.tupianleixing) == int(shoucangleixing) and i_shoucang.beishoucang_id == shoucang_id:
                i_shoucang.delete()
                return JsonResponse({"status": "1", "msg": "删除成功"})
    except ObjectDoesNotExist:
        return JsonResponse({"status": "0", "msg": "删除失败1"})
    return JsonResponse({"status": "0", "msg": "删除成功"})


# 用户展示收藏 0-理发店 1-理发师 2-服务——用户端
>>>>>>> cd77e1b... create
def yonghu_shoucang_show(request, shoucangleixing):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    i_yonghu = yonghu.objects.get(id=datagetter.get('yonghu_id'))
<<<<<<< HEAD
    shoucang_list=[]

    try:
        for i_shoucang in shoucang.objects.filter(yonghu=i_yonghu):
            if int(shoucangleixing)== 0 :
                the_lifadian = lifadian.objects.get(id=i_shoucang.beishoucang_id)
                shoucang_detail = {"lifadian_id": i_shoucang.beishoucang_id, "c_id": i_shoucang.tupianleixing, "lifadian_name": the_lifadian.dianming, "phone": the_lifadian.dianzhulianxi}
                shoucang_list.append(shoucang_detail)
            elif(int(shoucangleixing)== 1 ):
                the_lifashi = lifashi.objects.get(id=i_shoucang.beishoucang_id)
                shoucang_detail = {"lifashi_id": i_shoucang.beishoucang_id, "c_id": i_shoucang.tupianleixing,
                                   "lifashi_name": the_lifashi.yonghuming, "phone": the_lifashi.lianxidianhua}
                shoucang_list.append(shoucang_detail)
            else:
                the_fuwu = fuwu.objects.get(id=i_shoucang.beishoucang_id)
                shoucang_detail = {"fuwu_id": i_shoucang.beishoucang_id, "c_id": i_shoucang.tupianleixing,
                               "fuwu_name": the_fuwu.fuwumingcheng, "price": the_fuwu.jiage}
                shoucang_list.append(shoucang_detail)
            return JsonResponse(shoucang_list, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({"status":"0", "msg": "失败"})

=======
    print(i_yonghu)
    shoucang_list = []
    for i_shoucang in shoucang.objects.filter(yonghu_id=i_yonghu.id):
        try:
            if shoucangleixing == 0 and i_shoucang.tupianleixing== "0":
                the_lifadian = lifadian.objects.get(id=i_shoucang.beishoucang_id)
                shoucang_detail = {"lifadian_id": i_shoucang.beishoucang_id, "c_id": i_shoucang.tupianleixing,
                                       "lifadian_name": the_lifadian.dianming, "phone": the_lifadian.dianzhulianxi}
                shoucang_list.append(shoucang_detail)

                continue
            if shoucangleixing == 1 and i_shoucang.tupianleixing == "1":
                print(shoucangleixing)
                the_lifashi = lifashi.objects.get(id=i_shoucang.beishoucang_id)
                shoucang_detail = {"lifashi_id": i_shoucang.beishoucang_id, "c_id": i_shoucang.tupianleixing,
                                       "lifashi_name": the_lifashi.yonghuming, "phone": the_lifashi.lianxidianhua}
                shoucang_list.append(shoucang_detail)
                continue
            if shoucangleixing == 2 and i_shoucang.tupianleixing == "2":

                the_fuwu = fuwu.objects.get(id=i_shoucang.beishoucang_id)
                the_lifashi = lifashi.objects.get(id=the_fuwu.lifashi_id)
                shoucang_detail = {"fuwu_id": i_shoucang.beishoucang_id, "c_id": i_shoucang.tupianleixing,
                                       "fuwu_name": the_fuwu.fuwumingcheng, "fuwu_lifashi": the_lifashi.yonghuming,"price": the_fuwu.jiage}
                shoucang_list.append(shoucang_detail)
                continue
        except ObjectDoesNotExist:
            return JsonResponse({"status": "0", "msg": "失败"})
    return JsonResponse(shoucang_list, safe=False)
>>>>>>> cd77e1b... create
