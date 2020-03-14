from django.db import models



# 门店信息表
class Store(models.Model):
    # 门店名
    store_name = models.CharField(verbose_name='门店名',max_length=255,unique=True)
    # 门店电话
    store_telephone = models.CharField(
        verbose_name='门店电话', max_length=100, blank=False)
    # 门店地址
    store_address = models.TextField(verbose_name='门店地址', blank=False)
    # 门店商区
    store_area = models.CharField(
        verbose_name='门店商区', max_length=100, blank=True)
    # 门店经纬度
    store_longitude = models.DecimalField(
        verbose_name='门店经度', max_digits=22, decimal_places=16, blank=True, null=True)
    store_latitude = models.DecimalField(
        verbose_name='门店纬度', max_digits=22, decimal_places=16, blank=True, null=True)
    # 创建时间
    store_create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    # 操作时间
    store_operate_time = models.DateTimeField(verbose_name='操作时间',auto_now=True)
    
    def __str__(self):
        return self.store_name.__str__()

    __unicode__ = __str__

    class Meta:
        app_label = 'wechatapp'
        verbose_name = '门店信息'
        verbose_name_plural = '门店信息管理'
