from django.db import models
from wechat.models import Entity

# Create your models here.


class Store(Entity):
    '''门店信息'''
    phone = models.CharField(
        verbose_name='电话', max_length=20, blank=False)
    address = models.CharField(verbose_name='地址', max_length=100, blank=False)
    area = models.CharField(
        verbose_name='所在商区', max_length=20, blank=True,null=True)
    longlat = models.CharField(
        verbose_name='经纬度', max_length=100, blank=True,null=True)

    def __str__(self):
        return super().name.__str__()


    class Meta:
        verbose_name = '门店信息'
        verbose_name_plural = verbose_name
