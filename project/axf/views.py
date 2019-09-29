from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Wheel,Nav,Mustbuy,Shop,MainShow,User
import time
import os
import random
from django.conf  import settings
# Create your views here.
def home(request):
    wheelsList=Wheel.objects.all()
    navList=Nav.objects.all()
    mustbuyList = Mustbuy.objects.all()
    shopList = Shop.objects.all()
    shop1 = shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:11]
    mainList = MainShow.objects.all()

    return render(request,'axf/home.html',{"title":"主页",
                                           "wheelsList":wheelsList,
                                           "navList":navList,
                                           "mustbuyList":mustbuyList,
                                           "shop1": shop1,
                                           "shop2": shop2,
                                           "shop3": shop3,
                                           "shop4": shop4,
                                           "mainList": mainList
                                           })

def market(request):
    return render(request,'axf/market.html',{"title":"闪送超市"})

def cart(request):
    return render(request,'axf/cart.html',{"title":"购物车"})

def mine(request):
    username=request.session.get("username","未登录")
    return render(request,'axf/mine.html',{"title":"我的","username":username})

#登陆
from .forms.login import LoginForm
from django.http import HttpResponse
def login(request):
   if request.method=="POST":
       f=LoginForm(request.POST)
       if f.is_valid():
           # 信息格式没多大问题 验证账号和密码的正确性
            print("************************************")
            nameid = f.cleaned_data["username"]
            pswd = f.cleaned_data["passwd"]
            try:
               user=User.objects.get(userAccount=nameid)
               if user.userPasswd!=pswd:
                    return redirect('/login/')
            except User.DoesNotExist as e:
                    return redirect('/login/')
            # 登陆成功
            token=time.time()+random.randrange(1,100000)
            user.userToken=str(token)
            user.save()
            request.session["username"] = user.userName
            request.session["token"] = user.userToken

            return redirect('/mine/')
       else:
            return render(request,'axf/login.html',{"title":"登陆","form":f,"error":f.errors})
   else:
        f=LoginForm()
        return render(request, 'axf/login.html', {"title": "登陆", "form": f, "error": f.errors})


#注册
def register(request):
    if request.method == "POST":
        userAccount = request.POST.get("userAccount")
        userPasswd  = request.POST.get("userPass")
        userName    = request.POST.get("userName")
        userPhone   = request.POST.get("userPhone")
        userAdderss = request.POST.get("userAdderss")
        userRank    = 0
        token = time.time() + random.randrange(1, 100000)
        userToken = str(token)
        f = request.FILES["userImg"]
        userImg = os.path.join(settings.MDEIA_ROOT, userAccount + ".png")
        with open(userImg, "wb") as fp:
            for data in f.chunks():
                fp.write(data)

        user = User.createuser(userAccount,userPasswd,userName,userPhone,userAdderss,userImg,userRank,userToken)
        user.save()

        request.session["username"] = userName
        request.session["token"] = userToken

        return redirect('/mine/')
    else:
        return render(request, 'axf/register.html', {"title":"注册"})


def checkuserid(request):
    userid = request.POST.get("userid")
    try:
        user = User.objects.get(userAccount = userid)
        return JsonResponse({"data":"改用户已经被注册","status":"error"})
    except User.DoesNotExist as e:
        return JsonResponse({"data":"可以注册","status":"success"})

# 退出登陆
from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect('/mine/')
import os
from django.conf import settings
#上传图片
def upfile(request):
    return render(request,'axf/upfile.html')


def savefile(request):
    if request.method=="POST":
        f=request.FILES["file"]
        #文件在服务器端的路径
        filePath=os.path.join(settings.MDEIA_ROOT,f.name)
        with open(filePath,'wb')as fp:
            for info in f.chunks():
                fp.write(info)
        return HttpResponse("上传成功")
    else:
        return HttpResponse("上传失败")

def forecast(request):
    #return render(request, 'axf/map/forecast.html')
    return render(request, 'axf/map/世界地图.html')