from django.contrib import admin

# Register your models here.
from .models import Grades,Students,Users,Rawdata,Forecast

admin.site.site_header = '淮安市传染病预警后台管理系统'
admin.site.site_title = '登录系统后台'
admin.site.index_title = '后台管理'

class UsersAdmin(admin.ModelAdmin):
    list_display = ['pk','user_name','login_id','tele','mail','isInform',
                    'isMail','user_type','power_type','creator_id','update_id',
                   # 'lastTime','createTime',
                    'isDel','img']
    list_filter = ['user_name']
    search_fields = ['user_name']  # 查找
    list_per_page = 5


class RawdataAdmin(admin.ModelAdmin):
    list_display = ['pk', 'date', 'address', 'temperature', 'humidity', 'atmospheric', 'precipitation', 'sunshine', 'wind',
                    'aqi','pm2','pm10','SO2','CO','NO2','O3','incidence']
    list_filter = ['date']
    search_fields = ['address']  # 查找
    list_per_page = 5

# class AreaTabu1(admin.TabularInline):
#     model = Forecast
#     #默认
#     extra = 2


#@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = [ 'id','pre_date','pre_type','isDel', 'pre_result','creator_id','update_id','createTime','lastTime']
    #list_display = ['pk', 'pre_date', 'pre_type', 'isDel', 'pre_result', 'update_id']

    list_filter = ['pre_date']
    search_fields = ['pre_date']  # 查找
    list_per_page = 5

    #inlines = [AreaTabu1,]

class GradesAdmin(admin.ModelAdmin):
    #inlines = [StudentsInfo]
    # 列表页属性
    list_display = ['pk', 'gname', 'gdate', 'ggirlnum', 'gboynum', 'isDelete']
    list_filter = ['gname']
    search_fields = ['gname']#查找
    list_per_page = 5
    # 添加、修改页属性
    # fields = ['ggirlnum','gboynum','gname','gdate','isDelete']
    fieldsets = [
        ("num", {"fields": ['ggirlnum', 'gboynum']}),
        ("base", {"fields": ['gname', 'gdate', 'isDelete']}),
    ]


    # 注册要管理的对象
admin.site.register(Grades,GradesAdmin)
admin.site.register(Students)
admin.site.register(Users,UsersAdmin)
admin.site.register(Rawdata,RawdataAdmin)
admin.site.register(Forecast,ForecastAdmin)