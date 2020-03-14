import xadmin
from xadmin import views
from django.contrib import admin

# from .models.UserModel import UserProfile
# from user.models import UserProfile
from .models.ProductTypeModel import *
from .models.ProductModel import *
from .models.TrollyModel import MyTrolly
from .models.AdvModel import AdvPicModel

from .models.ActivityModel import *
from .models.SignUpModel import SignUp
from .models.StoreModel import Store
from .models.TestModel import *

from django.db import transaction
import xlrd


# class BaseSetting(object):
#     """xadmin的基本配置"""
#     enable_themes = True      # 开启主题切换功能
#     use_bootswatch = True 


# xadmin.site.register(views.BaseAdminView, BaseSetting)

# class GlobalSettings(object):
#     """xadmin的全局配置"""
#     site_title = "酷远后台管理系统"  # 设置站点标题
#     site_footer = "酷远商贸有限公司"  # 设置站点的页脚
#     menu_style = "accordion"  # 设置菜单折叠

# xadmin.site.register(views.CommAdminView, GlobalSettings)

# TODO(GU)  未优化
# class AdvPicAdmin(object):
#     list_display = ('order','productbaseinfo','image_img')
#     list_per_page = 20
# xadmin.site.register(AdvPicModel,AdvPicAdmin)

'''##########################################'''
'''############### 微信用户信息查看 ###############'''
'''##########################################'''


# @xadmin.sites.register(UserProfile)
# class UserProfileAdmin(object):
#     list_display = ('user', 'nickName', 'gender', 'city')
    
#     search_fields = ('city',)
#     refresh_times = [300, 600]
#     list_per_page = 20
#     List_display_links = None  # 禁用编辑链接

#     def has_add_permission(self):
#         return False

#     def has_delete_permission(self, request=None):
#         return False


'''##########################################'''
'''############### 小程序购物车信息查看 ###############'''
'''##########################################'''


@xadmin.sites.register(MyTrolly)
class MyTrollyAdmin(object):
    list_display = ('user', 'productbaseinfo', 'nums')

    readonly_fields = ('user', 'productbaseinfo',
                       'nums', 'checkbox')
    search_fields = ('productbaseinfo__productId',
                     'productbaseinfo__productName', 'productbaseinfo__systemCode', 'productbaseinfo__barCode')
    list_filter = ('productbaseinfo__productType',)

    refresh_times = [300, 600]
    list_per_page = 20

    List_display_links = None  # 禁用编辑链接

    def has_add_permission(self):
        return False

    def has_delete_permission(self, request=None):
        return False


'''##########################################'''
'''############### 商品详情图片管理 ###############'''
'''##########################################'''


@xadmin.sites.register(ProductUrl)
class ProductUrlAdmin(object):
    list_display = ('productbaseinfo', 'url', 'image_img')
    list_per_page = 20

'''##########################################'''
'''############### 商品类型海报管理 ###############'''
'''##########################################'''

@xadmin.sites.register(PTypePoster)
class PTypePosterAdmin(object):
    '''商品类型海报管理'''
    list_display = ('ptype', 'image', 'text', 'image_large')
    search_fields = ('ptype__name',)
    list_per_page = 20


'''##########################################'''
'''############### 商品类型图标管理 ###############'''
'''##########################################'''


@xadmin.sites.register(PTypeImage)
class PTypeImageAdmin(object):
    '''商品类型图标管理'''
    list_display = ('ptype', 'image', 'image_thumbnail',
                    'image_medium')
    search_fields = ('ptype__name',)
    list_per_page = 20


'''##########################################'''
'''############### 商品类型管理 ###############'''
'''##########################################'''


class PTypePosterStackInline(object):
    model = PTypePoster
    extra = 0

class PTypeImageStackInline(object):
    model = PTypeImage
    extra = 0

@xadmin.sites.register(PType)
class PTypeAdmin(object):
    '''商品类型管理'''
    list_display = ('name', 'parent', 'desc', 'full_name')
    search_fields = ('name', 'parent')
    list_editable = ('parent', 'desc')
    list_filter = ('parent', 'desc')
    list_per_page = 20

    def full_name(self,obj):
        fname = [obj.name.__str__()]
        tmp = obj.parent
        c = 0
        while tmp != None:
            if c > 10: # 限制循环
                continue
            fname.append(tmp.name.__str__())
            tmp = tmp.parent
            c += 1 
        return '|'.join(fname[::-1])
    full_name.short_description = '全称'

    inlines = [PTypePosterStackInline, PTypeImageStackInline]


'''##########################################'''
'''############### 商品标签管理 ###############'''
'''##########################################'''


