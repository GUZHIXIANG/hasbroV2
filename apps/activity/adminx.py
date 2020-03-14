import xadmin
from xadmin import views

from .models import *


@xadmin.sites.register(AType)
class ATypeAdmin(object):
    '''活动类型'''
    list_display = ('name', 'desc')
    search_fields = ('name', 'desc')
    list_editable = ('name', 'desc')
    list_per_page = 20


class ATextInline(object):
    model = AText
    extra = 0

@xadmin.sites.register(Activity)
class ActivityAdmin(object):
    '''活动信息管理'''

    list_display = ('name', 'atype','store',
                    "image_img", 'start_datetime', 'end_datetime')
    search_fields = ('name', 'atype','store', 'start_datetime', 'end_datetime')
    list_filter = ('atype',)
    list_editable = ('name', 'atype', 'start_datetime', 'end_datetime')
    show_detail_fields = ('name',)
    exclude = ('type',)
    filter_horizontal = ('store',)
    style_fields = {'store': 'm2m_transfer'}

    list_per_page = 20

    inlines = [ATextInline]

    def save_models(self):
        obj = self.new_obj
        obj.type = 3
        obj.save()

    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(type=3)
        return qs
