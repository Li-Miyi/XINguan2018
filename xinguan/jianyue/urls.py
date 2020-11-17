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
    path(r"jishidizhi/add", view.lifashi_yonghu.jishiqitadizhi, name="YonghuLifaJishidizhiAdd"),
    # 用户查看不同订单
    path(r"YonghuDingdan/<int:zhuangtai_id>", view.lifashi_yonghu.getYonghuDingdan, name="YonghuDingdan"),
    #理发师
    path(r"lifashi/yuyue_shijian", view.lifashi_yonghu.yuyue_shijian, name="LifashiYuyueShijianList"),
    # 服务列表页
    path(r"fuwuliebiao/", view.lifashi_yonghu.fuwuliebiao, name="fuwuliebiao"),
    #用户收藏
    path(r'shoucang/add/<int:shoucangleixing>', view.lifashi_yonghu.yonghu_shoucang_add, name='YonghuAddShoucang'),
    path(r'shoucang/delete/<int:shoucangleixing>', view.lifashi_yonghu.yonghu_shoucang_delete, name='YonghuDeleteShoucang'),
    path(r'shoucang/show/<int:shoucangleixing>', view.lifashi_yonghu.yonghu_shoucang_show,
         name='YonghuShowShoucang'),
    # 对图片的操作
    path(r'tupian/show/<int:tupianleixing>/<int:tupianlaiyuan_id>',views.tupian_show,name="YonghuLifashitupianshow"),
    path(r'tupian/delete/<path:tupianlujing>',views.tupian_delete,name="YonghuLifashitupiandelete"),
    path(r'tupian/add/<int:tupianleixing>/<int:tupianlaiyuan_id>',views.tupian_add,name="YonghuLifashitupianadd"),
    # 理发店管理操作
    path(r'lifadian/', view.lifadian.shouye, name="lifadian_shouye"),
    path(r'lifadian/zhuce/', view.lifadian.zhuce, name="lifadian_zhuceyanzheng"),
    path(r'lifadian/denglu/', view.lifadian.denglu, name="lifadian_degnluyanzheng"),
    path(r'lifadian/xiugai/', view.lifadian.xiugai, name="lifadian_xiugai"),
    # 小程序理发师端
    path(r"getOKDingdan/", view.lifashi_yonghu.getOKDingdan, name="LifashigetOKDingdan"),
    path(r"getLifadianName/", view.lifashi_yonghu.getLifadianName, name="LifashiZhuce"),
    path(r"getLifadian/<int:zhuangtaiid>/", view.lifashi_yonghu.getLifadian, name="LifashiGetLifadian"),
    path(r"thelifashiDetail/", view.lifashi_yonghu.lifashiDetail, name="LifashiDetail"),
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
    path('', views.app_index, name='moreng1')

    ]
