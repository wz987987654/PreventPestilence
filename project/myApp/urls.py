from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^$',views.index),
    url(r'^students/$',views.students),
    url(r'^students2/$', views.students2),
    url(r'^students3/$', views.students3),
    url(r'^stu/(\d+)/$',views.stupage),
    url(r'^studentsearch/$',views.studentsearch),
    url(r'^addstudent/$',views.addstudent),
    url(r'^addstudent2/$', views.addstudent2),
    url(r'^grades/$',views.grades),


    # 登陆
    url(r'^index/$',views.index,name="index"),
    url(r'^login/$',views.login,name="login"),
    #url(r'^register/$',views.register,name="register"),
    url(r'^to_adduser/$', views.to_adduser),
    url(r'^adduser/$', views.adduser),
    url(r'^logout/$', views.logout),
    url(r'^changepassword/$', views.changepassword),
    url(r'^to_change/$', views.to_change),
    url(r'^forecast/$',views.forecast,name='forecast')
]
