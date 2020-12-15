from django.urls import path

from . import views
from . import view

app_name = 'jianyue'
urlpatterns = [
    path(r'zhuce/', view.lifashi_yonghu.zhuce, name='yonghulifashizhuce'),
    path(r'denglu/', view.lifashi_yonghu.denglu, name="YonghuLifashidenglu"),
    path(r"xiugai/", view.lifashi_yonghu.xiugai, name="YonghuLifashixiugai"),
    path(r'liebiao/', view.lifashi_yonghu.liebiao, name="YonghuLifashiliebiao"),
    path(r'lifashidetail/', view.lifashi_yonghu.lifashi_detail, name="YonghuLifashidetail"),
    path(r'faxingList/', view.lifashi_yonghu.faxingList, name="YonghuFaxingList"),
    path(r"faxingDetail/", view.lifashi_yonghu.faxingDetail, name="YonghuFaxingDetail"),
    path(r"yonghuDetail/", view.lifashi_yonghu.yonghuDetail, name="YonghuDetail"),
    path(r'getYuyueOrder/', view.lifashi_yonghu.getYuyueOrder, name="YonghuYuyueOrder"),
    path(r"jishidizhi/add", view.lifashi_yonghu.jishidizhi_add, name="YonghuLifaJishidizhiAdd"),
    path(r"jishidizhi/detele", view.lifashi_yonghu.jishidizhi_delete, name="YonghuLifaJishidizhiDelete"),
    path(r"cancelorder/", view.lifashi_yonghu.CancelOrder, name="YonghuCancelOrder"),
    path(r"yonghu/getlifadian/", view.lifashi_yonghu.getLifadian, name="YonghuGetLifadian"),
    path(r"yonghu/zhifu/", view.lifashi_yonghu.zhifu, name="Yonghuzhifu"),
    # 评价
    path(r"setpingjia/", view.lifashi_yonghu.set_pingjia, name="setpingjia"),
    # 用户统计数据
    path(r"tongji/yuedu",view.lifashi_yonghu.tongji_yuedu,name="tongjiyuedu"),
    path(r"tongji/leixing", view.lifashi_yonghu.tongji_leixing, name="tongjileixing"),
    # 理发师统计数据
    path(r"lifashi/tongji/yuedu",view.lifashi_yonghu.lifashi_tongji_yuedu,name="tongjiyuedu"),
    path(r"lifashi/tongji/leixing", view.lifashi_yonghu.lifashi_tongji_leixing, name="tongjileixing"),
    # 用户查看不同订单
    path(r"YonghuDingdan/<int:zhuangtai_id>", view.lifashi_yonghu.getYonghuDingdan, name="YonghuDingdan"),
    #理发师
    path(r"lifashi/yuyue/count/", view.lifashi_yonghu.count_yuyue, name="LifashiYuyueCount"),
    # 服务列表页
    path(r"fuwuliebiao/", view.lifashi_yonghu.fuwuliebiao, name="fuwuliebiao"),
    path(r"fuwuliebiaoxiangqing/",view.lifashi_yonghu.fuwuliebiaoxiangqing,name="fuwuliebiaoxiangqing"),
    #用户收藏
    path(r'shoucang/add/<int:shoucangleixing>', view.lifashi_yonghu.yonghu_shoucang_add, name='YonghuAddShoucang'),
    path(r'shoucang/delete/<int:shoucangleixing>', view.lifashi_yonghu.yonghu_shoucang_delete, name='YonghuDeleteShoucang'),
    path(r'shoucang/show/<int:shoucangleixing>', view.lifashi_yonghu.yonghu_shoucang_show,name='YonghuShowShoucang'),
    #用户社区资讯
    path(r'zixun/add', view.lifashi_yonghu.fabuzixun, name="YonghuAddZixun"),
    path(r'zixun/show', view.lifashi_yonghu.getZixun, name="YonghuGetZixun"),
    path(r'zixun/dianzan', view.lifashi_yonghu.dianzan_zixun, name="YonghuDianzan"),

    # 对图片的操作
    path(r'tupian/show/<int:tupianleixing>/<int:tupianlaiyuan_id>',views.tupian_show,name="YonghuLifashitupianshow"),
    path(r'tupian/delete/<path:tupianlujing>',views.tupian_delete,name="YonghuLifashitupiandelete"),
    path(r'tupian/add/<int:tupianleixing>/<int:tupianlaiyuan_id>',views.tupian_add,name="YonghuLifashitupianadd"),
    path(r'touxiang/update/<int:tupianleixing>/<int:tupianlaiyuan_id>/<path:tupianlujing>', views.touxiang_update, name="touxiangupdate"),
    # 理发店管理操作
    path(r'lifadian/', view.lifadian.shouye, name="lifadian_shouye"),
    path(r'lifadian/zhuce/', view.lifadian.zhuce, name="lifadian_zhuceyanzheng"),
    path(r'lifadian/denglu/', view.lifadian.denglu, name="lifadian_degnluyanzheng"),
    path(r'lifadian/xiugai/', view.lifadian.xiugai, name="lifadian_xiugai"),
    path(r'lifadian/dengchu/',view.lifadian.dengchu,name="lifadian_dengchu"),
    # 小程序理发师端
    path(r"getOKDingdan/", view.lifashi_yonghu.getOKDingdan, name="LifashigetOKDingdan"),
    path(r"lifashi/OKdingdan/show", view.lifashi_yonghu.OKdingdan, name="LifashiOKDingdan"),
    path(r"getLifadianName/", view.lifashi_yonghu.getLifadianName, name="LifashiZhuce"),
    path(r"getLifadian/<int:zhuangtaiid>/", view.lifashi_yonghu.lifashigetLifadian, name="LifashiGetLifadian"),
    path(r"thelifashiDetail/", view.lifashi_yonghu.lifashiDetail, name="LifashiDetail"),
    path(r"lifashi/fuwu/add", view.lifashi_yonghu.fuwu_add, name="LifashiFuwuAdd"),
    path(r"lifashi/fuwu/delete", view.lifashi_yonghu.fuwu_delete, name="LifashiFuwuDelete"),
    path(r"lifashi/yuyue/show", view.lifashi_yonghu.yuyue_show, name="LifashiYuyueShow"),
    path(r"lifashi/yuyue/submit", view.lifashi_yonghu.yuyue_submit, name="LifashiYuyueSubmit"),
    path(r"lifashi/xiugai_lfs/",view.lifashi_yonghu.xiugai_lfs,name="lifashi_xiugai"),
    # 理发店图片
    path('lifadian/<int:dianzhulianxi>/xiangce/', view.lifadian.xiangce, name='lifadian_xiangce'),
    # 理发店个人界面
    path(r'lifadian/<int:dianzhulianxi>/', view.lifadian.geren, name="lifadian_geren"),
    # 物资
    path(r"lifadian/<int:dianzhulianxi>/wuzi/", view.lifadian.wuzi, name="lifadian_wuzi"),
    path(r"lifadian/<int:dianzhulianxi>/wuzi/zengjia.html", view.lifadian.wuzi_zengjia, name="lifadian_wuzizengjia"),
    path(r"lifadian/<int:dianzhulianxi>/wuzi/shanchu/", view.lifadian.wuzi_shanchu, name="lifadian_wuzishanchu"),
    path(r"lifadian/<int:dianzhulianxi>/wuzi/xiaohao/", view.lifadian.wuzi_xiaohao, name="lifadian_wuzixiaohao"),
    # 理发师
    path(r"lifadian/<int:dianzhulianxi>/lifashi/", view.lifadian.jixiao, name="lifashi_jixiao"),
    path(r"lifadian/<int:dianzhulianxi>/lifashi/anpai/", view.lifadian.anpai, name="lifashi_anpai"),
    path(r"lifadian/<int:dianzhulianxi>/lifashi/yuyuedingdan/", view.lifadian.dingdan_getter, name="lifashi_yuyue"),
    path(r"lifadian/<int:dianzhulianxi>/lifashi/fuwu/", view.lifadian.fuwu_getter, name="lifashi_fuwu"),
    # 地址借用
    path(r"lifadian/<int:dianzhulianxi>/dizhi/<slug:zhuangtai>", view.lifadian.dizhi, name="dizhi"),
    path(r"lifadian/<int:dianzhulianxi>/dizhi/chexiao/", view.lifadian.dizhi_chexiao, name="dizhi_chexiao"),
    path(r"lifadian/<int:dianzhulianxi>/dizhi/fankui/", view.lifadian.dizhi_fankui, name="dizhi_fankui"),
    path('', views.app_index, name='moreng1'),
    # 用户找回密码
    path(r"zhaohuimima/<int:shenfen>",view.lifashi_yonghu.fasongyouxiang,name="fasongyongxiang"),
    path(r"checkyanzhengma/<int:shenfen>", view.lifashi_yonghu.checkyanzhengma, name="checkyanzhengma"),
    path(r"xiugaimima/<int:shenfen>", view.lifashi_yonghu.xiugaimima, name="xiugaimima"),
    # 注册密保
    path(r"zhucemibao/", view.lifashi_yonghu.zhucemibao, name="zhucemibao"),
    # 获取密保
    path(r"huoqumibao/", view.lifashi_yonghu.huoqumibao, name="huoqumibao"),
    # 修改密保
    path(r"xiugaimibao/", view.lifashi_yonghu.xiugaimibao, name="xiugaimibao"),
    # 修改密码
    path(r"xiugaimima2/", view.lifashi_yonghu.xiugaimima2, name="xiugaimima")
]
