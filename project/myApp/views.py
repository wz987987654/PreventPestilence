from django.shortcuts import render
from django.views import View
from myApp.models import Users
import re



#注册相关
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

        #一定要是使用他自己的这种方式区创建而不是使用Users()去创建--你自己的项目和Django框架的整合
        user = Users.objects.create_user(username,email,password)

        #注册完之后该用户是不能登陆的，只有后段承认之后才可以使用，此处为了方便项目的进行，手动改成1
        user.is_active = 1

        #更新方法
        user.save()

        return  render(request, "myApp/index/index.html", {"userName":username})

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
