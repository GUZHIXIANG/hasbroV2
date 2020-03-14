from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# TODO(GU)  重写用户模型
class UserProfile(AbstractUser):
    '''用户信息'''
    type = models.IntegerField(verbose_name='类型',choices=((0,'后台'),(1,'小程序')),default=0)

    def __str__(self):
        return super().username.__str__()

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class UserManager(UserProfile):
    '''后台用户信息'''

    def __str__(self):
        return super().username.__str__()

    class Meta:
        verbose_name = '后台用户信息'
        verbose_name_plural = verbose_name
        proxy = True



class UserWechat(UserProfile):
    '''用户信息'''
    unionid = models.CharField(verbose_name='用户唯一标识',
        max_length=255, unique=True,  blank=True, null=True)
    nickName = models.CharField(verbose_name="昵称", max_length=20)
    age = models.IntegerField(verbose_name="年龄",blank=True,null=True)
    GENDER_CHOICES = ((0, '女'),(1, '男'))
    gender = models.IntegerField(verbose_name="性别",choices=GENDER_CHOICES, default=1)
    avatarUrl = models.CharField(verbose_name="头像路径",max_length=255, default="",null=True, blank=True)
    phone = models.CharField(verbose_name = "手机号",max_length=20,blank=True, null=True)
    country = models.CharField(verbose_name="所在国家", max_length=64, blank=True)
    province = models.CharField(verbose_name="所在省份", max_length=64, blank=True)
    city = models.CharField(verbose_name="所在城市", max_length=64, blank=True)
    language = models.CharField(verbose_name="语言", max_length=64, blank=True)

    def __str__(self):
        return super().username.__str__()

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def image_img(self):
        if self.avatarUrl:
            return str('<img src="%s" />' % self.avatarUrl)
        else:
            return u'上传图片'
    image_img.short_description = '微信头像'
    image_img.allow_tags = True
