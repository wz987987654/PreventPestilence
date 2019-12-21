from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from .models import Users
from itsdangerous import TimedJSONWebSignatureSerializer as Serialier
from itsdangerous import SignatureExpired
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os


import re



#注册相关  类视图，清晰请求方式的区分 PUT DELET OPTION ....
class RegisterView(View):
    # 跳转到登陆画面
    def get(self,request):
        return render(request, "myApp/user/register.html")

    #注册处理
    def post(self,request):
        username = request.POST.get("username");
        tel = request.POST.get("tel");
        email = request.POST.get("email");
        password = request.POST.get("password");
        password2 = request.POST.get("password2");
        msg = ""
        rep_dict = dict(tel=tel,username=username,email=email,password=password,password2=password2)
        if (not all([username,email,password,password2,tel])):
            msg="用户输入的信息不能为空"
            rep_dict["msg"] = msg
            return render(request, "myApp/user/register.html",rep_dict)

        #11位  13位  14位 （地域号 + 11位）18360939450 8618360939450  +8618360939450  （只是验证中国的手机号码）
        # if (not re.match(r'^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$',tel)):
        #    return render(request, "myApp/user/register.html",{"msg":"手机号码格式不正确"})

        if (not re.match(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$',email)):
            msg = "邮箱输入错误"
            rep_dict["msg"] = msg
            return render(request, "myApp/user/register.html", rep_dict)

        if (password != password2):
            msg = "两次密码不一致"
            rep_dict["msg"] = msg
            rep_dict.pop("password")
            rep_dict.pop("password2")
            return render(request, "myApp/user/register.html", rep_dict)

        #先要去检查电话是否存在
        user =  authenticate(email=email,user_phone = tel)


        if user is not None:
            msg = "手机号码或者email已经存在，请重新注册。"
            rep_dict["msg"] = msg
            rep_dict.pop("password")
            rep_dict.pop("password2")
            return render(request, "myApp/user/register.html", rep_dict)


        #一定要是使用他自己的这种方式区创建而不是使用Users()去创建--你自己的项目和Django框架的整合
        user = Users.objects.create_user(username,email,password)

        #注册完之后该用户是不能登陆的，只有后段承认之后才可以使用，此处为了方便项目的进行，手动改成1
        user.is_active = 0

        #更新方法
        user.save()

        #发送激活邮件，包含一个激活的链接在（get请求）

        serializer = Serialier(settings.SECRET_KEY, 3600)
        info = {"user_id": user.id}
        serialier_id_token = serializer.dumps(info)
        serialier_id_token = serialier_id_token.decode()

        #定义的发送邮件的方法；异步
        try:
            #测试方法
            #raise Exception("测试")
            send_register_active_email(user.email,user.username,serialier_id_token)
        except Exception as e:
            #print(e)
            #return render(request, "myApp/common/error.html", {"msg": "邮件发送失败，请检查相应配置或者联系管理员","jump_index":"http://127.0.0.1:8000/index/"})
            return render(request, "myApp/index/index.html", {"userName": username})
        return render(request, "myApp/index/index.html", {"userName": username})



# 激活用户视图
class ActiveView(View):
    def get(self,request,token):
        serializer = Serialier(settings.SECRET_KEY, 3600)
        try:
            user_dic = serializer.loads(token)
            id = user_dic["user_id"]
            user = Users.objects.get(id=id)
            user.is_active = 1
            user.save()
            return redirect(reversed('login'))
        except SignatureExpired as se:
            return HttpResponse("激活信息已经过期")


#登陆
class Login(View):
    def get(self,request):
        return render(request, "myApp/user/login.html")
    def post(self,request):
        print("aaa")
        # 1 画面输入项目的检查
        tel = request.POST.get("tel")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        cb1 = request.POST.get("cb1")

        # 1.1 输入项目不能为空
        rep_dict = dict(tel=tel, email=email, password=password, password2=password2)

        if not all([password, password2]):
            msg = "密码不能为空"
            rep_dict["msg"] = msg
            return render(request, "myApp/user/login.html", rep_dict)

        if not all([tel]) and not all([email]):
            msg = "电话号码或者邮箱必修输入"
            rep_dict["msg"] = msg
            return render(request, "myApp/user/login.html", rep_dict)

        if password != password2:
            msg = "两次密码不一致"
            rep_dict["msg"] = msg
            rep_dict.pop("password")
            rep_dict.pop("password2")
            return render(request, "myApp/user/login.html", rep_dict)

        if all([tel,email]):
            return render(request, "myApp/common/error.html",{"msg": "系统受到外部攻击，请联系管理员", "jump_index": "http://127.0.0.1:8000/index/"})
        user_by_auth = None
        if all(tel) and not all(email):
            # 2.2 手机号登陆
            user_by_auth = Users.objects.get(tel=tel)
        elif not all(tel) and all(email):
            # 先判断等方式
            # 1.2  输入项目必须合法 ,排除一些关键字，不如说 script ,比如说# ,比如说 delete ********

            # 2 根据db存放数据进行比较
            # 2.1 验证邮箱
            user_by_auth = Users.objects.get(email=email)

        if user_by_auth is None:
            msg = "用户不存在，请注册!"
            rep_dict["msg"] = msg
            return render(request, "myApp/user/login.html", rep_dict)

        # TODO
        auth_password = user_by_auth.password

        if user_by_auth.password != auth_password:
            msg = "密码输入有误"
            rep_dict["msg"] = msg
            rep_dict.pop("password")
            rep_dict.pop("password2")
            return render(request, "myApp/user/login.html", rep_dict)
        if cb1 is not None:
            # 有设置redis  TODO
            pass
        # 设置session
        request.session["user_id"] = user_by_auth.id
        # 3 处理结束跳转画面
        return render(request, "myApp/index/index.html", {"userName": user_by_auth.username})


#跳转到登陆画面
def toLogin(request):
    return render(request,"myApp/user/login.html")
#登陆
def dologin(request):
    return render(request, "myApp/user/index1.html")

#跳转到注册画面
def toRegisters(request):
    return render(request,"myApp/user/register.html")

def index(request):
    return render(request,"myApp/index/index1.html")


def upfile(request):
    return render(request,'myApp/common/upfile.html')

from django.conf import settings
def savefile(request):
    if request.method=="POST":
        f=request.FILES["file"]
        # 文件在服务器端的路径
        filePath=os.path.join(settings.MDEIA_ROOT,f.name)
        # 文件上传就相当于文件复制
        with open(filePath,'wb') as fp:
            for info in f.chunks():
                fp.write(info)
        return HttpResponse("上传成功")
    else:
        return HttpResponse("上传失败")

#暂时作为临时方法，以后用于celert
def send_register_active_email(to_main_user_mail, username, token):

    # 链接包含用户id  http://127.0.0.1:8080/user/active/{userId}?唯一id

    msg11 = "<h1>%s疾病预警系统欢迎您注册用户，点击下面链接进行激活：<h1><a hrefd='http://127.0.0.1:8080/user/active/%s'>http://127.0.0.1:8080/user/active/%s</a>" % (username, token, token)
    # recipt_list = [user.email]

    # 测试不能通过，不知道什么原因
    # send_mail(subject, "", context, recipt_list,html_message=msg11)
    # coding:utf-8
    # 第三方 SMTP 服务
    mail_host = settings.EMAIL_HOST  # 设置服务器
    mail_user = settings.EMAIL_FROM  # 用户名
    mail_pass = settings.EMAIL_HOST_PASSWORD  # "dkhafgqsflsjbhhg" 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格

    sender = settings.EMAIL_FROM
    receivers = [to_main_user_mail]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 设置格式
    message = MIMEText(msg11, 'html', 'utf-8')
    message['From'] = "疾病预警系统<http://127.0.0.1:8000/user/index>"
    message['To'] = to_main_user_mail

    subject = '疾病预警系统欢迎您:用户激活'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, settings.EMAIL_PORT)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print(u"邮件发送成功")
    except smtplib.SMTPException as e:
        pass


    """发送激活邮件"""
def forecast(request):
    print("a")
    return render(request, "myApp/forecast/forecast.html")

    # 组织邮件信息
    subject = '天天生鲜欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_main_user_mail]
    html_message = '<h1>%s, 欢迎你成为天天生鲜注册会员</h1>请点击下面连接激活你的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)


def inform(request):
    return render(request, "myApp/inform/inform.html")

def error(request):
    return render(request,"myApp/common/error.html")

def visualization(request):
    return render(request,'myApp/visualization/visualization.html')

def rawdata(request):
    return render(request,'myApp/rawdata/rawdata.html')

def line(request):
    return render(request,'myApp/index/line.html')

def aboutus(request):
    return render(request,'myApp/aboutus/aboutus.html')