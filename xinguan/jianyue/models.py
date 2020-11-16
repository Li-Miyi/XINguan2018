from django.db import models


# Create your models here.
class lifadian(models.Model):  # 理发店
    shenfenzheng = models.CharField(max_length=18, unique=True)
    dianzhuming = models.CharField(max_length=30)
    dianzhulianxi = models.CharField(max_length=20, unique=True)
    dianming = models.CharField(max_length=30)
    mima = models.CharField(max_length=30)


class dizhi(models.Model):
    lifadian = models.ForeignKey(lifadian,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    lng = models.FloatField()
    lat = models.FloatField()
    comprehension = models.IntegerField()


class lifashi(models.Model):  # 理发师
    lifadian = models.ForeignKey(lifadian, on_delete=models.CASCADE, null=True)
    shenfenzheng = models.CharField(max_length=18, null=True, unique=True)
    xingming = models.CharField(max_length=30)
    yonghuming = models.CharField(max_length=30)
    mima = models.CharField(max_length=30)
    lianxidianhua = models.CharField(max_length=30, unique=True)
    xingbie = models.CharField(max_length=1, choices=(('1', '男'), ('0', '女')))


class wuzi(models.Model):  # 物资
    lifadian = models.ForeignKey(lifadian, on_delete=models.CASCADE)
    wuziming = models.CharField(max_length=30)
    wuzileixing = models.CharField(max_length=30)
    shengyuliang = models.IntegerField(default=0)
    jinhuoshijian = models.DateTimeField()

    class Meta:
        unique_together = ('wuziming', 'wuzileixing', 'lifadian')

class yonghu(models.Model):  # 用户
    yonghuming = models.CharField(max_length=30)
    mima = models.CharField(max_length=30)
    xingming = models.CharField(max_length=30)
    xingbie = models.CharField(max_length=1, choices=(('1', '男'), ('0', '女')))
    lianxidianhua = models.CharField(max_length=30, unique=True)

def upload_to(instance,filename):
    tupianlianyuan_id = instance.tupianlaiyuan_id
    tupianleixing = ["lifadian","lifashi","faxing"][int(instance.tupianleixing)]
    return '/'.join([tupianleixing,str(tupianlianyuan_id),filename])

class tupian(models.Model):
    tupianlaiyuan_id = models.CharField(max_length=700)
    src = models.ImageField(upload_to=upload_to)
    tupianleixing = models.CharField(max_length=1, choices=(('0', '理发店'), ('1', '理发师'),('2','发型'),('3','用户')))

"""服务与理发师理发店对应"""


class fuwu(models.Model):
    lifashi = models.ForeignKey(lifashi, on_delete=models.CASCADE)
    jiage = models.IntegerField()
    fuwumingcheng = models.CharField(max_length=30)
    leixing = models.CharField(max_length=1, choices=(('1', '洗吹'), ('2', '烫发'), ('3', '染发'), ('4', '剪发'), ('5', '护理')))

    class Meta:
        unique_together = ('fuwumingcheng', 'lifashi')


class faxing(models.Model):  # 发型
    lifashi = models.ForeignKey(lifashi, on_delete=models.CASCADE)
    faxingming = models.CharField(max_length=30)
    leixing = models.CharField(max_length=1, choices=(('1', '短发'), ('2', '烫发'), ('3', '长发'), ('4', '染发')))
    beizhu = models.CharField(max_length=700)


class dingdan(models.Model):
    lifadian = models.ForeignKey(lifadian, on_delete=models.CASCADE)
    yonghu = models.ForeignKey(yonghu, on_delete=models.CASCADE)
    lifashi = models.ForeignKey(lifashi, on_delete=models.CASCADE)
    fuwuxiang = models.ForeignKey(fuwu, on_delete=models.CASCADE)


class yuyuedingdan(dingdan):
    yuyuekaishi = models.DateTimeField()
    yuyuexiaohao = models.TimeField(null=True)
    yijieshou = models.BooleanField()


class jiesuandingdan(dingdan):
    jieshushijian = models.DateTimeField()
    shijifeiyong = models.FloatField()
    shifouzhifu = models.BooleanField(default=0)

class pingjia(models.Model):
    yonghu = models.ForeignKey(yonghu, on_delete=models.CASCADE)
    dingdan = models.ForeignKey(dingdan, on_delete=models.CASCADE)
    pingfen = models.IntegerField(default=5)
    pingjia = models.CharField(max_length=100)


class jishiqitadizhi(models.Model):  # 理发师与地址的即时关系
    lifashi = models.ForeignKey(lifashi, on_delete=models.CASCADE)
    lifadian = models.ForeignKey(lifadian, on_delete=models.CASCADE)
    shenqingshijian = models.DateTimeField()
    zhuangtai = models.CharField(max_length=1, choices=(('1', '已批准'), ('0','未批准')))
    class Meta:
        unique_together = ('lifadian', 'lifashi')

class shoucang(models.Model):
    beishoucang_id = models.CharField(max_length=700)
    yonghu = models.ForeignKey(yonghu,on_delete=models.CASCADE)
    tupianleixing = models.CharField(max_length=1, choices=(('0', '理发店'), ('1', '理发师'),('2','服务')))

    class Meta:
        unique_together = ('beishoucang_id', 'yonghu','tupianleixing')