@xadmin.sites.register(PTag)
class PtagAdmin(object):
    '''商品标签管理'''
    list_display = ('name', 'description', 'product')
    search_fields = ('product__productId', 'product__productName',
                     'product__systemCode', 'product__barCode')
    filter_horizontal = ('product',)
    style_fields = {'product': 'm2m_transfer'}
    list_per_page = 20

'''##########################################'''
'''############### 商品信息管理 ###############'''
'''##########################################'''


class ProductUrlStackInline(object):
    model = ProductUrl
    extra = 0

@xadmin.sites.register(ProductBaseInfo)
class ProductBaseInfoAdmin(object):
    '''商品信息管理'''
    list_display = ('productId', 'productName',  'systemCode', 'barCode', "image_img",
                    'productType', 'color', 'norms', 'weight', 'price', 'quantity', 'shell','tag')
    search_fields = ('productId', 'productName',
                     'systemCode', 'barCode', 'price')
    list_filter = ('productType', 'shell')
    list_editable = ('shell',)
    list_per_page = 20

    inlines = [ProductUrlStackInline]

    def tag(self,obj):
        return '.'.join([x.name for x in obj.tags.all()])
    tag.short_description = '标签'
    #excel导入导出功能
    list_export = ['xls', 'xml', 'json']
    import_excel = True


    def post(self, request, *args, **kwargs):
        #  导入逻辑
        if 'excel' in request.FILES:
            pass
            excel_file = request.FILES.get('excel')
            file_type = excel_file.name.split('.')[1]
            if file_type in ['xlsx', 'xls']:  # 支持这两种文件格式
                # 打开工作文件
                data = xlrd.open_workbook(
                    filename=None, file_contents=excel_file.read())
                table = data.sheets()[0]
                rows = table.nrows
                try:
                    with transaction.atomic():
                        for row in range(1, rows):
                            vals = table.row_values(row)
                            print(vals)
                            CHOICE_dict = {'上架': 'on', '下架': 'off'}
                            ProductBaseInfo.objects.create(
                                productId=vals[0],
                                productName=vals[1],
                                systemCode=vals[2],
                                barCode=vals[3],
                                productType=1,
                                color=vals[5],
                                norms=vals[6],
                                weight=vals[7],
                                price=vals[8],
                                quantity=vals[9],
                                shell=CHOICE_dict.get(vals[10],'off'),
                            
                            )
                except Exception as e:
                    print(e)
                    return e
        return super().post(request, args, kwargs)
        

'''##########################################'''
'''############### 小程序活动报名信息查看 ###############'''
'''##########################################'''


@xadmin.sites.register(SignUp)
class SignUpAdmin(object):
    '''报名信息查看'''
    list_display = ('user', 'activity', 'store', 'signup_name',
                    'signup_phone', 'signup_create_time', 'signup_operate_time')
    readonly_fields = ('user', 'activity', 'store', 'signup_name',
                       'signup_phone', 'signup_create_time', 'signup_operate_time')
    search_fields = ('activity__activity_name', 'store__store_name')
    list_filter = ('activity', 'store')

    refresh_times = [300, 600]
    list_per_page = 20

    List_display_links = None  #禁用编辑链接

    def has_add_permission(self):
        return False

    def has_delete_permission(self,request=None):
        return False

'''##########################################'''
'''############### 门店信息管理 ###############'''
'''##########################################'''


@xadmin.sites.register(Store)
class StoreAdmin(object):
    '''门店信息管理'''
    list_display = ('store_name', 'store_telephone',
                    'store_address', 'store_area')
    search_fields = ('store_name', 'store_telephone',
                     'store_address')
    list_filter = ('store_area',)
    list_per_page = 20

'''##########################################'''
'''############### 活动类型管理 ###############'''
'''##########################################'''


@xadmin.sites.register(ActivityType)
class ATypeAdmin(object):
    '''活动类型管理'''
    list_display = ('activity_type', 'type_description')
    search_fields = ('activity_type',)


'''##########################################'''
'''############### 活动信息管理 ###############'''
'''##########################################'''

class AImageStackInline(object):
    model = ActivityImage
    extra = 0

class ATextStackInline(object):
    model = ActivityText
    extra = 0


@xadmin.sites.register(Activity)
class ActivityAdmin(object):
    '''活动信息管理'''
    list_display = ('activity_name',
                    'activity_type', 'activity_store', 'activity_start_datetime', 'activity_end_datetime', 'super_activity')
    search_fields = ('activity_name',)
    list_filter = ('activity_type', 'activity_store')
    date_hierarchy = ('activity_start_datetime', 'activity_end_datetime')
    list_per_page = 20
    # ordering = ('activity_start_datetime', 'activity_end_datetime')

    filter_horizontal = ('activity_store',)
    style_fields = {'activity_store': 'm2m_transfer'}
    inlines = [AImageStackInline, ATextStackInline]  # 关联子表

