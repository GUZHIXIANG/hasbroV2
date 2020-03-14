import xadmin
from xadmin import views

from .models import *


@xadmin.sites.register(Store)
class StoreAdmin(object):
    '''门店信息管理'''

    list_display = ('name', 'phone','address','area')
    search_fields = ('name', 'phone', 'address', 'area')
    list_filter = ('area',)
    list_editable = ('name', 'phone', 'address', 'area')
    show_detail_fields = ('name',)
    exclude = ('type',)

    list_per_page = 20

    def save_models(self):
        obj = self.new_obj
        obj.type = 2
        obj.save()

    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(type=2)
        return qs
