from django.db import models
'''
from myApp.models import Grades,Students
from django.utils import timezone
from datetime import *
'''
# Create your models here.
class Users(models.Model):
    user_name=models.CharField(verbose_name="用户名",max_length=20) # 用户名
    login_id=models.IntegerField(verbose_name="登陆id")   #用户登陆id
    #editable 加上去就不显示
    user_password=models.CharField(verbose_name="登陆密码",editable=False,max_length=20,default="12345678") # 用户密码
    tele=models.CharField(verbose_name="手机号码",max_length=20) #电话
    mail=models.CharField(verbose_name="邮箱",max_length=20) # 邮箱
    isInform=models.BooleanField(verbose_name="是否通知",default=True) # 是否通知
    isMail=models.BooleanField(verbose_name="是否发邮件",default=True) # 是否邮件
    #user_type=models.CharField(max_length=20) # 用户类型
    USER_TYPE_LIST = (
        (1, 'user'),
        (2, 'admin'),
    )
    user_type = models.IntegerField(verbose_name="用户类型",choices=USER_TYPE_LIST, default=1)
    power_type=models.CharField(verbose_name="用户权限",max_length=20) # 用户权限
    creator_id=models.IntegerField(verbose_name="创建者id")# 创建者id
    update_id=models.IntegerField(verbose_name="更新者id") #更新者id
    lastTime = models.DateTimeField(verbose_name="最后更新时间",auto_now=True)
    createTime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)

    isDel=models.BooleanField(verbose_name="是否删除",default=True)# 是否删除
    # fatheruser_id=models.IntegerField()#父亲用户ID
    #relevanceKey=models.CharField(max_length=20)#关联Key
    img = models.ImageField(verbose_name="头像",null=True, blank=True, upload_to="upload")# 上传图片

    class Meta:
        #verbose_name = '用户管理'
        verbose_name_plural = '用户管理'

class Rawdata(models.Model):
    date=models.DateTimeField(verbose_name="时间")
    address=models.CharField(max_length=20)
    temperature=models.FloatField(max_length=20)
    humidity=models.FloatField(max_length=20)
    atmospheric=models.FloatField(max_length=20)
    precipitation=models.IntegerField()
    sunshine=models.IntegerField()
    wind=models.FloatField(max_length=20)
    aqi=models.IntegerField()
    pm2=models.FloatField(max_length=20)
    pm10=models.FloatField(max_length=20)
    SO2=models.FloatField(max_length=20)
    CO=models.FloatField(max_length=20)
    NO2=models.FloatField(max_length=20)
    O3=models.FloatField(max_length=20)
    incidence=models.FloatField(max_length=20)
    class Meta:
        verbose_name_plural = '天气、污染原始数据'

class Forecast(models.Model):
    #pre_id=models.IntegerField(default=1)
    pre_date=models.DateTimeField(verbose_name="待预测日期",auto_now_add=True)
    pre_type=models.CharField(verbose_name="类型",max_length=20)
    isDel=models.BooleanField(verbose_name="是否删除",default=True)
    pre_result=models.CharField(verbose_name="预测结果",max_length=20)
    creator_id=models.IntegerField(verbose_name="创建者id",default=1)# 创建者id
    update_id=models.IntegerField(verbose_name="更新者id",default=1) #更新者id
    lastTime = models.DateTimeField(verbose_name="最后更新时间",auto_now=True)
    createTime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    class Meta:
        verbose_name_plural = '预测数据'

class Grades(models.Model):

    gname=models.CharField(max_length=20)
    gdate=models.DateTimeField()
    ggirlnum=models.IntegerField()
    gboynum=models.IntegerField()
    isDelete=models.BooleanField(default=True)


    def __str__(self):
        # return "%s-%d-%d"%(self.gname,self.ggirlnum,self.gboynum)
        return self.gname
    class Meta:
        db_table="grades"

class StudentsManager(models.Manager):

    def get_queryset(self):
        return super(StudentsManager, self).get_queryset().filter(isDelete=False)

    def createStudent(self,name,age,gender,contend,grade,lastT,createT,isD=False):
       #grade=self.model()#创建一个对象
       #print(type(grade))
        stu=self.model()
        stu.sname=name
        stu.sage=age
        stu.sgender=gender
        stu.scontend=contend
        stu.sgrade=grade
        stu.lastTime=lastT
        stu.createTime=createT
        return  stu

class Students(models.Model):
    # 定义一个类方法创建对象
    @classmethod
    def createStudent(cls, name, age, gender, contend, grade, lastT, createT, isD=False):
        stu = cls(sname=name, sage=age, sgender=gender, scontend=contend, sgrade=grade, lastTime=lastT,
                  createTime=createT, isDelete=isD)
        return stu

    # 自定义模型管理器
    # 当自定义模型管理器objects就不存在了
    stuObj= models.Manager()
    stuObj2= StudentsManager()

    sname = models.CharField(max_length=20)
    sgender = models.BooleanField(default=True)
    sage = models.IntegerField(db_column="age")
    scontend = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    lastTime = models.DateField(auto_now=True)
    createTime = models.DateField( auto_now_add=True)
    # 关联外键
    #sgrade = models.ForeignKey("Grades")
    sgrade=models.ForeignKey('Grades',on_delete=models.CASCADE)
    def  __str__(self):
        return self.sname
    lastTime=models.DateTimeField(auto_now=True)
    createTime=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table="students"
        ordering=['id']
