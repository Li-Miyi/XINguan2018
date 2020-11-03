from django.urls import path
<<<<<<< HEAD
from django.conf.urls.static import static
from django.conf import settings
=======

>>>>>>> 30db17da3434f47dc14955491f0991283dadec82
from . import  views
from . import  view
app_name = 'jianyue'
urlpatterns = [
    path(r'zhuce/',view.lifashi_yonghu.zhuce,name ='yonghulifashizhuce'),
    path(r'denglu/',view.lifashi_yonghu.denglu,name="YonghuLifashidenglu"),
    path(r"xiugai/",view.lifashi_yonghu.xiugai,name="YonghuLifashixiugai"),
<<<<<<< HEAD
    path(r'liebiao/',view.lifashi_yonghu.liebiao,name="YonghuLifashiliebiao"),
    path(r'lifashidetail/',view.lifashi_yonghu.lifashi_detail,name="YonghuLifashidetail"),

=======
>>>>>>> 30db17da3434f47dc14955491f0991283dadec82
    #理发店管理操作
    path(r'lifadian/',view.lifadian.shouye,name = "lifadian_shouye"),
    path(r'lifadian/zhuce/',view.lifadian.zhuce,name = "lifadian_zhuceyanzheng"),
    path(r'lifadian/denglu/',view.lifadian.denglu,name = "lifadian_degnluyanzheng"),
    path(r'lifadian/xiugai/',view.lifadian.xiugai,name="lifadian_xiugai"),
<<<<<<< HEAD
    #理发店图片
path('lifadian/xiangze/', view.lifadian.xiangce, name='lifadian_tupianzengjia'),
    #理发店个人界面
    path(r'lifadian/<int:dianzhulianxi>/',view.lifadian.geren,name="lifadian_geren"),
    #物资
=======
    #理发店个人界面
    path(r'lifadian/<int:dianzhulianxi>/',view.lifadian.geren,name="lifadian_geren"),
>>>>>>> 30db17da3434f47dc14955491f0991283dadec82
    path(r"lifadian/<int:dianzhulianxi>/wuzi/",view.lifadian.wuzi,name="lifadian_wuzi"),
    path(r"lifadian/<int:dianzhulianxi>/wuzi/zengjia.html",view.lifadian.wuzi_zengjia,name="lifadian_wuzizengjia"),
    path(r"lifadian/<int:dianzhulianxi>/wuzi/shanchu/",view.lifadian.wuzi_shanchu,name="lifadian_wuzishanchu"),
    path(r"lifadian/<int:dianzhulianxi>/wuzi/xiaohao/",view.lifadian.wuzi_xiaohao,name="lifadian_wuzixiaohao"),
<<<<<<< HEAD
    #理发师
    path(r"lifadian/<int:dianzhulianxi>/lifashi/",view.lifadian.jixiao,name="lifashi_jixiao"),
    path(r"lifadian/<int:dianzhulianxi>/lifashi/anpai/",view.lifadian.anpai,name="lifashi_anpai"),
    #地址借用
    path(r"lifadian/<int:dianzhulianxi>/dizhi/<slug:zhuangtai>",view.lifadian.dizhi,name="dizhi"),
    path(r"lifadian/<int:dianzhulianxi>/dizhi/chexiao/",view.lifadian.dizhi_chexiao,name="dizhi_chexiao"),
    path(r"lifadian/<int:dianzhulianxi>/dizhi/fankui/",view.lifadian.dizhi_fankui,name="dizhi_fankui"),
    path('',views.app_index,name ='moreng1')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    path('',views.app_index,name ='moreng1')

]
>>>>>>> 30db17da3434f47dc14955491f0991283dadec82
