from django.db import models

# Create your models here.

class lifadian(models.Model):#理发店
	dianzhuming = models.CharField(max_length=30)
	dianzhushenfenzheng = models.CharField(max_length=18)
	dianzhulianxi = models.CharField(max_length=20)
	dianming = models.CharField(max_length=30)
	dizhi = models.CharField(max_length=30)

class lifashi(models.Model):#理发师
	lifadian = models.ForeignKey(lifadian,on_delete=models.CASCADE,null=True)
	xingming = models.CharField(max_length=30)
	yonghuming = models.CharField(max_length=30)
	mima = models.CharField(max_length=30)
	lianxidianhua = models.CharField(max_length=30,unique=True)
	xingbie = models.CharField(max_length=1,choices=(('1','男'),('0','女')))

class wuzi(models.Model):#物资
	lifadianID = models.ForeignKey(lifadian,on_delete=models.CASCADE)
	wuziming = models.CharField(max_length=30)
	wuzileixing = models.CharField(max_length=30)
	shengyuliang = models.IntegerField()
	shangcijinhuo = models.DateTimeField()

class lifashizhuang(models.Model):#理发师状态
	lifashi = models.ForeignKey(lifashi,on_delete=models.CASCADE)
	zhuangtai = models.CharField(max_length=1,choices=((1,'繁忙'),(0,'空闲')))
	xiayikongxian = models.DateTimeField()


class yonghu(models.Model): #用户
	yonghuming = models.CharField(max_length=30)
	mima = models.CharField(max_length=30)
	xingming =models.CharField(max_length=30)
	xingbie = models.CharField(max_length=1,choices=(('1','男'),('0','女')))
	lianxidianhua = models.CharField(max_length=30,unique=True)

class dingdan(models.Model):
	lifadian = models.ForeignKey(lifadian,on_delete=models.CASCADE)
	yonghu = models.ForeignKey(yonghu,on_delete=models.CASCADE)
	lifashi = models.ForeignKey(lifashi,on_delete=models.CASCADE)
	fuwuxiang = models.CharField(max_length=30)

class yuyuedingdan(dingdan):
	yuyuekaishi = models.DateTimeField()
	yuyuexiaohao = models.TimeField()
	gujifeiyong = models.FloatField()

class jiesuandingdan(dingdan):
	jieshushijian = models.DateTimeField()
	shijifeiyong = models.FloatField()
	shifouzhifu = models.BooleanField(default=0)

class pingjia(models.Model):
	yonghu = models.ForeignKey(yonghu,on_delete=models.CASCADE)
	dingdan = models.ForeignKey(dingdan,on_delete=models.CASCADE)
	pingfen = models.IntegerField()
	pingjia = models.CharField(max_length=100)

class renyuananpai(models.Model):
	lifashi = models.ForeignKey(lifashi,on_delete=models.CASCADE)
	lifadian = models.ForeignKey(lifadian,on_delete=models.CASCADE)
	anpaidingdan = models.ForeignKey(dingdan,on_delete=models.CASCADE)


class jixiaotongji(models.Model):
	lifashi = models.ForeignKey(lifashi, on_delete=models.CASCADE)
	lifadian = models.ForeignKey(lifadian, on_delete=models.CASCADE)
	fuwuleixing = models.CharField(max_length=30)
	xiaofeizongliang = models.FloatField
	zonghepingfen = models.FloatField()