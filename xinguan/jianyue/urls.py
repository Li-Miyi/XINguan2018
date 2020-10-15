from django.urls import path

from . import  views
from . import  view
app_name = 'jianyue'
urlpatterns = [
    path(r'zhuce/',view.lifashi_yonghu.zhuce,name ='yonghulifashizhuce'),
    path(r'denglu/',view.lifashi_yonghu.denglu,name="YonghuLifashidenglu"),
    path(r"xiugai/",view.lifashi_yonghu.xiugai,name="YonghuLifashixiugai"),
    #理发店管理操作
    path(r'lifadian/',view.lifadian.shouye,name = "lifadian_shouye"),
    path(r'lifadian/zhuce/',view.lifadian.zhuce,name = "lifadian_zhuceyanzheng"),
    path(r'lifadian/denglu/',view.lifadian.denglu,name = "lifadian_degnluyanzheng"),
    path(r'lifadian/xiugai/',view.lifadian.xiugai,name="lifadian_xiugai"),
    #理发店个人界面
    path(r'lifadian/<int:dianzhulianxi>/',view.lifadian.geren,name="lifadian_geren"),
    path(r"lifadian/<int:dianzhulianxi>/wuzi/",view.lifadian.wuzi,name="lifadian_wuzi"),
    path(r"lifadian/<int:dianzhulianxi>/wuzi/zengjia.html",view.lifadian.wuzi_zengjia,name="lifadian_wuzizengjia"),
    path(r"lifadian/<int:dianzhulianxi>/wuzi/shanchu/",view.lifadian.wuzi_shanchu,name="lifadian_wuzishanchu"),
    path(r"lifadian/<int:dianzhulianxi>/wuzi/xiaohao/",view.lifadian.wuzi_xiaohao,name="lifadian_wuzixiaohao"),
    path('',views.app_index,name ='moreng1')

]
