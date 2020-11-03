from django.db import models

# Create your models here.
class lifadian(models.Model):#理发店
	shenfenzheng = models.CharField(max_length=18, unique=True)
	dianzhuming = models.CharField(max_length=30)
	dianzhulianxi = models.CharField(max_length=20,unique=True)
	dianming = models.CharField(max_length=30)
	dizhi = models.CharField(max_length=30)
	mima = models.CharField(max_length=30)

class lifashi(models.Model):#理发师
	lifadian = models.ForeignKey(lifadian,on_delete=models.CASCADE,null=True)
	shenfenzheng = models.CharField(max_length=18,null=True,unique=True)
	xingming = models.CharField(max_length=30)
	yonghuming = models.CharField(max_length=30)
	mima = models.CharField(max_length=30)
	lianxidianhua = models.CharField(max_length=30,unique=True)
	xingbie = models.CharField(max_length=1,choices=(('1','男'),('0','女')))

class wuzi(models.Model):#物资
	lifadian = models.ForeignKey(lifadian,on_delete=models.CASCADE)
	wuziming = models.CharField(max_length=30)
	wuzileixing = models.CharField(max_length=30)
	shengyuliang = models.IntegerField(default=0)
	jinhuoshijian = models.DateTimeField()
	class Meta:
		unique_together = ('wuziming','wuzileixing','lifadian')


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



class jixiaotongji(models.Model):
	lifashi = models.ForeignKey(lifashi, on_delete=models.CASCADE)
	lifadian = models.ForeignKey(lifadian, on_delete=models.CASCADE)
	fuwuleixing = models.CharField(max_length=30)
	xiaofeizongliang = models.FloatField
	zonghepingfen = models.FloatField()

class tupian(models.Model):
	url = models.CharField(max_length=500,unique=True)
	lifadian = models.ForeignKey(lifadian,on_delete=models.CASCADE)

"""服务与理发师理发店对应"""
class fuwu(models.Model):
	lifashi = models.ForeignKey(lifashi,on_delete=models.CASCADE)
	jiage = models.IntegerField()
	pingjia = models.FloatField(default=5)
	fuwumingcheng = models.CharField(max_length=30)
	leixing = models.CharField(max_length=1, choices=(('1', '洗吹'), ('2', '烫发'), ('3', '染发'), ('4', '剪发'), ('5', '护理')))

	class Meta:
		unique_together = ('fuwumingcheng','lifashi')

class faxing(models.Model): #发型
	lifashi = models.ForeignKey(lifashi,on_delete=models.CASCADE)
	tupian = models.CharField(max_length=30)
	leixing = models.CharField(max_length=1,choices=(('1','短发'),('2','烫发'),('3','长发'),('4','染发')))
	beizhu = models.CharField(max_length=700)

class dingdan(models.Model):
	lifadian = models.ForeignKey(lifadian, on_delete=models.CASCADE)
	yonghu = models.ForeignKey(yonghu, on_delete=models.CASCADE)
	lifashi = models.ForeignKey(lifashi, on_delete=models.CASCADE)
	fuwuxiang = models.ForeignKey(fuwu, on_delete=models.CASCADE)

class yuyuedingdan(dingdan):
	yuyuekaishi = models.DateTimeField()
	yuyuexiaohao = models.TimeField()
	gujifeiyong = models.FloatField()

class jiesuandingdan(dingdan):
	jieshushijian = models.DateTimeField()
	shijifeiyong = models.FloatField()
	shifouzhifu = models.BooleanField(default=0)

class renyuananpai(models.Model):
	lifashi = models.ForeignKey(lifashi,on_delete=models.CASCADE)
	lifadian = models.ForeignKey(lifadian,on_delete=models.CASCADE)
	anpaidingdan = models.ForeignKey(dingdan,on_delete=models.CASCADE)




class pingjia(models.Model):
	yonghu = models.ForeignKey(yonghu,on_delete=models.CASCADE)
	dingdan = models.ForeignKey(dingdan,on_delete=models.CASCADE)
	pingfen = models.IntegerField()
	pingjia = models.CharField(max_length=100)
