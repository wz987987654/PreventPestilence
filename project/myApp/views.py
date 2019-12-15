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
        send_register_active_email(user.email,user.username,serialier_id_token)

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
        return render(request,"myApp/user/login.html")
    def post(self,request):
        # 1 画面输入项目的检查
            # 1.1 输入项目不能为空
            # 1.2  输入项目必须合法

        # 2 根据db存放数据进行比较
            # 邮箱
            # 手机号
                # 验证通过
                    # 判断有没有登陆90天
                        # 有设置redis  TODO
                        # 设置session
                # 没有
            # 设置session

        # 3 处理结束跳转画面
        pass



#跳转到登陆画面
def toLogin(request):
    return render(request,"myApp/user/login.html")
#登陆
def dologin(request):
    return render(request, "myApp/user/register.html")
#跳转到注册画面
def toRegisters(request):
    return render(request,"myApp/user/register.html")

def index(request):
    return render(request,"myApp/index/index.html")



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

    # 设置她的格式
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
    # 组织邮件信息
    subject = '天天生鲜欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_main_user_mail]
    html_message = '<h1>%s, 欢迎你成为天天生鲜注册会员</h1>请点击下面连接激活你的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)


def forecast(request):
    return render(request,"myApp/forecast/中国地图.html")