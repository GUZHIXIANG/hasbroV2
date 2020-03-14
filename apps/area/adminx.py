import xadmin
from xadmin import views

from .models import *


@xadmin.sites.register(Areas)
class AreasAdmin(object):
    '''门店信息管理'''

    list_display = ('id', 'name','parent_id','type')
    search_fields = ('id', 'name', 'parent_id', 'type')
    list_filter = ('type',)

    list_per_page = 20