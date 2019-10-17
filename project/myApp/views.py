from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import time
import os
import random
from django.conf  import settings
# Create your views here.
def index(request):
    #return HttpResponse("sunck is a good man")
    return render(request,'myApp/index.html')

from .models import Users,Students,Grades,StudentsManager
def students(request):
    studentsList=Students.stuObj2.all()
    return render(request,'myApp/students.html',{"students":studentsList})

def students2(request):
    # 报异常
    studentsList=Students.stuObj2.get(sgender=True)
    #return render(request,'myApp/students.html',{"students":studentsList})
    return HttpResponse("-------------")

# 显示前5个学生
def students3(request):
    studentsList = Students.stuObj2.all()[0:5] # 最后一个不算
    return render(request, 'myApp/students.html', {"students": studentsList})

# 分页显示学生
def stupage(request,page):
    # 0-5 5-10 10-15
    # 1   2     3
    # page*5
    page=int(page)
    studentsList=Students.stuObj2.all()[(page-1)*5:page*5]
    return render(request,'myApp/students.html',{"students":studentsList})

from django.db.models import Max,Min,F,Q

# 查询
def studentsearch(request):
    # 查寻名字中有孙的
    #studentsList=Students.stuObj2.filter(sname__contains="孙")
    #studentsList = Students.stuObj2.filter(sname__startswith="孙")
    #studentsList = Students.stuObj2.filter(pk__in=[2,4,6,8,10])
    #studentsList = Students.stuObj2.filter(sage__gte=30)
    #studentsList = Students.stuObj2.filter(lastTime__year=2107)
    #studentsList = Students.stuObj2.filter(sname__contains="孙")
    #studentsList = Students.stuObj2.filter(students__scontend__contains='薛延美')
    # 描述中带有'薛延美'这三个字的数据时属于哪个班级的
    grade = Grades.objects.filter(students__scontend__contains='薛延美')
    studentsList =Students.stuObj2.filter(Q(pk__lte=3) | Q(sage__gt=50))
    # maxAge=Students.stuObj2.aggregate(Max('sage'))
    # print(maxAge)
    return render(request,'myApp/students.html',{"students":studentsList})

def addstudent(request):
    grade=Grades.objects.get(pk=1)
    # 创建一个学生对象
    stu=Students.createStudent("六个话",34,True,"我叫刘德华，请多多关照",grade,"2017-8-10","2017-8-11")
    stu.save()
    return HttpResponse("dfs")
def addstudent2(request):
    grade=Grades.objects.get(pk=1)
    # 创建一个学生对象
    stu=Students.stuObj2.createStudent("张学友",34,True,"我叫张学友，请多多关照",grade,"2017-8-10","2017-8-11")
    stu.save()
    return HttpResponse("********")

from django.db.models import F,Q
def grades(request):
    # g=Grades.objects.filter(ggirlnum__gt=F('gboynum')+20)
    # print(g)

    return HttpResponse("QQQQQo")

#登陆
from .forms.login import LoginForm
def login(request):
   if request.method=="POST":
       f=LoginForm(request.POST)
       if f.is_valid():
           # 信息格式没多大问题 验证账号和密码的正确性
            print("************************************")
            nameid = f.cleaned_data["user_name"]
            pswd = f.cleaned_data["user_password"]
            try:
               user=Users.objects.get(userAccount=nameid)
               if user.userPasswd!=pswd:
                    return redirect('/login/')
            except Users.DoesNotExist as e:
                    return redirect('/login/')
            # 登陆成功

            user.save()
            request.session["username"] = user.userName

            return redirect('/mine/')
       else:
            return render(request,'myapp/login.html',{"title":"登陆","form":f,"error":f.errors})
   else:
        f=LoginForm()
        return render(request, 'myapp/login.html', {"title": "登陆", "form": f, "error": f.errors})


#注册
def register(request):
    if request.method == "POST":
        userAccount = request.POST.get("user_id")
        userPasswd  = request.POST.get("user_password")
        userName    = request.POST.get("user_name")
        userPhone   = request.POST.get("tele")
        userMail = request.POST.get("mail")

        token = time.time() + random.randrange(1, 100000)
        userToken = str(token)
        f = request.FILES["img"]
        userImg = os.path.join(settings.MDEIA_ROOT, userAccount + ".png")
        with open(userImg, "wb") as fp:
            for data in f.chunks():
                fp.write(data)

        user = Users.createuser(userAccount,userPasswd,userName,userPhone,userMail,userImg,userToken)
        user.save()

        request.session["user_name"] = userName
        request.session["token"] = userToken

        return redirect('/mine/')
    else:
        return render(request, 'myApp/register.html', {"title":"注册"})
