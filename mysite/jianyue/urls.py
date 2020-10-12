from django.urls import path

from . import views

app_name = 'jianyue'
urlpatterns = [
    path(r'zhuce/',views.zhuce,name ='zhuce')
]