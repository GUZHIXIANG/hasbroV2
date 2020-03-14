from django.db import models
# from django.contrib.auth.models import User
from user.models import UserProfile


# 行政区划表
class Areas(models.Model):
    id = models.CharField(verbose_name='行政编号', max_length=20, primary_key=True)
    name = models.CharField(verbose_name='行政区划名', max_length=20)
    parent_id = models.CharField(
        verbose_name='上级行政编号', max_length=20)
    type = models.IntegerField(verbose_name='行政等级',default=0)

    class Meta:
        db_table = 'wechatapp'
        verbose_name = 'Areas'
        verbose_name_plural = '行政区划表'

    def __unicode__(self):
        return self.name


# 收件地址信息表
class Address(models.Model):
    # 关联用户 ----- 关联用户信息表
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True,related_name='oldadress')
    # 联系人
    name = models.CharField(
        verbose_name='联系人', max_length=10, blank=True)
    # 手机号
    mobile = models.CharField(
        verbose_name='手机号', max_length=20, blank=True)
    # 关联地区 ----- 省份
    province = models.ForeignKey(
        Areas, on_delete=models.CASCADE,related_name='province')
    # 关联地区 ----- 城市
    city = models.ForeignKey(
        Areas, on_delete=models.CASCADE,related_name='city')
    # 关联地区 ----- 区域
    district = models.ForeignKey(
        Areas, on_delete=models.CASCADE,related_name='district')
    # 详细地址
    address = models.CharField(
        verbose_name='详细地址', max_length=256, blank=True)
    # 默认设置
    CHOICE_TYPE = ((False,'否'),(True,'是'))
    is_default = models.BooleanField(
        verbose_name='默认设置',choices=CHOICE_TYPE, default=False)
    # 创建时间
    signup_create_time = models.DateTimeField(
        verbose_name='创建时间', auto_now_add=True)
    # 操作时间
    signup_operate_time = models.DateTimeField(
        verbose_name='操作时间', auto_now=True)

    def __str__(self):
        return self.user_id.__str__()

    class Meta:
        app_label = 'wechatapp'
        verbose_name = 'Address'
        verbose_name_plural = '收件地址信息表'
