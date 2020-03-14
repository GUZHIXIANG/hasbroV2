import xadmin
from xadmin import views
from django.contrib import admin
from xadmin.plugins.auth import UserAdmin
from .models import *


# TODO(GU)  重写用户模型
xadmin.site.unregister(UserProfile)
# xadmin.site.register(UserProfile,UserAdmin)
# @xadmin.sites.register(UserProfile)
# class UserProfileAdmin(object):
#     '''用户信息'''
#     list_display = ('username', 'nickName', 'gender', 'city')
#     search_fields = ('city',)
#     refresh_times = [300, 600]
#     list_per_page = 20



@xadmin.sites.register(UserManager)
class UserManagerAdmin(UserAdmin):
    '''后台用户信息'''
    list_display = ('username','last_name','first_name','email','is_superuser','is_staff','is_active')
    search_fields = ('username',)
    list_per_page = 20
    exclude = ('type',)
    style_fields = {'groups': 'm2m_transfer','user_permissions': 'm2m_transfer'}

    def save_models(self):
        obj = self.new_obj
        obj.type = 0
        obj.save()
    
    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(type=0)
        return qs




@xadmin.sites.register(UserWechat)
class UserWechatAdmin(object):
    '''小程序用户信息'''
    list_display = ('username', 'nickName', 'gender', 'city')
    search_fields = ('username',)
    refresh_times = [300, 600]
    list_per_page = 20
    exclude = ('type',)
    style_fields = {'groups': 'm2m_transfer','user_permissions': 'm2m_transfer'}    

    def save_models(self):
        obj = self.new_obj
        obj.type = 1
        obj.save()
    
    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(type=1)
        return qs