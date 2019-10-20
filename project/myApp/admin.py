from django.contrib import admin

# Register your models here.
from .models import Grades,Students,Users,Rawdata,Forecast,Inform,Collect,Message,Jurisdiction

admin.site.site_header = '淮安市传染病预警后台管理系统'
admin.site.site_title = '登录系统后台'
admin.site.index_title = '后台管理'

class UsersAdmin(admin.ModelAdmin):
    list_display = ['id','user_name',
                    #'login_id',
                    'user_mail','user_phone','isInform',
                    'isMail','user_type','power_type','creator_id','update_id',
                   # 'lastTime','createTime',
                    'isDel','img']
    list_filter = ['user_name']
    search_fields = ['user_name']  # 查找
    list_per_page = 5

class RawdataAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'address', 'temperature', 'humidity', 'atmospheric', 'precipitation', 'sunshine', 'wind',
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

    list_filter = ['pre_date','pre_type'] # 过滤器
    search_fields = ['pre_date','pre_type']  # 查找
    date_hierarchy = 'pre_date'  # 详细时间分层筛选　
    list_per_page = 5

    #inlines = [AreaTabu1,]
class InformAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'isSend', 'creator_id', 'update_id', 'createTime', 'lastTime']
    list_filter = ['creator_id','update_id', 'createTime', 'lastTime']
    search_fields = ['id', 'content', 'isSend', 'creator_id', 'update_id', 'createTime', 'lastTime']  # 查找
    list_per_page = 5

class CollectAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'inform_id', 'creator_id', 'update_id', 'createTime', 'lastTime', 'isDel']
    list_filter = ['creator_id', 'update_id', 'createTime', 'lastTime']
    search_fields = ['id', 'user_id', 'inform_id', 'creator_id', 'update_id', 'createTime', 'lastTime', 'isDel']  # 查找
    list_per_page = 5

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'user_id','isShow', 'creator_id', 'update_id', 'createTime', 'lastTime', 'isDel']
    list_filter = ['user_id','isShow','creator_id', 'update_id', 'createTime', 'lastTime']
    search_fields = [ 'user_id', 'isShow', 'creator_id', 'update_id', 'createTime', 'lastTime']  # 查找
    list_per_page = 5



class JurisdictionAdmin(admin.ModelAdmin):
    list_display = ['id', 'root_name','creator_id', 'update_id', 'createTime', 'lastTime']
    list_filter = ['id', 'root_name','creator_id', 'update_id', 'createTime', 'lastTime']
    search_fields = ['id', 'root_name','creator_id', 'update_id', 'createTime', 'lastTime']  # 查找
    list_per_page = 5

class GradesAdmin(admin.ModelAdmin):
    #inlines = [StudentsInfo]
    # 列表页属性
    list_display = ['id', 'gname', 'gdate', 'ggirlnum', 'gboynum', 'isDelete']
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
admin.site.register(Inform,InformAdmin)
admin.site.register(Collect,CollectAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Jurisdiction,JurisdictionAdmin)