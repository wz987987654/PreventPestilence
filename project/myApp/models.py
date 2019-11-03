from django.contrib.auth.models import AbstractUser
from django.db import models


'''
from myApp.models import Grades,Students
from django.utils import timezone
from datetime import *
'''
# Create your models here.
# 用户类（合并auth user）
class Users(AbstractUser):
    username=models.CharField(verbose_name="用户名",max_length=20,default="admin") # 用户名
    #login_id=models.IntegerField(verbose_name="登陆id")   #用户登陆id
    #editable 加上去就不显示
    password=models.CharField(verbose_name="登陆密码",editable=False,max_length=10000,default="12345678") # 用户密码
    user_phone=models.CharField(verbose_name="手机号码",max_length=20,default=1) #电话
    user_mail=models.CharField(verbose_name="邮箱",max_length=20,default=1) # 邮箱
    isInform=models.BooleanField(verbose_name="是否推送最新通知",default=True) # 是否通知
    isMail=models.BooleanField(verbose_name="是否发邮件",default=True) # 是否邮件
    #user_type=models.CharField(max_length=20) # 用户类型
    USER_TYPE_LIST = (
        (1, 'user'),
        (2, 'admin'),
    )
    user_type = models.IntegerField(verbose_name="用户类型",choices=USER_TYPE_LIST, default=1)
    power_type=models.CharField(verbose_name="用户权限",max_length=20) # 用户权限
    creator_id=models.IntegerField(verbose_name="创建者id",default=0)# 创建者id
    update_id=models.IntegerField(verbose_name="更新者id",default=0) #更新者id
    lastTime = models.DateTimeField(verbose_name="最后更新时间",auto_now=True)
    createTime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    isDel=models.BooleanField(verbose_name="是否能删除",default=True)# 是否删除
    # fatheruser_id=models.IntegerField()#父亲用户ID
    #relevanceKey=models.CharField(max_length=20)#关联Key
    img = models.ImageField(verbose_name="头像",null=True, blank=True, upload_to="upload")# 上传图片

    USERNAME_FIELD = 'id'

    class Meta:
        #指定表名
        db_table = 'myApp_users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name



# 通知类
class Inform(models.Model):
    inform_id=models.IntegerField(verbose_name="通知id", default=1)
    content=models.CharField(verbose_name="内容",max_length=20)
    focus_id=models.IntegerField(verbose_name="关注用户的id")
    isSend=models.BooleanField(verbose_name="是否收到",default=True)
    creator_id = models.IntegerField(verbose_name="创建者id", default=1)  # 创建者id
    update_id = models.IntegerField(verbose_name="更新者id", default=1)  # 更新者id
    lastTime = models.DateTimeField(verbose_name="最后更新时间", auto_now=True)
    createTime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    isDel = models.BooleanField(verbose_name="是否能删除", default=True)
    class Meta:
        #verbose_name = '用户管理'
        verbose_name_plural = '通知管理'
# 原始数据类
class Rawdata(models.Model):
    date=models.DateTimeField(verbose_name="时间")
    address=models.CharField(verbose_name="地址",max_length=20)
    temperature=models.FloatField(verbose_name="温度",max_length=20)
    humidity=models.FloatField(verbose_name="湿度",max_length=20)
    atmospheric=models.FloatField(verbose_name="气压",max_length=20)
    precipitation=models.IntegerField(verbose_name="降水")
    sunshine=models.IntegerField(verbose_name="日照")
    wind=models.FloatField(verbose_name="风力",max_length=20)
    aqi=models.IntegerField(verbose_name="空气质量")
    pm2=models.FloatField(verbose_name="pm2.5",max_length=20)
    pm10=models.FloatField(verbose_name="pm10",max_length=20)
    SO2=models.FloatField(verbose_name="SO2",max_length=20)
    CO=models.FloatField(verbose_name="CO",max_length=20)
    NO2=models.FloatField(verbose_name="NO2",max_length=20)
    O3=models.FloatField(verbose_name="O3",max_length=20)
    incidence=models.FloatField(verbose_name="发病数",max_length=20)
    class Meta:
        verbose_name_plural = '天气、污染原始数据'
# 预测类
class Forecast(models.Model):
    #pre_id=models.IntegerField(default=1)
    pre_date=models.DateTimeField(verbose_name="待预测日期",auto_now_add=True)
    pre_type=models.CharField(verbose_name="类型",max_length=20)
    #isDel=models.BooleanField(verbose_name="是否可以删除",default=True)
    real_result = models.CharField(verbose_name="实际结果", max_length=20)
    pre_result=models.CharField(verbose_name="预测结果",max_length=20)
    # creator_id=models.IntegerField(verbose_name="创建者id",default=1)# 创建者id
    # update_id=models.IntegerField(verbose_name="更新者id",default=1) #更新者id
    lastTime = models.DateTimeField(verbose_name="最后更新时间",auto_now=True)
    createTime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    class Meta:
        verbose_name_plural = '预测数据'

# 通知收藏类
class Collect(models.Model):
    collect_id=models.IntegerField()
    user_id = models.ForeignKey('Users',on_delete=models.CASCADE)
    inform_id=models.ForeignKey('Inform',on_delete=models.CASCADE)
    creator_id = models.IntegerField(verbose_name="创建者id", default=1)  # 创建者id
    update_id = models.IntegerField(verbose_name="更新者id", default=1)  # 更新者id
    lastTime = models.DateTimeField(verbose_name="最后更新时间", auto_now=True)
    createTime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    isDel = models.BooleanField(verbose_name="是否能删除", default=True)
    class Meta:
        #verbose_name = '用户管理'
        verbose_name_plural = '收藏管理'

# 留言类
class Message(models.Model):
    message_id=models.IntegerField(verbose_name="留言id",default=1)
    content=models.CharField(verbose_name="留言内容",max_length=2000)
    user_id=models.ForeignKey('Users',on_delete=models.CASCADE)
    #inform_id=models.ForeignKey('Inform',on_delete=models.CASCADE)
    isShow=models.BooleanField(verbose_name="是否显示",default=True)
    creator_id = models.IntegerField(verbose_name="创建者id", default=1)  # 创建者id
    update_id = models.IntegerField(verbose_name="更新者id", default=1)  # 更新者id
    lastTime = models.DateTimeField(verbose_name="最后更新时间", auto_now=True)
    createTime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    isDel = models.BooleanField(verbose_name="是否能删除", default=True)
    class Meta:
        #verbose_name = '用户管理'
        verbose_name_plural = '留言管理'

class Jurisdiction(models.Model):
    root_id=models.IntegerField(verbose_name="权限id",default=1)

    ROOT_NAME_LIST = (
        (1, '预测发病数'),
        (2, '爬取数据'),
        (3, '保存数据'),
    )

    root_name=models.IntegerField(verbose_name="权限名", choices=ROOT_NAME_LIST, default=1)
    creator_id = models.IntegerField(verbose_name="创建者id", default=1)  # 创建者id
    update_id = models.IntegerField(verbose_name="更新者id", default=1)  # 更新者id
    lastTime = models.DateTimeField(verbose_name="最后更新时间", auto_now=True)
    createTime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    isDel = models.BooleanField(verbose_name="是否能删除", default=True)
    class Meta:
        #verbose_name = '用户管理'
        verbose_name_plural = '权限管理'



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
    class Meta:
        #verbose_name = '用户管理'
        verbose_name_plural = '测试1'

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
    class Meta:
        #verbose_name = '用户管理'
        verbose_name_plural = '测试2'