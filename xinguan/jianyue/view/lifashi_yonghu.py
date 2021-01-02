# Create your views here.
from datetime import datetime
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse,HttpResponse
from django.utils import timezone
from ..models import quxiaodingdan, lifashi_xiaoxi,xiaoxi,yonghu, lifashi, lifadian,huiyuan, fuwu, EmailVerifyRecord,jiesuandingdan, pingjia, dingdan, jishiqitadizhi, faxing, tupian, \
    yuyuedingdan, shoucang, dizhi, zixun,mibao
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import datetime


"""用户与理发师"""

@csrf_exempt
def zhuce(request):
    if request.method == "POST":
        data_getter = request.POST
    elif request.method == "GET":
        data_getter = request.GET
    else:
        return JsonResponse({"success": 0, "msg": "注册失败"})
    shenfen = data_getter.get('shenfen')
    print(data_getter.get('mima'))
    try:
        if shenfen == 'lifashi':
                print("lifashi")
                xingming = data_getter.get('xingming')
                mima = data_getter.get('mima')
                lianxifangshi = data_getter.get('lianxifangshi')
                xingbie = data_getter.get('xingbie')
                yonghuming = data_getter.get('yonghuming')
                lifadian_id = data_getter.get('lifadian_id')
                email = data_getter.get('email')
                lifashi.objects.create(xingming=xingming, yonghuming=yonghuming, mima=mima,
                                       lianxidianhua=int(lianxifangshi), xingbie=xingbie, lifadian_id=lifadian_id, email=email)
        elif shenfen == 'yonghu':
                print("yonghu")
                xingming = data_getter.get('xingming')
                mima = data_getter.get('mima')
                lianxifangshi = data_getter.get('lianxifangshi')
                xingbie = data_getter.get('xingbie')
                yonghuming = data_getter.get('yonghuming')
                email = data_getter.get('email')
                yonghu.objects.create(xingming=xingming, yonghuming=yonghuming, mima=mima, lianxidianhua=lianxifangshi,
                                      xingbie=xingbie, email=email)
        return JsonResponse({"status": 1, "msg": "注册成功"})
    except IntegrityError:
        return JsonResponse({"success": 0, "msg": "手机号码已注册"})

@csrf_exempt
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
        request.session['is_login'] = True  # 登录状态
        request.session["tel"] = lianxifangshi
        request.session.set_expiry(14 * 24 * 3600)
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

def xiugai_lfs(request):
    if request.method == "POST":
        data_getter=request.POST
    elif request.method == "GET":
        data_getter=request.GET
    else:
        return  JsonResponse({"success": 0,"msg": "访问方法错误"})
    ziduan=data_getter.get("ziduan")
    lianxifangshi=data_getter.get("lianxifangshi")
    neirong=data_getter.get("neirong")
    the_lifashi=lifashi.objects.filter(lianxidianhua=lianxifangshi)
    data = {ziduan:neirong}
    try:
        the_lifashi.update(**data)
    except TypeError:
        return JsonResponse({"status": 0, "msg": "字段错误"})
    except IntegrityError:
        return JsonResponse({"status": 2, "msg": "字段内容已被注册"})
    return JsonResponse({"status": 1, "msg": "修改成功"})

def pingfenjiangxu(list):
    n = len(list)
    # 外层循环控制从头走到尾的次数
    for j in range(n - 1):
        # 用一个count记录一共交换的次数，可以排除已经是排好的序列
        count = 0
        # 内层循环控制走一次的过程
        for i in range(0, n - 1 - j):
            # 如果前一个元素小于后一个元素，则交换两个元素（升序）
            if list[i]['pingfen'] < list[i + 1]['pingfen']:
                # 交换元素
                list[i], list[i + 1] = list[i + 1], list[i]
                # 记录交换的次数
                count += 1
        # count == 0 代表没有交换，序列已经有序
    return list

