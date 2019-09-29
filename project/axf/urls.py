from django.conf.urls import url,include
from .import views
urlpatterns = [

    url(r'^home/$',views.home,name="home"),
    url(r'^market/$',views.market,name="market"),
    url(r'^cart/$',views.cart,name="cart"),
    url(r'^mine/$',views.mine,name="mine"),
    # 登陆
    url(r'^login/$',views.login,name="login"),
    url(r'^register/$',views.register,name="register"),
    # 验证账号是否被注册
    url(r'^checkuserid/$',views.checkuserid,name="checkuserid"),
    # 退出登陆
    url(r'^quit/$',views.quit,name="quit"),
    url(r'^upfile/$',views.upfile,name="upfile"),
    url(r'^savefile/$',views.savefile),
    url(r'^forecast/$',views.forecast)

]