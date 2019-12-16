from django.conf.urls import url
from . import views
from .views import RegisterView
from .views import ActiveView
from .views import Login
urlpatterns=[

    # 主页
    url(r'^index/$', views.index, name="index"),

    #用户
    url(r'^user/login$', Login.as_view(), name="login"),
    url(r'^user/dologin$', Login.as_view(), name="dologin"),
    url(r'^user/register$', RegisterView.as_view(), name="register"),
    url(r'^user/doRegister$', RegisterView.as_view(), name="doRegister"),
    url(r'^forecast/chinamap$', views.forecast, name="forecast"),

    url(r'^user/active/(?P<token>.*)$',ActiveView.as_view() , name="active$"),


    #
    # url(r'^$',views.index),
    # url(r'^students/$',views.students),
    # url(r'^students2/$', views.students2),
    # url(r'^students3/$', views.students3),
    # url(r'^stu/(\d+)/$',views.stupage),
    # url(r'^studentsearch/$',views.studentsearch),
    # url(r'^addstudent/$',views.addstudent),
    # url(r'^addstudent2/$', views.addstudent2),
    # url(r'^grades/$',views.grades),
    #
    #
    #
    # url(r'^login/$',views.login,name="login"),
    # #url(r'^register/$',views.register,name="register"),
    # url(r'^to_adduser/$', views.to_adduser),
    # url(r'^adduser/$', views.adduser),
    # url(r'^logout/$', views.logout),
    # url(r'^changepassword/$', views.changepassword),
    # url(r'^to_change/$', views.to_change),
    # url(r'^forecast/$',views.forecast,name='forecast')
]
