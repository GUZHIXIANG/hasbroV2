import xadmin
from xadmin import views
from django.contrib import admin

from .models import *
from product.models import *
from activity.models import *
from store.models import *
from area.models import *
from user.models import *

class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True      # 开启主题切换功能
    use_bootswatch = True
xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "酷远后台管理系统"  # 设置站点标题
    site_footer = "酷远商贸有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠

    def get_site_menu(self):
        menu = (
            {'title': '用户管理', 'menus': (
                # {'title': '用户信息', 'url': self.get_model_url(
                #     UserProfile, 'changelist')},
                {'title': '后台用户', 'url': self.get_model_url(
                    UserManager, 'changelist')},
                {'title': '小程序用户', 'url': self.get_model_url(
                    UserWechat, 'changelist')},                                        
            )},
            {'title': '小程序管理', 'menus': (
                {'title': '首页广告', 'url': self.get_model_url(Advert, 'changelist')},
                {'title': '购物车', 'url': self.get_model_url(
                    Trolly, 'changelist')},
                {'title': '收货地址', 'url': self.get_model_url(
                    Address, 'changelist')},
                {'title': '活动报名', 'url': self.get_model_url(
                    Join, 'changelist')},
                {'title': '实体信息', 'url': self.get_model_url(
                    Entity, 'changelist')},
                )}, 
            {'title': '商品管理', 'menus': (
                {'title': '商品类型', 'url': self.get_model_url(PType, 'changelist')}, 
                {'title': '商品标签', 'url': self.get_model_url(PTag, 'changelist')},
                {'title': '商品信息', 'url': self.get_model_url(
                    Product, 'changelist')},
                )},
            {'title': '活动管理', 'menus': (
                {'title': '活动类型', 'url': self.get_model_url(
                    AType, 'changelist')},
                {'title': '活动信息', 'url': self.get_model_url(
                    Activity, 'changelist')},
            )},
            {'title': '门店管理', 'menus': (
                {'title': '门店信息', 'url': self.get_model_url(
                    Store, 'changelist')},
            )},
            {'title': '行政区划管理', 'menus': (
                {'title': '行政区划', 'url': self.get_model_url(
                    Areas, 'changelist')},
            )},
                
        )
        return menu
xadmin.site.register(views.CommAdminView, GlobalSettings)


# TODO(GU)  重写用户模型
# @xadmin.sites.register(UserProfile)
# class UserProfileAdmin(object):
#     '''用户信息'''
#     list_display = ('username', 'nickName', 'gender', 'city')
#     search_fields = ('city',)
#     refresh_times = [300, 600]
#     list_per_page = 20

# TODO(GU)  隐藏实体
@xadmin.sites.register(Entity)
class EntityAdmin(object):
    '''实体信息'''
    list_display = ('name', 'type', 'create_time', 'operate_time')
    list_per_page = 20

    list_display_links = None

    def has_add_permission(self):
        return False

    def has_delete_permission(self, request=None):
        return False


@xadmin.sites.register(Advert)
class AdvertAdmin(object):
    '''广告信息'''
    def name(self, obj):
        return obj.entity.name
    name.short_description = '名称'
    def type(self, obj):
        return obj.entity.get_type_display()
    type.short_description = '类型'
    list_display = ('name','type', 'image_img','order', 'is_show')
    search_fields = ('entity__name', 'entity__type')
    list_per_page = 20


@xadmin.sites.register(Join)
class JoinAdmin(object):
    '''报名信息查看'''
    list_display = ('user', 'activity', 'store', 'name',
                    'phone')
    readonly_fields = ('user', 'activity', 'store', 'name',
                       'phone')
    search_fields = ('activity__name', 'store__name')
    list_filter = ('activity', 'store')

    refresh_times = [300, 600]
    list_per_page = 20

    list_display_links = None  # 禁用编辑链接

    def has_add_permission(self):
        return False

    def has_delete_permission(self, request=None):
        return False


@xadmin.sites.register(Trolly)
class TrollyAdmin(object):
    '''购物车查看'''

    def name(self, obj):
        return obj.pinfo.product.name
    name.short_description = '名称'
    def ptype(self,obj):
        return obj.pinfo.product.get_ptype_display()
    ptype.short_description = '分类'
    def color(self, obj):
        return obj.pinfo.color
    color.short_description = '颜色'
    def weight(self,obj):
        return obj.pinfo.weight
    weight.short_description = '重量'
    def norms(self,obj):
        return obj.pinfo.norms
    norms.short_description = '规格'
    def price(self, obj):
        return obj.pinfo.price
    price.short_description = '单价'

    list_display = ('user', 'name', 'ptype', 'color',
                    'weight', 'norms', 'price', 'nums')
    search_fields = ('pinfo__price', 'pinfo__product__name')
    list_filter = ('pinfo__product__ptype',)
    refresh_times = [300, 600]
    list_per_page = 20

    List_display_links = None  # 禁用编辑链接

    def has_add_permission(self):
        return False

    def has_delete_permission(self, request=None):
        return False


@xadmin.sites.register(Address)
class AddressAdmin(object):
    '''地址查看'''

    def get_province(self, obj):
        return obj.province.name
    get_province.short_description = '省份'
    def get_city(self, obj):
        return obj.city.name
    get_city.short_description = '城市'
    def get_district(self, obj):
        return obj.district.name
    get_district.short_description = '区域'
    list_display = ('user', 'name', 'phone', 'get_province',
                    'get_city', 'get_district', 'address')
    list_filter = ('province__name', 'city__name', 'district__name')
    refresh_times = [300, 600]
    list_per_page = 20

    List_display_links = None  # 禁用编辑链接

    def has_add_permission(self):
        return False

    def has_delete_permission(self, request=None):
        return False
