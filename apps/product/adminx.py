import xadmin
from xadmin import views

from .models import *
from wechat.models import *


class PTypePosterInline(object):
    model = PTypePoster
    extra = 0


class PTypeImageInline(object):
    model = PTypeImage
    extra = 0


@xadmin.sites.register(PType)
class PTypeAdmin(object):
    '''商品类型'''
    list_display = ('name', 'parent', 'desc', 'full_name')
    search_fields = ('name', 'parent')
    list_editable = ('parent', 'desc')
    list_filter = ('parent', 'desc')
    list_per_page = 20

    def full_name(self, obj):
        fname = [obj.name.__str__()]
        tmp = obj.parent
        c = 0
        while tmp != None:
            if c > 10:  # 限制循环
                continue
            fname.append(tmp.name.__str__())
            tmp = tmp.parent
            c += 1
        return '|'.join(fname[::-1])
    full_name.short_description = '全称'

    inlines = [PTypePosterInline, PTypeImageInline]


@xadmin.sites.register(PTag)
class PtagAdmin(object):
    '''商品标签'''
    list_display = ('name', 'desc', 'product')
    search_fields = ('product__productId', 'product__productName',
                     'product__systemCode', 'product__barCode')
    filter_horizontal = ('product',)
    style_fields = {'product': 'm2m_transfer'}
    list_per_page = 20




class PBannerInline(object):
    model = PBanner
    extra = 0


class PInfoInline(object):
    model = PInfo
    extra = 0

@xadmin.sites.register(Product)
class ProductAdmin(object):
    '''商品信息管理'''

    def tag(self, obj):
        return '.'.join([x.name for x in obj.ptag.all()])
    tag.short_description = '标签'

    list_display = ('productId', 'name','ptype',"image_preview", 'tag', 'shell')
    search_fields = ('productId', 'name',
                     'systemCode', 'barCode')
    list_filter = ('ptype', 'shell')
    list_editable = ('shell',)
    show_detail_fields = ('productId',)
    exclude = ('type',)

    list_per_page = 20

    inlines = [PInfoInline,PBannerInline]

    def save_models(self):
        obj = self.new_obj
        obj.type = 1
        obj.save()
    
    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(type=1)
        return qs






