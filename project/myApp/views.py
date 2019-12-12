from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from myApp.models import Users
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
#
# def students(request):
#     studentsList=Students.stuObj2.all()
#     return render(request, 'myApp/app/students.html', {"students":studentsList})
#
# def students2(request):
#     # 报异常
#     studentsList=Students.stuObj2.get(sgender=True)
#     #return render(request,'myApp/students.html',{"students":studentsList})
#     return HttpResponse("-------------")
#
# # 显示前5个学生
# def students3(request):
#     studentsList = Students.stuObj2.all()[0:5] # 最后一个不算
#     return render(request, 'myApp/app/students.html', {"students": studentsList})
#
# # 分页显示学生
# def stupage(request,page):
#     # 0-5 5-10 10-15
#     # 1   2     3
#     # page*5
#     page=int(page)
#     studentsList=Students.stuObj2.all()[(page-1)*5:page*5]
#     return render(request, 'myApp/app/students.html', {"students":studentsList})

from django.db.models import Max,Min,F,Q

# # 查询
# def studentsearch(request):
#     # 查寻名字中有孙的
#     #studentsList=Students.stuObj2.filter(sname__contains="孙")
#     #studentsList = Students.stuObj2.filter(sname__startswith="孙")
#     #studentsList = Students.stuObj2.filter(pk__in=[2,4,6,8,10])
#     #studentsList = Students.stuObj2.filter(sage__gte=30)
#     #studentsList = Students.stuObj2.filter(lastTime__year=2107)
#     #studentsList = Students.stuObj2.filter(sname__contains="孙")
#     #studentsList = Students.stuObj2.filter(students__scontend__contains='薛延美')
#     # 描述中带有'薛延美'这三个字的数据时属于哪个班级的
#     grade = Grades.objects.filter(students__scontend__contains='薛延美')
#     studentsList =Students.stuObj2.filter(Q(pk__lte=3) | Q(sage__gt=50))
#     # maxAge=Students.stuObj2.aggregate(Max('sage'))
#     # print(maxAge)
#     return render(request, 'myApp/app/students.html', {"students":studentsList})
#
# def addstudent(request):
#     grade=Grades.objects.get(pk=1)
#     # 创建一个学生对象
#     stu=Students.createStudent("六个话",34,True,"我叫刘德华，请多多关照",grade,"2017-8-10","2017-8-11")
#     stu.save()
#     return HttpResponse("dfs")
# def addstudent2(request):
#     grade=Grades.objects.get(pk=1)
#     # 创建一个学生对象
#     stu=Students.stuObj2.createStudent("张学友",34,True,"我叫张学友，请多多关照",grade,"2017-8-10","2017-8-11")
#     stu.save()
#     return HttpResponse("********")
#
# from django.db.models import F,Q
# def grades(request):
#     # g=Grades.objects.filter(ggirlnum__gt=F('gboynum')+20)
#     # print(g)
#
#     return HttpResponse("QQQQQo")
#
# #登陆
# # 说明：这个装饰器的作用，就是在每个视图函数被调用时，都验证下有没法有登录，
# # 如果有过登录，则可以执行新的视图函数，
# # 否则没有登录则自动跳转到登录页面。
# def check_login(f):
#     @wraps(f)
#     def inner(request,*arg,**kwargs):
#         if request.session.get('is_login')=='1':
#             return f(request,*arg,**kwargs)
#         else:
#             return redirect('/login/')
#     return inner
#
# def login(request):
#     # 如果是POST请求，则说明是点击登录按扭 FORM表单跳转到此的，那么就要验证密码，并进行保存session
#     if request.method=="POST":
#         user_name=request.POST.get('user_name')
#         user_password=request.POST.get('user_password')
#
#         user=Users.objects.filter(user_name=user_name,user_password=user_password)
#         print(user)
#         if user:
#             #登录成功
#             # 1，生成特殊字符串
#             # 2，这个字符串当成key，此key在数据库的session表（在数据库存中一个表名是session的表）中对应一个value
#             # 3，在响应中,用cookies保存这个key ,(即向浏览器写一个cookie,此cookies的值即是这个key特殊字符）
#             request.session['is_login']='1'  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
#             request.session['user_id']=user[0].id
#             messages.success(request,"登陆成功")
#             #return redirect('/myApp/index/')
#             return redirect('/index/')
#         else:
#             messages.success(request,"账号密码错误")
#             return redirect('/login/')
#     # 如果是GET请求，就说明是用户刚开始登录，使用URL直接进入登录页面的
#     return render(request, 'myApp/app/login.html')
#
# def index(request):
#     # students=Students.objects.all()  ## 说明，objects.all()返回的是二维表，即一个列表，里面包含多个元组
#     # return render(request,'index.html',{"students_list":students})
#     # user_name1=request.session.get('user_name')
#     user_id1=request.session.get('user_id')
#     # 使用user_id去数据库中找到对应的user信息
#     userobj=Users.objects.filter(id=user_id1)
#     print(userobj)
#     if userobj:
#         return render(request, 'myApp/index/index.html')
#     else:
#         return render(request, 'myApp/index/index.html')
#
# def adduser(request):
#     if request.method=="POST":
#         user_name=request.POST.get('user_name')
#         user_mail=request.POST.get('user_mail')
#         user_phone = request.POST.get('user_phone')
#         user_password = request.POST.get('user_password')
#         creator_id=request.POST.get('creator_id')
#         print(user_name)
#         test1 = Users(user_name=user_name,user_password=user_password,user_mail=user_mail,user_phone=user_phone,creator_id=creator_id)
#         test1.save()
#     return render(request, 'myApp/app/login.html')
#
# def to_adduser(request):
#     return render(request, 'myApp/app/adduser.html')
#
# def to_change(request):
#     return render(request, 'myApp/app/changepassword.html')
#
# def logout(request):
#     request.session['is_login']='0'
#
#     return render(request, 'myApp/app/login.html')
#
# def changepassword(request):
#     user_name=request.POST.get('user_name')
#     user_password=request.POST.get('user_password')
#     userobj = Users.objects.filter(user_name=user_name)
#
#     # Test.objects.filter(user_name=user_name).update(user_password=user_password)
#     if userobj:
#         user = Users.objects.get(user_name=user_name)
#         user.user_password=user_password
#         user.save()
#         messages.info(request,"修改成功")
#         return redirect('/login/')
#     else:
#         messages.info(request,"没有找到该user_name")
#         return redirect('/myApp/to_change/')
#
#
#
# def forecast(request):
#     temperature = request.POST.get('temperature')
#     humidity = request.POST.get('humidity')
#     atmospheric = request.POST.get('atmospheric')
#     precipitation = request.POST.get('precipitation')
#     sunshine = request.POST.get('sunshine')
#     wind = request.POST.get('wind')
#     aqi = request.POST.get('aqi')
#     pm2 = request.POST.get('pm2')
#     SO2 = request.POST.get('SO2')
#     CO = request.POST.get('CO')
#     NO2 = request.POST.get('NO2')
#     O3 = request.POST.get('O3')
#     forecast=Forecast.objects.filter(temperature=temperature,humidity=humidity,atmospheric=atmospheric,precipitation=precipitation,
#                                      sunshine=sunshine,wind=wind,aqi=aqi,pm2=pm2,SO2=SO2,CO=CO,NO2=NO2,O3=O3)
#
#     #
#     #return redirect( 'map')
#
#

#暂时作为临时方法，以后用于celert
def send_register_active_email(to_main_user_mail, username, token):
    # 链接包含用户id  http://127.0.0.1:8080/user/active/{userId}?唯一id

    msg11 = "<h1>%s淮阴师范疫病预防中心欢迎您注册用户，点击下面链接进行激活：<h1><a hrefd='http://127.0.0.1:8080/user/active/%s'>http://127.0.0.1:8080/user/active/%s</a>" % (username, token, token)
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
    message['From'] = "宁夏大学疾病预防中心<http://127.0.0.1:8000/user/index>"
    message['To'] = to_main_user_mail

    subject = '淮阴师范疫病预防中心欢迎你:用户激活'
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