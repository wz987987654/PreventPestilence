from django.conf.urls import url
from . import views
from .views import RegisterView
from .views import ActiveView
from .views import Login
urlpatterns=[

    # 主页
    url(r'^index/$', views.index, name="index"),

    # 用户登录
    url(r'^user/login$', Login.as_view(), name="login"),
    url(r'^user/dologin$', Login.as_view(), name="dologin"),
    # 注册
    url(r'^user/register$', RegisterView.as_view(), name="register"),
    url(r'^user/doRegister$', RegisterView.as_view(), name="doRegister"),
    url(r'^user/toRegisters$', views.toRegisters, name="toRegisters"),

    url(r'^user/active/(?P<token>.*)$',ActiveView.as_view() , name="active$"),

    url(r'^forecast/forecast$', views.forecast, name="forecast"),
    url(r'^inform/inform$', views.inform),
    url(r'^error', views.error, name="error"),
    url(r'^upfile/$',views.upfile),
    url(r'^savefile/$',views.savefile),
    url(r'^visualization', views.visualization, name="visualization"),


]