def liebiao(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    duixiang=datagetter.get('duixiang')
    page=int(datagetter.get('page'))
    pagesize=int(datagetter.get('pagesize'))
    paixufangshi=datagetter.get('paixufangshi')
    #理发师和理发店的所有数据
    lifadian_datas = []
    lifashi_datas = []
    for i_lifadian in lifadian.objects.all():
        #理发店图片
        lifadian_data = {"name": i_lifadian.dianming, "id": i_lifadian.pk}
        try:
            lifadiantupian=tupian.objects.filter(tupianleixing=0,tupianlaiyuan_id=i_lifadian.pk)[0].src.name
            if "http" in lifadiantupian:
                lifadian_data["lifadiantupian"]=lifadiantupian
            else:
                lifadian_data["lifadiantupian"]="http://127.0.0.1:8000/media/"+lifadiantupian
        except:
            lifadian_data["lifadiantupian"]="https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1023914563,1561594966&fm=26&gp=0.jpg"
        i_lifadian_total_pingfen = 0
        i_lifadian_total_jiage = 0
        i_lifadian_count = 0
        for i_lifashi in lifashi.objects.filter(lifadian=i_lifadian):
            lifashi_data = {'id': i_lifashi.id, 'name': i_lifashi.xingming, 'lifadian' :i_lifadian.dianming}
            #头像
            try:
                lifashitouxiang=tupian.objects.get(tupianleixing=5,tupianlaiyuan_id=i_lifashi.id).src.name
                if "http" in lifashitouxiang:
                    lifashi_data["lifashitouxiang"]=lifashitouxiang
                else:
                    lifashi_data["lifashitouxiang"]="http://127.0.0.1:8000/media/"+lifashitouxiang
            except:
                lifashi_data["lifashitouxiang"]="https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=1746949651,2632447771&fm=26&gp=0.jpg"
            i_lifashi_total_pingfen = 0
            i_lifashi_total_jiage = 0
            i_lifashi_count = 0
            lifashi_data["month_count"] = "暂无"
            for i_jiesuan in jiesuandingdan.objects.filter(lifashi=i_lifashi):
                #月销售额
                month_count=0
                time_now_year=datetime.datetime.now().year
                time_now_month=datetime.datetime.now().month
                if i_jiesuan.jieshushijian.year==time_now_year and i_jiesuan.jieshushijian.month==time_now_month:
                    month_count += 1
                #月销售额
                if month_count!= 0:
                    lifashi_data["month_count"] = str(month_count)+"件"
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
    #分页数据
    if duixiang=="lifashi":
        if paixufangshi=='价格最低':
            lifashi_datas=jiageshengxu(lifashi_datas)
        elif paixufangshi=='价格最高':
            lifashi_datas=jiagejiangxu(lifashi_datas)
        elif paixufangshi=='好评优先':
            lifashi_datas==pingfenjiangxu(lifashi_datas)
        else:
            pass
        lifashi_return=[]
        if(len(lifashi_datas)%pagesize==0):
            total_pages=len(lifashi_datas)//pagesize
        else:
            total_pages=len(lifashi_datas)//pagesize + 1
        print((len((lifashi_datas))))
        if(page<total_pages):
            i=0
            while(i<pagesize):
                lifashi_return.append(lifashi_datas[i+(page-1)*pagesize])
                i=i+1
            return JsonResponse({"lifashi": lifashi_return, "lifashihasMoreData": True})
        if(page>=total_pages):
            i=0
            while(i<len(lifashi_datas)-(page-1)*pagesize):
                lifashi_return.append(lifashi_datas[i+(page-1)*pagesize])
                i=i+1
            return JsonResponse({"lifashi": lifashi_return, "lifashihasMoreData": False})
    if duixiang=="lifadian":
        if paixufangshi=='价格最低':
            lifadian_datas=jiageshengxu(lifadian_datas)
        elif paixufangshi=='价格最高':
            lifadian_datas=jiagejiangxu(lifadian_datas)
        elif paixufangshi=='好评优先':
            lifadian_datas==pingfenjiangxu(lifadian_datas)
        else:
            pass
        lifadian_return=[]
        if(len(lifadian_datas)%pagesize==0):
            total_pages=len(lifadian_datas)//pagesize
        else:
            total_pages=len(lifadian_datas)//pagesize + 1
        print((len((lifadian_datas))))
        if(page<total_pages):
            i=0
            while(i<pagesize):
                lifadian_return.append(lifadian_datas[i+(page-1)*pagesize])
                i=i+1
            return JsonResponse({"lifadian": lifadian_return, "lifadianhasMoreData": True})
        if(page>=total_pages):
            i=0
            while(i<len(lifadian_datas)-(page-1)*pagesize):
                lifadian_return.append(lifadian_datas[i+(page-1)*pagesize])
                i=i+1
            return JsonResponse({"lifadian": lifadian_return, "lifadianhasMoreData": False})
    # return JsonResponse({"lifashi": lifashi_datas, "lifadian": lifadian_datas})


def lifashi_detail(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    print(datagetter.get('lifashi_id'))
    fuwuleixing = {"1":"洗吹","2":"烫发","3":"染发","4":"剪发","5":"护理"}
    faxingleixing = {"1":"短发","2":"烫发","3":"长发","4":"染发"}
    the_lifashi = lifashi.objects.get(id=datagetter.get('lifashi_id'))
    lifashi_id = the_lifashi.id
    lifa_fuwu = []
    lifashi_lifadian = []
    lifashi_faxing = []
    lifashi_pingjia = []
    try:
        i_lifashi = lifashi.objects.get(id=lifashi_id)
    except lifashi.DoesNotExist:
        return JsonResponse({"status": 0,"msg":"id输入错误"})
    for i_fuwu in fuwu.objects.filter(lifashi=i_lifashi):
        try:
            search_dict = {"tupianleixing": "6", "tupianlaiyuan_id":i_lifadian.id}
            i_tupian = tupian.objects.filter(**search_dict).first()
            src = str(i_tupian.src)
        except:
            src = "http://img.08087.cc/uploads/20190819/10/1566182856-otPJlNpiKT.jpeg"
        lifa_fuwu_detail = {"fuwu_id": i_fuwu.id, "type": fuwuleixing[i_fuwu.leixing], "fuwu_name": i_fuwu.fuwumingcheng,
                                "price": i_fuwu.jiage,"tupian":src}
        lifa_fuwu.append(lifa_fuwu_detail)
    for i_lifadian in lifadian.objects.filter(lifashi=i_lifashi):
        try:
            search_dict = {"tupianleixing": "0", "tupianlaiyuan_id":i_lifadian.id}
            i_tupian = tupian.objects.filter(**search_dict).first()
            src = str(i_tupian.src)
        except:
            src = "../../image/0.jpg"
        lifadian_detail = {"lifadian_id": i_lifadian.id, "lifadian_name": i_lifadian.dianming, "tupian":src}
        lifashi_lifadian.append(lifadian_detail)
        print(lifadian_detail)
    for i_faxing in faxing.objects.filter(lifashi=i_lifashi):
        try:
            search_dict = {"tupianleixing": "2", "tupianlaiyuan_id": i_faxing.id}
            i_tupian = tupian.objects.filter(**search_dict).first()
            src = str(i_tupian.src)
        except:
            src = "../../image/0.jpg"
        faxing_detail = {"faxing_id":i_faxing.id, "faxingname": i_faxing.faxingming, "leixing": faxingleixing[i_faxing.leixing],"tupian": src}
        lifashi_faxing.append(faxing_detail)
    for i_dingdan in dingdan.objects.filter(lifashi_id=lifashi_id):
        for i_pingjia in pingjia.objects.filter(dingdan_id=i_dingdan.id):
            lifashi_pingjia_detail = {'id': i_pingjia.id, "pingfen": i_pingjia.pingfen, "pingjia": i_pingjia.pingjia}
            lifashi_pingjia.append(lifashi_pingjia_detail)
    return JsonResponse(
        {"id": i_lifashi.id, "name": i_lifashi.xingming, "yonghuming": i_lifashi.yonghuming,'phone': i_lifashi.lianxidianhua, "fuwu": lifa_fuwu,
         "lifadian": lifashi_lifadian, "faxing":lifashi_faxing,"pingjia": lifashi_pingjia})

# 返回不同的服务类型——用户端
def fuwuliebiao(request):  # 服务列表页
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
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
                {"fuwu_id": fuwu_info.id ,"lifadian_name": lifadian_name, "jiage": jiage, "fuwumingcheng": fuwumingcheng, "leixing": leixing,
                 "pingfen": pingfen})
        except Exception as e:
            return JsonResponse({"status": 0, "msg": "访问错误"})
    if len(fuwuliebiao) == 0:
        return JsonResponse({"status": 5, "msg": "请指定服务类型"})
    else:
        return JsonResponse(fuwuliebiao, safe=False)

#根据服务列表获得服务列表详情
def fuwuliebiaoxiangqing(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    try:
        fuwu_id=datagetter.get("fuwu_id")
        fuwuxiangqing=fuwu.objects.get(id=fuwu_id) #获取服务实体
        fw_leixing=fuwuxiangqing.get_leixing_display() #类型
        fw_jiage=fuwuxiangqing.jiage #价格
        fw_mingcheng=fuwuxiangqing.fuwumingcheng #名称
        dingdan=fuwuxiangqing.dingdan_set.all() #反向查询每一个订单的相关评价
        pingfen_sum = 0  # 设定最初总分0
        pingfen_num = 0  # 设定评分数量0
        for dd in dingdan:
            pingjia_list = dd.pingjia_set.all()  # 反向查询每一个订单的相关评价
            for pj in pingjia_list:
                pingfen_sum = pingfen_sum + pj.pingfen
                pingfen_num = pingfen_num + 1
        if pingfen_num == 0 and pingfen_sum == 0:
            pingfen = '暂无评价'
        else:
            pingfen = round(pingfen_sum / pingfen_num, 2)
        fw_pingfen=pingfen #评分
        fw_xingming=fuwuxiangqing.lifashi.xingming #理发师姓名
        fw_xingbie=fuwuxiangqing.lifashi.get_xingbie_display()#理发师性别
        fw_lianxidianhua=fuwuxiangqing.lifashi.lianxidianhua#理发师电话
        lifashitupian=tupian.objects.filter(tupianlaiyuan_id=fuwuxiangqing.lifashi.id)[0]
        fw_lifashi_image=str(lifashitupian.src)
        fw_dianming=fuwuxiangqing.lifashi.lifadian.dianming#理发店名字
        fw_dizhi=fuwuxiangqing.lifashi.lifadian.dizhi_set.all()[0].name#理发店地址
        fw_dianzhulianxi=fuwuxiangqing.lifashi.lifadian.dianzhulianxi#店主联系方式
        lifadiantupian=tupian.objects.filter(tupianlaiyuan_id=fuwuxiangqing.lifashi.lifadian.id)[0]
        fw_lifadian_image=str(lifadiantupian.src)
        result=JsonResponse({"leixing":fw_leixing,"jiage":fw_jiage,"mingcheng":fw_mingcheng,"pingfen":fw_pingfen,
                             "xingming":fw_xingming,"xingbie":fw_xingbie,"lianxidianhua":fw_lianxidianhua,
                             "lifashi_image":fw_lifashi_image,"lifadian_image":fw_lifadian_image,"dianming":fw_dianming,
                             "dizhi":fw_dizhi,"dianzhulianxi":fw_dianzhulianxi})
    except Exception as e:
        result=JsonResponse({"status": 0, "msg": "访问失败","cuowu":str(e)})
    return result


# 获取不同类型的发型库-用户端
def faxingList(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    faxing_c_id = int(datagetter.get('faxing_c_id')[0])
    page =  datagetter.get('page')
    start = int(page)*6
    pagesize = int(datagetter.get('pagesize'))
    faxing_len = faxing.objects.filter(leixing=faxing_c_id).count()
    faxing1 = faxing.objects.filter(leixing=faxing_c_id).order_by('-id')[start:start+pagesize]
    faxingList = []
    faxing_leixing = {"1": "短发", "2": "烫发", "3": "长发", "4": "染发"}
    for i_faxing in faxing1:
        imageList = []
        for i_image in tupian.objects.filter(tupianlaiyuan_id=i_faxing.id):
            if (i_image.tupianleixing == "2"):
                if "https://" in str(i_image.src):
                    i_image.src = str(i_image.src)
                else:
                    i_image.src = "http://127.0.0.1:8000/media/" + str(i_image.src)
                imgae_detail = {"image_id": i_image.id, "image_src": str(i_image.src)}
                imageList.append(imgae_detail)
        faxing_detail = {"id": i_faxing.id, "c_id": i_faxing.leixing,
                                 "c_name": faxing_leixing[i_faxing.leixing], "f_name": i_faxing.faxingming,
                                 "beizhu": i_faxing.beizhu, "image": imageList}
        faxingList.append(faxing_detail)
    return JsonResponse({'faxing':faxingList, "pagenum" : int(page)+1, 'total':faxing_len})


# 发型详情页面-用户端
def faxingDetail(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    faxing_id = int(datagetter.get('faxing_id'))
    imageList = []
    faxingList = []
    lifashiList = []
    lifadianList = []
    lifadianimageList = []
    i_faxing = faxing.objects.get(id=faxing_id)
    i_lifashi = lifashi.objects.get(id=i_faxing.lifashi_id)
    for lifashi_image in tupian.objects.filter(tupianlaiyuan_id=i_lifashi.id):
        if (lifashi_image.tupianleixing == "5"):
            if "https://" in str(lifashi_image.src):
                lifashi_image.src = str(lifashi_image.src)
            else:
                lifashi_image.src = "http://127.0.0.1:8000/media/" + str(lifashi_image.src)
            lifashi_image_src = str(lifashi_image.src)
    lifashi_detail = {"f_id": i_lifashi.id, "f_name": i_lifashi.yonghuming,
                      "phone": i_lifashi.lianxidianhua, "f_image" : lifashi_image_src}
    lifashiList.append(lifashi_detail)
    i_lifadian = lifadian.objects.get(id=i_lifashi.lifadian_id)
    i_dizhi = dizhi.objects.get(lifadian_id=i_lifadian.id)
    for lifadian_image in tupian.objects.filter(tupianlaiyuan_id=i_lifadian.id):
        if (lifadian_image.tupianleixing == "0"):
            if "https://" in str(lifadian_image.src):
                lifadian_image.src = str(lifadian_image.src)
            else:
                lifadian_image.src = "http://127.0.0.1:8000/media/" + str(lifadian_image.src)
            lifadian_image_src = str(lifadian_image.src)
            lifadianimageList.append(lifadian_image_src)
    lifadian_detail = {"s_id": i_lifadian.id, "s_name": i_lifadian.dianming,
                       "s_address" : i_dizhi.name, "s_image" : lifadianimageList[0]}
    lifadianList.append(lifadian_detail)
    for i_image in tupian.objects.filter(tupianlaiyuan_id=faxing_id):
        if (i_image.tupianleixing == "2"):
            if "https://" in str(i_image.src):
                i_image.src = str(i_image.src)
            else:
                i_image.src = "http://127.0.0.1:8000/media/" + str(i_image.src)
            i_image_src = str(i_image.src)
            imageList.append(i_image_src)
    faxing_detail = {"id": faxing_id, "c_id": i_faxing.leixing, "f_name": i_faxing.faxingming,
                     "beizhu": i_faxing.beizhu, "image": imageList}
    faxingList.append(faxing_detail)
    return JsonResponse({'faxing': faxingList, 'lifashi': lifashiList, 'lifadian': lifadianList})



# 获取用户信息-用户端
def yonghuDetail(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    yonghu_detail = {}
    sex = {"0":"女","1":"男"}
    lianxifangshi = datagetter.get("lianxifangshi")
    print(lianxifangshi)
    i_yonghu = yonghu.objects.get(lianxidianhua=lianxifangshi)
    yonghu_id = i_yonghu.id
    try:
        yonghu_detail = {"id": i_yonghu.id, "yonghuming": i_yonghu.yonghuming, "xingming": i_yonghu.xingming,
                "sex": sex[i_yonghu.xingbie]}
        return JsonResponse(yonghu_detail)
    except:
        return JsonResponse({"status": 0,"msg": "用户信息调取失败"})
    # for i_image in tupian.objects.filter(tupianlaiyuan_id=yonghu_id):
    #     print(i_image.tupianleixing)
    #     try:
    #         if (i_image.tupianleixing == "3"):
    #             yonghu_detail = {"id": i_yonghu.id, "yonghuming": i_yonghu.yonghuming, "xingming": i_yonghu.xingming,
    #                              "sex": sex[i_yonghu.xingbie], "touxiang": str(i_image.src)}
    #     except:
    #         yonghu_detail = {"id": i_yonghu.id, "yonghuming": i_yonghu.yonghuming, "xingming": i_yonghu.xingming,
    #                          "sex": sex[i_yonghu.xingbie], "touxiang": "../../pages/image/默认头像.png"}


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


# 理发师获取首页获取订单-理发师端
@csrf_exempt
def lifashi_get_dingdan(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    page = datagetter.get('page')
    start = int(page)*10
    pagesize = int(datagetter.get('pagesize'))
    the_lifashi = lifashi.objects.get(id=datagetter.get('lifashi_id'))
    zhuangtai_id = int(datagetter.get('zhuangtai_id'))
    dingdanList = []
    shifouzhifu = ['未支付',"已支付"]
    if zhuangtai_id == 1 or zhuangtai_id == 0:
            dingdan_len = jiesuandingdan.objects.filter(lifashi_id=the_lifashi.id,shifouzhifu=zhuangtai_id).count()
            Dingdan =  jiesuandingdan.objects.filter(lifashi_id=the_lifashi.id,shifouzhifu=zhuangtai_id).order_by('-id')[start:start+pagesize]
            for i_jiesuan in Dingdan:
                if i_jiesuan.shifouzhifu == zhuangtai_id:
                    jieshushijian = str(i_jiesuan.jieshushijian).replace("T", " ")
                    try:
                        i_huiyuan = huiyuan.objects.filter(yonghu=i_jiesuan.yonghu,lifashi=i_jiesuan.lifashi)
                        if i_huiyuan.exists():
                            is_huiyuan = True
                        else:
                            is_huiyuan = False
                        i_fuwu = fuwu.objects.get(id=i_jiesuan.fuwuxiang_id)
                        dingdan_detail = {"dingdan_id": i_jiesuan.id, "fuwu_name": i_fuwu.fuwumingcheng,"price": i_fuwu.jiage, 
                                        "shijian": jieshushijian,"shifouzhifu":shifouzhifu[int(i_jiesuan.shifouzhifu)],"is_huiyuan":is_huiyuan}
                        dingdanList.append(dingdan_detail)
                    except:
                        return JsonResponse({"status": 0, "msg": "您还没有已完成的订单"})
    else:
        dingdan_len = yuyuedingdan.objects.filter(lifashi_id=the_lifashi.id).count()
        Yuyue =  yuyuedingdan.objects.filter(lifashi_id=the_lifashi.id).order_by('-dingdan_ptr_id')[start:start+pagesize]
        for i_yuyue in Yuyue:
            i_fuwu = fuwu.objects.get(id=i_yuyue.fuwuxiang_id)
            i_huiyuan = huiyuan.objects.filter(yonghu=i_yuyue.yonghu,lifashi=i_yuyue.lifashi)
            if i_huiyuan.exists():
                is_huiyuan = True
            else:
                is_huiyuan = False
            dingdan_detail = {"yuyue_id": i_yuyue.id, "is_jieshou":i_yuyue.yijieshou,"shijian": i_yuyue.yuyuekaishi,"is_huiyuan":is_huiyuan,
                              "yuyue_xiaohao": i_yuyue.yuyuexiaohao, "fuwu_name": i_fuwu.fuwumingcheng,"price": i_fuwu.jiage,
                                      }
            dingdanList.append(dingdan_detail)
    return JsonResponse({'Dingdan':dingdanList,'pagenum': int(page)+1,'total': dingdan_len})

# 获取理发师信息——理发师端
def lifashiDetail(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    lianxifangshi = datagetter.get("lianxifangshi")
    the_lifashi = lifashi.objects.get(lianxidianhua=lianxifangshi)
    the_detail = {"id":the_lifashi.id, "name": the_lifashi.xingming,
                          "yonghuming": the_lifashi.yonghuming, "phone": the_lifashi.lianxidianhua}
    return JsonResponse(the_detail)
#用户修改订单信息
@csrf_exempt
def xiugai_yuyue_dingdan(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    yuyue_id = datagetter.get("yuyue_id")
    yuyue_shijian = datagetter.get('yuyue_shijian')
    print(yuyue_shijian)
    try:
        i_yuyue = yuyuedingdan.objects.get(id=yuyue_id)
        i_yuyue.yuyuekaishi = yuyue_shijian
        i_yuyue.save()
        return JsonResponse({"msg":"修改成功","status":1})
    except:
        return JsonResponse({"msg":"修改失败","status":0})



# 用户提交预约订单——用户端
@csrf_exempt
def getYuyueOrder(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    yonghudianhua = datagetter.get('yonghu_phone')
    lifashi_id = datagetter.get('lifashi_id')
    fuwu_id = datagetter.get('fuwu_id')
    yuyuekaishi = datagetter.get('select_time')
    lifadian_id = datagetter.get('lifadian_id')
    the_yonghu = yonghu.objects.get(lianxidianhua=yonghudianhua)
    yuyuedingdan.objects.create(yuyuekaishi=yuyuekaishi, lifadian_id=lifadian_id, yonghu=the_yonghu,
                                lifashi_id=lifashi_id, fuwuxiang_id=fuwu_id, yijieshou=0)
    return JsonResponse({"status":"1","data":"添加成功"})

@csrf_exempt
#用户取消预约
def CancelOrder(request):
    yuyue_id = request.POST.get("dingdan_id")
    try:
        dingdan.objects.get(id=yuyue_id).delete()
        return JsonResponse({"status":0, "msg": "删除成功"})
    except:
        return JsonResponse({"status":1, "msg": "删除失败"})

@csrf_exempt
#返回所有的取消订单 0-用户 1-理发师
def lifashi_show_quxiao_dingdan(request,shenfeng):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    the_id = datagetter.get('the_id')
    page = datagetter.get('page')
    start = int(page*6)
    pagesize = int(datagetter.get('pagesize'))
    if(shenfeng==0):
        Quxiao = quxiaodingdan.objects.filter(yonghu=the_id).order_by('-id')[start:start+pagesize]
        quxiao_len = quxiaodingdan.objects.filter(yonghu=the_id).count()
    else:
        Quxiao = quxiaodingdan.objects.filter(lifashi=the_id).order_by('-id')[start:start+pagesize]
        quxiao_len = quxiaodingdan.objects.filter(lifashi=the_id).count()
    dingdanList = []
    for i_quxiao in Quxiao:
        i_fuwu_id = i_quxiao.fuwuxiang_id
        i_fuwu = fuwu.objects.get(id=i_fuwu_id)
        try:
            i_tupian_src = tupian.objects.get(tupianleixing="6",tupianlaiyuan_id=i_fuwu_id)
        except:
            i_tupian_src = "https://s3.ax1x.com/2020/12/11/rAJowR.jpg"
        i_lifashi_id = i_fuwu.lifashi_id
        dingdan_detail = {"fuwu_id":i_fuwu.id,"fuwu_name":i_fuwu.fuwumingcheng,
        "quxiaoshijian":i_quxiao.quxiaoshijian,"quxiao_yuanyin":i_quxiao.quxiaoyuanyin,"fuwu_tupian":i_tupian_src}
        dingdanList.append(dingdan_detail)
    return JsonResponse({"dingdan":dingdanList,"total":quxiao_len,"pagenum":int(page)+1})


# 用户收藏 0-理发店 1-理发师 2-服务——用户端
@csrf_exempt
def yonghu_shoucang_add(request, shoucangleixing):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    shoucang_id = datagetter.get('shoucang_id')
    i_yonghu = yonghu.objects.get(id=datagetter.get('yonghu_id'))
    shoucang.objects.create(beishoucang_id=shoucang_id, yonghu=i_yonghu, shoucangleixing=shoucangleixing)
    return JsonResponse({"status": '1', "msg": "收藏成功"})

#判断用户是否收藏 0-理发店 1-理发师 2-服务——用户端
@csrf_exempt
def yonghu_is_shoucang(request, shoucangleixing):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    yonghu_id = datagetter.get('yonghu_id')
    shoucang_id = datagetter.get('shoucang_id')
    result = shoucang.objects.filter(beishoucang_id=shoucang_id,yonghu=yonghu_id,shoucangleixing=shoucangleixing)
    if result:
        return JsonResponse({'msg':"收藏","is_shoucang":True})
    else:
        return JsonResponse({'msg':"没有收藏","is_shoucang":False})


# 用户取消收藏 0-理发店 1-理发师 2-服务——用户端
@csrf_exempt
def yonghu_shoucang_delete(request, shoucangleixing):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    shoucang_id = datagetter.get('shoucang_id')
    i_yonghu = yonghu.objects.get(id=datagetter.get('yonghu_id'))
    try:
        i_shoucang = shoucang.objects.get(yonghu=i_yonghu,shoucangleixing=shoucangleixing,beishoucang_id=shoucang_id)
        i_shoucang.delete()
        return JsonResponse({"status": "1", "msg": "删除成功"})
    except ObjectDoesNotExist:
        return JsonResponse({"status": "0", "msg": "删除失败"})


# 用户展示收藏 0-理发店 1-理发师 2-服务——用户端
def yonghu_shoucang_show(request, shoucangleixing):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    i_yonghu = yonghu.objects.get(id=datagetter.get('yonghu_id'))
    shoucang_list = []
    for i_shoucang in shoucang.objects.filter(yonghu=i_yonghu):
        if  shoucangleixing== 0 and int(i_shoucang.shoucangleixing) == shoucangleixing :
            the_lifadian = lifadian.objects.get(id=i_shoucang.beishoucang_id)
            shoucang_detail = {"lifadian_id": i_shoucang.beishoucang_id, "c_id": i_shoucang.shoucangleixing,
                                   "lifadian_name": the_lifadian.dianming, "phone": the_lifadian.dianzhulianxi}
            shoucang_list.append(shoucang_detail)
        elif shoucangleixing== 1 and int(i_shoucang.shoucangleixing) == shoucangleixing:
            the_lifashi = lifashi.objects.get(id=i_shoucang.beishoucang_id)
            shoucang_detail = {"lifashi_id": i_shoucang.beishoucang_id, "c_id": i_shoucang.shoucangleixing,
                                   "lifashi_name": the_lifashi.yonghuming, "phone": the_lifashi.lianxidianhua}
            shoucang_list.append(shoucang_detail)
        elif shoucangleixing== 2 and int(i_shoucang.shoucangleixing) == shoucangleixing:
            print(i_shoucang.beishoucang_id)
            the_fuwu = fuwu.objects.get(id=i_shoucang.beishoucang_id)
            shoucang_detail = {"fuwu_id": i_shoucang.beishoucang_id, "c_id": i_shoucang.shoucangleixing,
                                   "fuwu_name": the_fuwu.fuwumingcheng, "price": the_fuwu.jiage}
            shoucang_list.append(shoucang_detail)
    return JsonResponse(shoucang_list, safe=False)





# 得到用户所有订单——用户端(0-未支付， 1-已支付，2 -预约）
@csrf_exempt
def getYonghuDingdan(request, zhuangtai_id):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    the_yonghu = yonghu.objects.get(id=datagetter.get('yonghu_id'))
    zhuangtai = ["未支付", "已支付", "预约"]
    yonghu_id = the_yonghu.id
    dingdanList = []
    for i_dingdan in dingdan.objects.filter(yonghu_id=yonghu_id):
        if zhuangtai_id == 1 or zhuangtai_id == 0:
            for i_jiesuan in jiesuandingdan.objects.filter(dingdan_ptr_id=i_dingdan.id):
                if i_jiesuan.shifouzhifu == zhuangtai_id:
                    try:
                        i_fuwu = fuwu.objects.get(id=i_dingdan.fuwuxiang_id)
                        jiesuanshijian = str(i_jiesuan.jieshushijian).replace("T"," ")
                        try:
                            i_huiyuan = huiyuan.objects.get(yonghu=the_yonghu,lifashi=i_fuwu.lifashi)
                            is_huiyuan = True
                        except:
                            is_huiyuan = False
                        try:
                            i_jiage = i_jiesuan.shijifeiyong
                        except:
                            i_jiage = i_fuwu.jiage
                        dingdan_detail = {"dingdan_id": i_dingdan.id, "fuwu_name": i_fuwu.fuwumingcheng, "zhuangtai": zhuangtai[zhuangtai_id],
                                          "price": i_jiage, "jiesuanshijian": jiesuanshijian,"is_huiyuan":is_huiyuan}
                        dingdanList.append(dingdan_detail)
                    except:
                        return JsonResponse({"status": 0, "msg": "您还没有已完成的订单"})
        if zhuangtai_id == 2:
                for i_yuyue in yuyuedingdan.objects.filter(dingdan_ptr_id=i_dingdan.id):
                    try:
                        i_huiyuan = huiyuan.objects.get(yonghu=the_yonghu,lifashi=i_yuyue.lifashi)
                        is_huiyuan = True
                    except:
                        is_huiyuan = False
                    i_fuwu = fuwu.objects.get(id=i_dingdan.fuwuxiang_id)
                    dingdan_detail = {"yuyue_id": i_dingdan.id, "yuyue_start": i_yuyue.yuyuekaishi,"zhuangtai": zhuangtai[zhuangtai_id],
                                      "yuyue_xiaohao": i_yuyue.yuyuexiaohao, "fuwu_name": i_fuwu.fuwumingcheng,"price": i_fuwu.jiage,"is_huiyuan":is_huiyuan}
                    dingdanList.append(dingdan_detail)
    return JsonResponse(dingdanList, safe=False)

#理发师——预约订单总数
def count_yuyue(request):
    id = request.GET.get("yuyuedingdan_id")
    yuyuexiaohao = request.GET.get("yuyuexiaohao")
    yuyuexiaohao = datetime.datetime.strptime(yuyuexiaohao, '%H:%M')
    the = yuyuedingdan.objects.get(id=id)
    begin = the.yuyuekaishi
    deadline = the.yuyuekaishi + timezone.timedelta(
        hours=yuyuexiaohao.hour,
        minutes=yuyuexiaohao.minute,
        )
    after = yuyuedingdan.objects.filter(lifadian__lifashi=the.lifashi,yuyuekaishi__gt=begin,yuyuekaishi__lt=deadline,yijieshou=1)
    before = []
    the_in = []
    for i in yuyuedingdan.objects.filter(lifadian__lifashi=the.lifashi,yijieshou=1):
        i_deadline = i.yuyuekaishi + timezone.timedelta(
            hours=i.yuyuexiaohao.hour,
            minutes=i.yuyuexiaohao.minute,
            seconds=i.yuyuexiaohao.second)
        if begin <= i_deadline <= deadline:
            before.append(i)
        elif i_deadline >= deadline and i.yuyuekaishi <= begin:
            the_in.append(i)
    num =  len(list(set(list(after))  | set(before) | set(the_in)))
    return JsonResponse({"status":"1","msg":num})

#理发师获取自己的理发店——理发师端
def lifashigetLifadian(request, zhuangtaiid):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    i_lifashi = lifashi.objects.get(id=datagetter.get("lifashi_id"))
    i_lifahi_id = i_lifashi.id
    lifadianList = []
    for i_dizhi in jishiqitadizhi.objects.filter(lifashi_id=i_lifahi_id):
        if int(i_dizhi.zhuangtai) == zhuangtaiid :
            the_lifadian = lifadian.objects.get(id=i_dizhi.lifadian_id)
            shenqingshijian = str(i_dizhi.shenqingshijian).replace("T"," ")
            the_detail = {"dianzhuming": the_lifadian.dianzhuming, "phone":the_lifadian.dianzhulianxi, "lifadian_id": the_lifadian.id,
                              "name":the_lifadian.dianming, "time":shenqingshijian,"zhuangtai":i_dizhi.zhuangtai}
            lifadianList.append(the_detail)
    return JsonResponse(lifadianList, safe=False)


#理发师增加其他地址
@csrf_exempt
def jishidizhi_add(request):
    lifashi_id = request.POST.get("lifashi_id")
    lifadian_id = request.POST.get("lifadian_id")
    jishiqitadizhi.objects.create(lifashi_id=lifashi_id,lifadian_id=lifadian_id,shenqingshijian=timezone.now(),zhuangtai='0')
    return JsonResponse({"status":1,"msg":"申请成功"})

@csrf_exempt
# 理发师撤销其他地址
def jishidizhi_delete(request):
    lifashi_id = int(request.POST.get("lifashi_id"))
    lifadian_id = int(request.POST.get('lifadian_id'))
    for i_dizhi in jishiqitadizhi.objects.filter(lifashi_id=lifashi_id):
        if i_dizhi.lifadian_id == lifadian_id:
            i_dizhi.delete()
            break
    return JsonResponse({"status":1, "msg": "删除成功"})

#理发师增加服务
@csrf_exempt
def fuwu_add(request):
    lifashi_id = request.POST.get("lifashi_id")
    fuwu_name = request.POST.get("fuwu_name")
    fuwu_leixing = request.POST.get('leixing')
    jiage = request.POST.get("jiage")
    fuwu.objects.create(lifashi_id=lifashi_id, fuwumingcheng=fuwu_name, leixing=fuwu_leixing, jiage=jiage)
    return JsonResponse({"status":1,"msg":"增加成功"})

@csrf_exempt
# 理发师删除服务
def fuwu_delete(request):
    fuwu_id = int(request.POST.get('fuwu_id'))
    i_fuwu = fuwu.objects.get(id=fuwu_id)
    i_fuwu.delete()
    return JsonResponse({"status":1, "msg": "删除成功"})

@csrf_exempt
# 理发师——预约订单详情
def yuyue_show(request):
    yuyue_id = int(request.POST.get('yuyue_id'))
    i_yuyue = yuyuedingdan.objects.get(id=yuyue_id)
    i_dingdan = dingdan.objects.get(id=yuyue_id)
    i_yonghu = yonghu.objects.get(id=i_dingdan.yonghu_id)
    i_lifashi = lifashi.objects.get(id=i_dingdan.lifashi_id)
    try:
        i_tupian = tupian.objects.get(tupianleixing="3", tupianlaiyuan_id=i_yonghu.id)
        src = i_tupian.src
    except:
        src = "../../image/默认头像.png"
    try:
        the_tupian = tupian.objects.get(tupianleixing="1", tupianlaiyuan_id=i_lifashi.id)
        the_src = the_tupian.src
    except:
        the_src = "../../image/默认头像.png"
    if i_yuyue.yuyuexiaohao != None:
        gujishijian = i_yuyue.yuyuexiaohao
    else:
        gujishijian ="00:00"
    i_fuwu = fuwu.objects.get(id=i_dingdan.fuwuxiang_id)
    i_lifadian = lifadian.objects.get(id=i_dingdan.lifadian_id)
    return JsonResponse({"yonghuming":i_yonghu.yonghuming, "phone": i_yonghu.lianxidianhua, "touxiang": str(src), "xiaohao":gujishijian ,
                         "shifoujieshou": i_yuyue.yijieshou,"yuyuekaishi": i_yuyue.yuyuekaishi,
                         "lifashi":{"lifashi_id":i_lifashi.id, "lifashi_name": i_lifashi.xingming, "lifashi_phone": i_lifashi.lianxidianhua, "touxiang":str(the_src) },
                         "fuwu": i_fuwu.fuwumingcheng, "lifadian": i_lifadian.dianming, "fuwu_price": i_fuwu.jiage})

@csrf_exempt
# 理发师——预约订单提交估计时间
def yuyue_submit(request):
    yuyue_id = int(request.POST.get('yuyue_id'))
    yuyuexiaohao = request.POST.get('yuyuexiaohao')
    i_yuyue = yuyuedingdan.objects.get(id=yuyue_id)
    i_yuyue.yuyuexiaohao=yuyuexiaohao
    i_yuyue.yijieshou = '1'
    i_yuyue.save()
    return JsonResponse({"status":1, "msg": "提交成功"})

@csrf_exempt
# 理发师——获取已完成订单详情
def OKdingdan(request):
    dingdan_id = int(request.POST.get('dingdan_id'))
    i_dingdan = dingdan.objects.get(id=dingdan_id)
    i_jiesuan =jiesuandingdan.objects.get(id=i_dingdan.id)
    i_yonghu = yonghu.objects.get(id=i_dingdan.yonghu_id)
    i_lifashi = lifashi.objects.get(id=i_dingdan.lifashi_id)
    shifouzhifu = ['false', 'true']
    try:
        i_tupian = tupian.objects.get(tupianleixing="3", tupianlaiyuan_id=i_yonghu.id)
        src = i_tupian.src
    except:
        src = "../../image/0.png"
    try:
        i_lifashi_tupian = tupian.objects.get(tupianleixing="1", tupianlaiyuan_id=i_lifashi.id)
        lifashi_src = i_lifashi_tupian.src
    except:
        lifashi_src = "../../image/默认头像.png"
    i_fuwu = fuwu.objects.get(id=i_dingdan.fuwuxiang_id)
    i_lifadian = lifadian.objects.get(id=i_dingdan.lifadian_id)
    try:
        i_pingjia = pingjia.objects.get(dingdan_id=i_dingdan.id)
        is_pingjia = "true"
        the_pingjia = {"pingfen":i_pingjia.pingfen, "pingjia": i_pingjia.pingjia}
    except:
        is_pingjia = 'false'
        the_pingjia = {}
    return JsonResponse({"dingdan_id":i_dingdan.id,"yonghuming": i_yonghu.yonghuming, "phone": i_yonghu.lianxidianhua, "touxiang": str(src),
                         "jiesuanshijian": i_jiesuan.jieshushijian,
                         "lifashi":{ "lifashi_id": i_lifashi.id,"lifashi_phone":i_lifashi.lianxidianhua,"lifashi_name": i_lifashi.xingming,"lifashi_touxiang":lifashi_src},
                         "is_zhifu": shifouzhifu[i_jiesuan.shifouzhifu], "fuwu": i_fuwu.fuwumingcheng,
                         "lifadian": i_lifadian.dianming, "fuwu_price": i_fuwu.jiage, "is_pingjia": is_pingjia,"pingjia": the_pingjia})

#用户——获取理发店信息
def getLifadian(request):
    lifadian_id = request.GET.get('lifadian_id')
    i_lifadian = lifadian.objects.get(id=lifadian_id)
    try:
        i_dizhi = dizhi.objects.get(lifadian_id=lifadian_id)
        the_dizhi={"lng": i_dizhi.lng, "lat": i_dizhi.lat}
        dizhi_name = i_dizhi.name
    except:
        the_dizhi={}
        dizhi_name = "暂无地址信息"
    lifashiList=[]
    fuwuList = []
    leixing = ["洗吹","烫发","染发","剪发","护理"]
    lifadian_tupianList=[]
    for i_lifashi in lifashi.objects.filter(lifadian_id=lifadian_id):
        try:
            lifashi_tupian = tupian.objects.get(tupianleixing="1", tupianlaiyuan_id=i_lifashi.id)
            src = lifashi_tupian.src
        except:
            src="../../image/默认头像.png"
        the_detail = {"lifashi_id": i_lifashi.id, "name": i_lifashi.yonghuming, "phone": i_lifashi.lianxidianhua,"lifashi_img": str(src)}
        lifashiList.append(the_detail)
        for i_fuwu in fuwu.objects.filter(lifashi_id=i_lifashi.id):
            print(i_fuwu.leixing)
            the_fuwu = {"fuwu_id": i_fuwu.id, "name": i_fuwu.fuwumingcheng, "type": leixing[int(i_fuwu.leixing)]}
            fuwuList.append(the_fuwu)
    try:
        for i_tupian in tupian.objects.filter(tupianleixing="0", tupianlaiyuan_id=i_lifadian.id):
            the_tupian = {"tupian_id": i_tupian.id, "src": str(i_tupian.src)}
            lifadian_tupianList.append(the_tupian)
    except:
        lifadian_tupianList = []
    return JsonResponse({"lifadian_name": i_lifadian.dianming, "lifadian_phone":i_lifadian.dianzhulianxi, "dizhi":the_dizhi,
                         "dizhiming":dizhi_name, "lifadian_img":lifadian_tupianList,"lifashi":lifashiList, "fuwu": fuwuList})


#用户支付函数
@csrf_exempt
def zhifu(request):
    dingdan_id = request.POST.get('dingdan_id')
    i_dingdan = jiesuandingdan.objects.get(id=dingdan_id)
    i_fuwu = i_dingdan.fuwuxiang
    i_yonghu = i_dingdan.yonghu
    i_lifashi = i_dingdan.lifashi
    print(i_yonghu.id)
    print(i_lifashi.id)
    try:
        i_huiyuan = huiyuan.objects.get(yonghu=i_yonghu,lifashi=i_lifashi) 
        dingdan_jiage = i_fuwu.jiage * 0.8
    except:
        dingdan_jiage = i_fuwu.jiage
    print(dingdan_jiage)
    i_dingdan.shifouzhifu='1'
    i_dingdan.shijifeiyong = dingdan_jiage 
    i_dingdan.save()
    return JsonResponse({"status": "1","msg":"支付成功"})

@csrf_exempt
#用户评价
def set_pingjia(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    try:
        dingdan_id = int(datagetter.get("dingdan_id"))
        i_dingdan = dingdan.objects.get(id=dingdan_id)
        pingfen = datagetter.get("score1")
        pingfen=int(pingfen)
        i_pingjia = datagetter.get("text")
        yonghu_id=dingdan.objects.get(id=dingdan_id).yonghu_id
        i_yonghu = yonghu.objects.get(id=yonghu_id)
        yonghu_id=int(yonghu_id)
        pingjia.objects.create(dingdan=i_dingdan,yonghu=i_yonghu,pingfen=pingfen,pingjia=i_pingjia)
        return JsonResponse({ "msg": "评论成功"})
    except Exception as e:
        return JsonResponse({"message":str(e)})

@csrf_exempt
#用户添加社区资讯
def fabuzixun(request):
    yonghu_id = request.POST.get("yonghu_id")
    print(yonghu_id)
    the_neirong = request.POST.get("neirong")
    i_zixun = zixun.objects.create(neirong=the_neirong, yonghu_id=yonghu_id)
    zixun_id = i_zixun.id
    print(zixun_id)
    return JsonResponse({"staus":"发布成功", "zixun_id": zixun_id})


#统计数据
@csrf_exempt
def tongji_yuedu(request):
    yonghu_id = request.POST.get("id")
    the_dingdan = jiesuandingdan.objects.filter(yonghu_id=yonghu_id,jieshushijian__year=timezone.now().year)
    sum_month_res = the_dingdan.annotate(month=ExtractMonth("jieshushijian")).\
        values("month").order_by("month").annotate(price=Sum('shijifeiyong'))
    data=[0]*12
    for i in sum_month_res:
        data[i['month']-1] = i["price"]
    return JsonResponse({'status':1,"data":data})

@csrf_exempt
def tongji_leixing(request):
    yonghu_id = request.POST.get("id")
    the_dingdan = jiesuandingdan.objects.filter(yonghu_id=yonghu_id,jieshushijian__year=timezone.now().year)

    data = {}

    for i in the_dingdan:
        key = i.fuwuxiang.get_leixing_display()
        data.setdefault(key,0)
        data[key] += i.shijifeiyong
    output= []
    for k,v in data.items():
        output.append({"name":k,"value":v})
    return JsonResponse({'status': 1, "data": output})

#用户得到社区资讯
def getZixun(request):
    page = request.GET.get('page')
    start = int(page)*10
    pagesize = int(request.GET.get('pagesize'))
    ZixunList = []
    zixun_len =  zixun.objects.all().count()
    Zixun = zixun.objects.all().order_by('-id')[start:start+pagesize]
    for item in Zixun:
        i_yonghu = item.yonghu
        the_zixun_tupian = tupian.objects.get(tupianlaiyuan_id=item.id, tupianleixing=4)
        zixun_tupian_src = "http://127.0.0.1:8000/media/"+the_zixun_tupian.src.name
        the_touxiang_tupian = tupian.objects.get(tupianlaiyuan_id=i_yonghu.id, tupianleixing=3)
        touxiang_tupian_src = the_touxiang_tupian.src.name
        zixun_detail = {"id":item.id, "yonghuming":i_yonghu.yonghuming, "yonghu_id": i_yonghu.id, "yonghu_touxiang":touxiang_tupian_src,
                        "neirong": item.neirong, "dianzanshu": item.dianzanshu, 'fabushijian':item.fabushijian,
                        'zixun_tupian_src':zixun_tupian_src}
        ZixunList.append(zixun_detail)
    return JsonResponse({'zixun':ZixunList,"pagenum": int(page)+1,'total':zixun_len})

def zhucemibao(request):
    if request.method == "POST":
        data_getter = request.POST
    elif request.method == "GET":
        data_getter = request.GET
    else:
        return JsonResponse({"success": 0, "msg": "注册失败"})
    shenfen = data_getter.get('shenfen')
    mibaowenti=data_getter.get('mibaowenti')
    mibaodaan=data_getter.get('mibaodaan')
    mibaolaiyuan_id=data_getter.get('mibaolaiyuan_id')
    try:
        mibao.objects.create(shenfen=shenfen,mibaowenti=mibaowenti,mibaodaan=mibaodaan,mibaolaiyuan_id=mibaolaiyuan_id)
        return JsonResponse({"status": 1, "msg": "注册成功"})
    except:
        return JsonResponse({"success": 0, "msg": "注册失败"})

def huoqumibao(request):
    if request.method == "POST":
        data_getter = request.POST
    elif request.method == "GET":
        data_getter = request.GET
    else:
        return JsonResponse({"success": 0, "msg": "注册失败"})
    shenfen=data_getter.get('shenfen')
    mibaolaiyuan_id=data_getter.get('mibaolaiyuan_id')
    try:
        yonghumibao=mibao.objects.get(shenfen=shenfen,mibaolaiyuan_id=mibaolaiyuan_id)
        mibaowenti=yonghumibao.mibaowenti
        mibaodaan=yonghumibao.mibaodaan
        return JsonResponse({"success": 1,"mibaozhuangtai": 1,"mibaowenti": mibaowenti,"mibaodaan" :mibaodaan})
    except:
        return JsonResponse({"success" :0,"mibaozhuangtai" :0,"msg" :"未找到该用户密保，请注册"})

def xiugaimibao(request):
    if request.method == "POST":
        data_getter = request.POST
    elif request.method == "GET":
        data_getter = request.GET
    else:
        return JsonResponse({"success": 0, "msg": "修改失败"})
    shenfen=data_getter.get('shenfen')
    mibaolaiyuan_id=data_getter.get('mibaolaiyuan_id')
    yuanmibaodaan=data_getter.get('yuanmibaodaan')
    xinmibaowenti=data_getter.get('xinmibaowenti')
    xinmibaodaan=data_getter.get('xinmibaodaan')
    data={"mibaowenti": xinmibaowenti,"mibaodaan": xinmibaodaan}
    try:
        yonghumibao=mibao.objects.filter(shenfen=shenfen,mibaolaiyuan_id=mibaolaiyuan_id)
        mibaodaan=mibao.objects.filter(shenfen=shenfen,mibaolaiyuan_id=mibaolaiyuan_id)[0].mibaodaan
        print(yonghumibao)
        if yuanmibaodaan==mibaodaan:
            yonghumibao.update(**data)
            return JsonResponse({"status": 1, "msg": "修改成功"})
        else:
            return JsonResponse({"status": 2,"msg": "原密保答案错误","yuanmibaodaan":yuanmibaodaan,"mibaodaan":mibaodaan})
    except Exception as e:
        return JsonResponse({"status": 0,"msg": str(e)})

def xiugaimima2(request):
    if request.method == "POST":
        data_getter = request.POST
    elif request.method == "GET":
        data_getter = request.GET
    else:
        return JsonResponse({"success": 0, "msg": "修改失败"})
    yuanmima=data_getter.get('yuanmima')
    xinmima=data_getter.get('xinmima')
    shenfen=data_getter.get('shenfen')
    lianxidianhua=data_getter.get('lianxidianhua')
    data={"mima":xinmima}
    try:
        if shenfen == 'lifashi':
            the_lifashi=lifashi.objects.filter(lianxidianhua=lianxidianhua)
            if the_lifashi[0].mima == yuanmima:
                the_lifashi.update(**data)
                return JsonResponse({"status": 1,"msg" :"修改成功"})
            else:
                return JsonResponse({"status": 2,"msg": "密码错误"})
        else:
            the_yonghu=yonghu.objects.filter(lianxidianhua=lianxidianhua)
            if the_yonghu[0].mima == yuanmima:
                the_yonghu.update(**data)
                return JsonResponse({"status": 1, "msg": "修改成功"})
            else:
                return JsonResponse({"status": 2, "msg": "密码错误"})
    except Exception as e:
        return  JsonResponse({"status": 0,"msg" :str(e)})

def jiageshengxu(list):
    n = len(list)
    # 外层循环控制从头走到尾的次数
    for j in range(n - 1):
        # 用一个count记录一共交换的次数，可以排除已经是排好的序列
        count = 0
        # 内层循环控制走一次的过程
        for i in range(0, n - 1 - j):
            # 如果前一个元素大于后一个元素，则交换两个元素（升序）
            if list[i]['price'] > list[i + 1]['price']:
                # 交换元素
                list[i], list[i + 1] = list[i + 1], list[i]
                # 记录交换的次数
                count += 1
        # count == 0 代表没有交换，序列已经有序
    return list

def jiagejiangxu(list):
    n = len(list)
    # 外层循环控制从头走到尾的次数
    for j in range(n - 1):
        # 用一个count记录一共交换的次数，可以排除已经是排好的序列
        count = 0
        # 内层循环控制走一次的过程
        for i in range(0, n - 1 - j):
            # 如果前一个元素小于后一个元素，则交换两个元素（升序）
            if list[i]['price'] < list[i + 1]['price']:
                # 交换元素
                list[i], list[i + 1] = list[i + 1], list[i]
                # 记录交换的次数
                count += 1
        # count == 0 代表没有交换，序列已经有序
    return list


#用户对资讯进行点赞
def dianzan_zixun(request):
    zixun_id = request.GET.get('zixun_id')
    i_zixun = zixun.objects.get(id=zixun_id)
    dianzanshu = i_zixun.dianzanshu+1
    i_zixun.dianzanshu = dianzanshu
    try:
        i_zixun.save()
        return JsonResponse({"status":1,"msg":"点赞成功"})
    except:
        return JsonResponse({"status":0,"msg":"点赞失败"})

# 得到理发师所有发型——理发师端(1-短发，2 -烫发， 3 -长发，4 -染发）
@csrf_exempt
def getFaxing(request, faxing_c_id):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    i_lifashi = lifashi.objects.get(id=datagetter.get("lifashi_id"))
    i_lifashi_id = i_lifashi.id
    faxing_c_id = faxing_c_id
    page = datagetter.get('page')
    start = int(page)*6
    pagesize = int(datagetter.get('pagesize'))
    faxing_len = faxing.objects.filter(lifashi_id = i_lifashi_id,leixing=faxing_c_id).count()
    faxing1 = faxing.objects.filter(lifashi_id = i_lifashi_id,leixing=faxing_c_id).order_by('-id')[start:start+pagesize]
    faxingList = []
    faxing_leixing = {"1": "短发", "2": "烫发", "3": "长发", "4": "染发"}
    for i_faxing in faxing1:
        imageList = []
        for i_image in tupian.objects.filter(tupianlaiyuan_id=i_faxing.id,tupianleixing="2"):
            if "https://" in str(i_image.src):
                i_image.src = str(i_image.src)
            else:
                i_image.src = "http://127.0.0.1:8000/media/"+str(i_image.src)
            imgae_detail = {"image_id": i_image.id, "image_src": str(i_image.src)}
            imageList.append(imgae_detail)
        faxing_detail = {"id": i_faxing.id, "c_id": i_faxing.leixing,
                                     "c_name": faxing_leixing[i_faxing.leixing], "f_name": i_faxing.faxingming,
                                     "f_beizhu": i_faxing.beizhu, "image": imageList}
        faxingList.append(faxing_detail)
    return JsonResponse({'faxing': faxingList, 'pagenum': int(page)+1, 'total':faxing_len})

#理发师添加发型
@csrf_exempt
def faxing_add(request):
    lifashi_id = request.POST.get("lifashi_id")
    faxing_name = request.POST.get("mingcheng")
    faxing_leixing = request.POST.get('leixing')
    faxing_xinxi = request.POST.get("xinxi")
    i_faxing= faxing.objects.create(lifashi_id = lifashi_id, faxingming = faxing_name, leixing = faxing_leixing, beizhu = faxing_xinxi)
    faxing_id = i_faxing.id
    print(faxing_id)
    return JsonResponse({"staus": "添加成功", "faxing_id": faxing_id})

import random
def get_random_code(length=4):
    """获得随机字符串"""
    code = ''
    choice_str = '0123456789'
    for _ in range(length):
        random_str = random.choice(choice_str)
        code += random_str
    return code

#找回密码 0=用户 1=理发师
from django.conf import settings
from django.core.mail import send_mail
def fasongyouxiang(request,shenfen):
    """type=1 找回密码"""
    _type = request.GET.get("type")
    lianxifangshi = request.GET.get("lianxifangshi")
    """发送邮件"""
    email_rcode = EmailVerifyRecord()
    from_email = settings.DEFAULT_FROM_EMAIL
    # 忘记密码发送验证邮件, 和 发送验证码逻辑一样
    if shenfen==0:
        try:
            i_yonghu = yonghu.objects.get(lianxidianhua=lianxifangshi)
            email = i_yonghu.email
        except:
            return JsonResponse({"status":"0", "msg":"用户不存在"})
    else:
        try:
            i_yonghu = lifashi.objects.get(lianxidianhua=lianxifangshi)
            email = i_yonghu.email
        except:
            return JsonResponse({"status":"0", "msg":"用户不存在"})
    if _type == '1':
        random_code = get_random_code()
        email_title = '找回密码'
        email_body = '您的验证码为：'+random_code
        # 保存验证码
        email_rcode.code = random_code
        email_rcode.send_type = _type
        email_rcode.email = email
        email_rcode.yonghu = i_yonghu
        email_rcode.save()
        # 真正启动Django自带的发送邮件功能，邮件标题，邮件内容，发送人，发给谁，发送成功则返回1，失败则返回0
        email_status = send_mail(subject=email_title, message=email_body, from_email=from_email, recipient_list=[email])
        return HttpResponse(email_status)

#找回密码，验证验证码 0=用户 1=理发师
def checkyanzhengma(request, shenfen):
    lianxifangshi = request.GET.get("lianxifangshi")
    the_code = request.GET.get("code")
    if shenfen==0:
        i_yonghu = yonghu.objects.get(lianxidianhua=lianxifangshi)
    else:
        i_yonghu = lifashi.objects.get(lianxidianhua=lianxifangshi)
    print(i_yonghu)
    email_rcode = EmailVerifyRecord.objects.get(yonghu=i_yonghu)
    code = email_rcode.code
    if the_code == code:
        email_rcode.delete()
        return JsonResponse({"status":"1","msg":"验证码一致"})
    else:
        return JsonResponse({"status":"0","msg":"验证码错误"})

#重置密码，验证验证码 0=用户 1=理发师
@csrf_exempt
def xiugaimima(request, shenfen):
    lianxifangshi = request.POST.get("lianxifangshi")
    new_mima = request.POST.get("mima")
    try:
        if shenfen==0:
                i_yonghu = yonghu.objects.get(lianxidianhua=lianxifangshi)
                i_yonghu.mima = new_mima
                i_yonghu.save()
        else:
                i_yonghu = lifashi.objects.get(lianxidianhua=lianxifangshi)
                i_yonghu.mima = new_mima
                i_yonghu.save()
        return JsonResponse({"status":"true","msg":"修改成功"})
    except:
        return JsonResponse({"status":"false","msg":"修改失败"})



#统计理发师数据
@csrf_exempt
def lifashi_tongji_yuedu(request):
    lifashi_id = request.POST.get("id")
    the_dingdan = jiesuandingdan.objects.filter(lifashi_id=lifashi_id,jieshushijian__year=timezone.now().year)
    sum_month_res = the_dingdan.annotate(month=ExtractMonth("jieshushijian")).\
        values("month").order_by("month").annotate(price=Sum('shijifeiyong'))
    data=[0]*12
    for i in sum_month_res:
        data[i['month']-1] = i["price"]
    return JsonResponse({'status':1,"data":data})

@csrf_exempt
def lifashi_tongji_leixing(request):
    lifashi_id = request.POST.get("id")
    the_dingdan = jiesuandingdan.objects.filter(lifashi_id=lifashi_id,jieshushijian__year=timezone.now().year)
    data = {}
    for i in the_dingdan:
        key = i.fuwuxiang.get_leixing_display()
        data.setdefault(key,0)
        data[key] += i.shijifeiyong
    output= []
    for k,v in data.items():
        output.append({"name":k,"value":v})
    return JsonResponse({'status': 1, "data": output})


@csrf_exempt
def getFuwu(request):
    page = request.GET.get('page')
    start = int(page) * 10
    pagesize = int(request.GET.get('pagesize'))
    lifa_fuwu = []
    fuwuleixing = {"1": "洗吹", "2": "烫发", "3": "染发", "4": "剪发", "5": "护理"}
    the_lifashi = lifashi.objects.get(id=request.GET.get('lifashi_id'))
    lifashi_id = the_lifashi.id
    try:
        i_lifashi = lifashi.objects.get(id=lifashi_id)
    except lifashi.DoesNotExist:
        return JsonResponse({"status": 0, "msg": "id输入错误"})
    fuwu_len = fuwu.objects.filter(lifashi=i_lifashi).count()
    for i_fuwu in fuwu.objects.filter(lifashi=i_lifashi).order_by('-id')[start:start + pagesize]:
        try:
            #search_dict = {"tupianleixing": "1", "tupianlaiyuan_id": i_lifashi.id}
            # i_tupian = tupian.objects.filter(**search_dict).first()
            i_tupian = tupian.objects.get(tupianlaiyuan=i_lifashi.id, tupianleixing="1")
            src = str(i_tupian.src)
        except:
            src = "../../image/0.jpg"
        lifa_fuwu_detail = {"fuwu_id": i_fuwu.id, "type": fuwuleixing[i_fuwu.leixing],
                            "fuwu_name": i_fuwu.fuwumingcheng,
                            "price": i_fuwu.jiage, "tupian": src}
        lifa_fuwu.append(lifa_fuwu_detail)
    return JsonResponse({'fuwu': lifa_fuwu, "pagenum": int(page) + 1, 'total': fuwu_len})

def number_timefield(the_dingdan,begin,deadline):
    after = the_dingdan.filter(yuyuekaishi__gt=begin, yuyuekaishi__lt=deadline,
                                        yijieshou=1)
    before = []
    the_in = []
    for i in the_dingdan:
        i_deadline = i.yuyuekaishi + timezone.timedelta(
            hours=i.yuyuexiaohao.hour,
            minutes=i.yuyuexiaohao.minute,
            seconds=i.yuyuexiaohao.second)
        if begin <= i_deadline <= deadline:
            before.append(i)
        elif i_deadline>=deadline and i.yuyuekaishi <= begin:#计算包括这段时间的
            the_in.append(i)

    # print([after,before,the_in])
    num =  len(list(set(list(after))  | set(before)| set(the_in)))
    return num
#用户——当前理发师预约人数
def lifashi_count_yuyue(request):
    lifashi_id = request.GET.get("lifashi_id")
    select_time = request.GET.get("select_time")
    the_time = datetime.datetime.strptime(select_time, "%Y-%M-%d")
    # now = timezone.now().today()
    data=[]
    start = timezone.datetime(year=the_time.year, month=the_time.month, day=the_time.day)
    the_dingdan = yuyuedingdan.objects.filter(lifashi_id=lifashi_id,yuyuekaishi__gte=start)
    for i in range(12):
        end = start+ timezone.timedelta(hours=2)
        num = number_timefield(the_dingdan, start, end)
        if i==5 or i==6 or i==7 or i==8 or i==9 or i==10:
            data.append({"begin": start, "end": end, "number": num})
        start = end
    return JsonResponse({"msg":"成功","data":data})
#理发师修改预约订单为结算订单
@csrf_exempt
def lifashi_yuyue_jiesuan(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    yuyuedingdan_id = datagetter.get("yuyuedingdan_id")
    jieshushijian = datetime.datetime.now()
    # 保存主表的订单
    i_dingdan = dingdan.objects.get(id=yuyuedingdan_id)
    i_fuwuxiang_id = i_dingdan.fuwuxiang_id
    i_lifadian_id = i_dingdan.lifadian_id
    i_lifashi_id = i_dingdan.lifashi_id
    i_yonghu_id = i_dingdan.yonghu_id
    #保存子表的订单信息，然后删除
    i_yuyuedingdan = yuyuedingdan.objects.get(id=yuyuedingdan_id)
    i_dingdan.delete()
    i_yuyuedingdan.delete()
    try:
        dingdan.objects.create(id=yuyuedingdan_id, fuwuxiang_id=i_fuwuxiang_id, lifadian_id=i_lifadian_id, lifashi_id=i_lifashi_id, yonghu_id=i_yonghu_id)
        i_fuwu = fuwu.objects.get(id=i_fuwuxiang_id)
        fuwu_price = i_fuwu.jiage
        jiesuandingdan.objects.create(id=yuyuedingdan_id,jieshushijian=jieshushijian,shijifeiyong=fuwu_price,
        fuwuxiang_id=i_fuwuxiang_id, lifadian_id=i_lifadian_id, lifashi_id=i_lifashi_id, yonghu_id=i_yonghu_id)
        return JsonResponse({'status':1,"msg":"修改订单状态成功"})
    except:
        return JsonResponse({'status':0,"msg":"失败"})

#理发师或者用户取消预约订单
@csrf_exempt
def cancel_yuyue_dingdan(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    yuyuedingdan_id = datagetter.get('yuyuedingdan_id')
    i_quxiaoshijian = datetime.datetime.now()
    i_quxiaoyuanyin = datagetter.get('yuanyin')
     # 保存主表的信息
    i_dingdan = dingdan.objects.get(id=yuyuedingdan_id)
    i_fuwuxiang_id = i_dingdan.fuwuxiang_id
    i_lifadian_id = i_dingdan.lifadian_id
    i_lifashi_id = i_dingdan.lifashi_id
    i_yonghu_id = i_dingdan.yonghu_id
    #保存子表的订单信息，然后删除
    i_yuyuedingdan = yuyuedingdan.objects.get(id=yuyuedingdan_id)
    i_dingdan.delete()
    i_yuyuedingdan.delete()
    try:
        dingdan.objects.create(id=yuyuedingdan_id, fuwuxiang_id=i_fuwuxiang_id, lifadian_id=i_lifadian_id, lifashi_id=i_lifashi_id, yonghu_id=i_yonghu_id)
        i_fuwu = fuwu.objects.get(id=i_fuwuxiang_id)
        fuwu_price = i_fuwu.jiage
        quxiaodingdan.objects.create(id=yuyuedingdan_id,quxiaoshijian=i_quxiaoshijian,quxiaoyuanyin=i_quxiaoyuanyin,
        fuwuxiang_id=i_fuwuxiang_id, lifadian_id=i_lifadian_id, lifashi_id=i_lifashi_id, yonghu_id=i_yonghu_id)
        return JsonResponse({'status':1,"msg":"取消订单成功"})
    except:
        return JsonResponse({'status':0,"msg":"失败"})

#用户申请理发师会员
@csrf_exempt
def yonghu_huiyuan(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    lifashi_id = datagetter.get('lifashi_id')
    yonghu_id = datagetter.get('yonghu_id')
    i_lifashi = lifashi.objects.get(id=lifashi_id)
    i_yonghu = yonghu.objects.get(id=yonghu_id)
    try:
        huiyuan.objects.create(yonghu=i_yonghu,lifashi=i_lifashi,zhuangtai="0")
        return JsonResponse({'status':1,"msg":"申请会员成功"})
    except:
        return JsonResponse({'status':0,"msg":"申请会员失败"})

# 判断用户是否是该理发师的会员
@csrf_exempt
def yonghu_is_huiyuan(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    lifashi_id = datagetter.get('lifashi_id')
    yonghu_id = datagetter.get('yonghu_id')
    i_lifashi = lifashi.objects.get(id=lifashi_id)
    i_yonghu = yonghu.objects.get(id=yonghu_id)
    try:
        i_huiyuan = huiyuan.objects.get(yonghu=i_yonghu,lifashi=i_lifashi,zhuangtai="1")
        return JsonResponse({'is_huiyuan':True,"msg":"是会员"})
    except:
        return JsonResponse({'is_huiyuan':False,"msg":"不是会员"})

#理发师同意用户申请会员
@csrf_exempt
def lifashi_confirm_huiyuan(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    lifashi_id = datagetter.get('lifashi_id')
    yonghu_id = datagetter.get('yonghu_id')
    i_lifashi = lifashi.objects.get(id=lifashi_id)
    i_yonghu = yonghu.objects.get(id=yonghu_id)
    try:
        i_huiyuan = huiyuan.objects.get(yonghu=i_yonghu,lifashi=i_lifashi)
        i_huiyuan.zhuangtai = "1"
        return JsonResponse({'status':1,"msg":"确认成功"})
    except:
        return JsonResponse({'status':0,"msg":"确认失败"})

#用户获取自己所有会员
@csrf_exempt
def yonghu_show_huiyuan(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    yonghu_id = datagetter.get("yonghu_id")
    page = datagetter.get('page')
    pagesize = datagetter.get('pagesize')
    start = page*6
    huiyuan_list = []
    try:
        huiyuan_len = huiyuan.objects.filter(yonghu=yonghu_id).count()
    except:
        huiyuan_len = 0
    Huiyuan = huiyuan.objects.filter(yonghu=yonghu_id,zhuangtai="1").order_by('-id')[int(start):int(start+pagesize)]
    for item in Huiyuan:
        i_lifashi = item.lifashi
        print(i_lifashi.id)
        try:
            i_lifashi_tupian = tupian.objects.get(tupianlaiyuan_id=i_lifashi.id, tupianleixing=1)
            lifashi_tupian_src = i_lifashi_tupian.src.name
        except:
            lifashi_tupian_src = "../../image/lifashi1.png"
        try:
            xiaofei_count = jiesuandingdan.objects.get(yonghu=yonghu_id,lifashi=i_lifashi).count()
        except:
            xiaofei_count = 0
        huiyuan_detail = {
            'id':item.id,"lifashi_id":i_lifashi.id,"lifashi_name":i_lifashi.yonghuming,"xiaofei_count":xiaofei_count,"lifashi_image":lifashi_tupian_src,
            "zhuangtai": int(item.zhuangtai)
        }
        huiyuan_list.append(huiyuan_detail)
    return JsonResponse({"huiyuan":huiyuan_list,"pagenum":int(page)+1,"total":huiyuan_len})

#理发师获取用户会员列表
@csrf_exempt
def lifashi_show_huiyuan(request):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    lifashi_id = datagetter.get("lifashi_id")
    page = datagetter.get('page')
    pagesize = datagetter.get('pagesize')
    start = page*6
    huiyuan_list = []
    try:
        huiyuan_len = huiyuan.objects.filter(lifashi=lifashi_id).count()
    except:
        huiyuan_len = 0
    Huiyuan = huiyuan.objects.filter(lifashi=lifashi_id).order_by('-id')[int(start):int(start+pagesize)]
    for item in Huiyuan:
        i_yonghu = item.yonghu
        try:
            i_yonghu_tupian = tupian.objects.get(tupianlaiyuan_id=i_yonghu.id, tupianleixing=3)
            yonghu_tupian_src = i_yonghu_tupian.src.name
        except:
            yonghu_tupian_src = "../../image/lifashi1.png"
        try:
            xiaofei_count = jiesuandingdan.objects.get(yonghu=i_yonghu.id,lifashi=lifashi_id).count()
        except:
            xiaofei_count = 0
        huiyuan_detail = {
            'id':item.id,"yonghu_id":i_yonghu.id,"yonghu_name":i_yonghu.yonghuming,"xiaofei_count":xiaofei_count,"lifashi_image":yonghu_tupian_src
            ,"zhuangtai":item.zhuangtai }
        huiyuan_list.append(huiyuan_detail)
    return JsonResponse({"huiyuan":huiyuan_list,"pagenum":int(page)+1,"total":huiyuan_len})


#发送消息 0-用户 1-理发师
@csrf_exempt
def add_xiaoxi(request,shenfeng):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    from_id = int(datagetter.get('from_id'))
    to_id = int(datagetter.get('to_id'))
    content = datagetter.get('content')
    print(from_id)
    try:
        if(shenfeng==0):
                the_from = yonghu.objects.get(id=from_id)
                the_to = lifashi.objects.get(id=to_id)
                the_xiaoxi = xiaoxi(from_id=the_from,to_id=the_to,content=content)
        else:
                the_from = lifashi.objects.get(id=from_id)
                the_to = yonghu.objects.get(id=to_id)
                the_xiaoxi = lifashi_xiaoxi(from_id=the_from,to_id=the_to,content=content)
        the_xiaoxi.save()
        return JsonResponse({"status":1,"msg":"发送成功"})
    except:
        return JsonResponse({"status":0,"msg":"发送失败"})

#获取聊天信息 0-用户 1-理发师
@csrf_exempt
def show_xiaoxi(request,shenfeng):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    from_id = datagetter.get('from_id')
    to_id = datagetter.get('to_id')
    self_count = int(datagetter.get('self_count'))
    other_count = int(datagetter.get('other_count'))
    if(shenfeng==0):
        # 获取用户发送的消息
        the_from = yonghu.objects.get(id=from_id)
        the_to = lifashi.objects.get(id=to_id)
        xiaoxi_list = xiaoxi.objects.filter(from_id=the_from,to_id=the_to)[self_count:]
        self_count = xiaoxi.objects.filter(from_id=the_from,to_id=the_to)[self_count:].count() + self_count
        xiaoxi_new_list1 = []
        for i_xiaoxi in xiaoxi_list:
            xiaoxi_detail = {"pubtime":i_xiaoxi.pubtime,"content":i_xiaoxi.content,"self":True}
            xiaoxi_new_list1.append(xiaoxi_detail)
        #获取理发师 发送的消息
        the_from = lifashi.objects.get(id=to_id)
        the_to = yonghu.objects.get(id=from_id)
        xiaoxi_list = lifashi_xiaoxi.objects.filter(from_id=the_from,to_id=the_to)[other_count:]
        other_count = lifashi_xiaoxi.objects.filter(from_id=the_from,to_id=the_to)[other_count:].count() + other_count
        xiaoxi_new_list2 = []
        for i_xiaoxi in xiaoxi_list:
            xiaoxi_detail = {"pubtime":i_xiaoxi.pubtime,"content":i_xiaoxi.content,"self":False}
            xiaoxi_new_list2.append(xiaoxi_detail)
        new_list = xiaoxi_new_list1+xiaoxi_new_list2
    if(shenfeng==1):
            # 获取用户发送的消息
        the_from = yonghu.objects.get(id=to_id)
        the_to = lifashi.objects.get(id=from_id)
        xiaoxi_list = xiaoxi.objects.filter(from_id=the_from,to_id=the_to)[other_count:]
        other_count = xiaoxi.objects.filter(from_id=the_from,to_id=the_to)[other_count:].count() + other_count
        xiaoxi_new_list1 = []
        for i_xiaoxi in xiaoxi_list:
            xiaoxi_detail = {"pubtime":i_xiaoxi.pubtime,"content":i_xiaoxi.content,"self":False}
            xiaoxi_new_list1.append(xiaoxi_detail)
        #获取理发师 发送的消息
        the_from = lifashi.objects.get(id=from_id)
        the_to = yonghu.objects.get(id=to_id)
        xiaoxi_list = lifashi_xiaoxi.objects.filter(from_id=the_from,to_id=the_to)[self_count:]
        self_count = lifashi_xiaoxi.objects.filter(from_id=the_from,to_id=the_to)[self_count:].count() + self_count
        xiaoxi_new_list2 = []
        for i_xiaoxi in xiaoxi_list:
            xiaoxi_detail = {"pubtime":i_xiaoxi.pubtime,"content":i_xiaoxi.content,"self":True}
            xiaoxi_new_list2.append(xiaoxi_detail)
        new_list = xiaoxi_new_list1+xiaoxi_new_list2
    return JsonResponse({"xiaoxi_list":new_list,"self_count":self_count,"other_count":other_count})

#获取聊天列表 0-用户 1-理发师
@csrf_exempt
def get_xiaoxi_list(request,shenfeng):
    if request.method == "POST":
        datagetter = request.POST
    else:
        datagetter = request.GET
    yonghu_id = datagetter.get('yonghu_id')
    print(yonghu_id)
    if(shenfeng==0):
        xiaoxi_list = xiaoxi.objects.filter(from_id=yonghu_id)
    else:
        xiaoxi_list = lifashi_xiaoxi.objects.filter(from_id=yonghu_id)
    to_list_id = []
    for i_xiaoxi in xiaoxi_list:
        to_id = i_xiaoxi.to_id.id
        to_list_id.append(to_id)
        to_list_id = list(set(to_list_id))
    detail_list = []
    for i_id in to_list_id:
        if(shenfeng==0):
            try:
                to_img_src =  tupian.objects.get(tupianlaiyuan_id=i_id,tupianleixing=1)
            except:
                to_img_src = "../../image/默认头像.png"
        else:
            try:
                to_img_src =  tupian.objects.get(tupianlaiyuan_id=i_id,tupianleixing=3)
            except:
                to_img_src = "../../image/默认头像.png"
        to_detail = {"to_id":i_id,"to_img":to_img_src}
        detail_list.append(to_detail)
    return JsonResponse({"status":1,"list":detail_list})



