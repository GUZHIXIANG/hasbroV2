# from django.db import models
# from django.contrib.auth.models import User
# from user.models import UserProfile
# # Create Extened UserProfile for more information

# class UserProfile(models.Model):
    
#     # 外表关联 主表是内建用户生成表
#     user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile',verbose_name='微信ID')

#     # unionid 是微信上用户的 unionid
#     unionid = models.CharField(max_length=255,unique=True, verbose_name='unionid',blank=True,null=True)
    
#     nickName = models.CharField("昵称",max_length=100)
#     USER_GENDER_CHOICES = (
#                            (0,'女'),
#                            (1,'男'),
#                            )
    
#     gender = models.SmallIntegerField(choices=USER_GENDER_CHOICES,
#                                    default=1,
#                                    verbose_name="性别")
    
    
#     avatarUrl = models.CharField(max_length=255,default="", 
#                               null=True, blank=True,
#                               verbose_name="头像")
    
#     phone = models.BigIntegerField(blank=True,null=True)
    
#     country = models.CharField(max_length=64,blank=True)
    
#     province = models.CharField(max_length=64,blank=True)
    
#     city = models.CharField(max_length=64, blank=True, verbose_name="所在城市")
    
#     language = models.CharField(max_length=64,blank=True)
   
#     def __str__(self):
#         return self.user.__str__()

#     class Meta:
#         app_label = 'wechatapp'
#         verbose_name = '小程序用户'
#         verbose_name_plural = '小程序用户查看'

#     def image_img(self):
#         if self.avatarUrl:
#             return str('<img src="%s" />' % self.avatarUrl)
#         else:
#             return u'上传图片'

#     image_img.short_description = '头像'
#     image_img.allow_tags = True
