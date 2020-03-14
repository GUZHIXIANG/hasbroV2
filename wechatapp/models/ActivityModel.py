from django.db import models
from django.utils import timezone
from stdimage.models import StdImageField
from wechatapp.models.StoreModel import Store
 


# 活动信息表
class Activity(models.Model):
    # 父活动 ----- 自关联
    super_activity = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True,verbose_name='父活动')
    # 活动名
    activity_name = models.CharField(
        verbose_name='活动名', max_length=100, unique=True)
    # 活动类型 ----- 关联活动类型表
    activity_type = models.ForeignKey(
        'ActivityType', on_delete=models.CASCADE, default=1,verbose_name='活动类型')
    # 活动描述
    activity_descripation = models.TextField(verbose_name='活动描述', blank=True)
    # 关联门店 ----- 关联门店信息表
    # activity_store = models.ManyToManyField(
    #     Store, through='ActivityStore',verbose_name='活动门店')
    activity_store = models.ManyToManyField(
        Store, verbose_name='活动门店',null=True,blank=True)
    # 活动开始时间
    activity_start_datetime = models.DateTimeField(
        verbose_name='开始时间', default=timezone.now)
    # 活动结束时间
    activity_end_datetime = models.DateTimeField(
        verbose_name='结束时间', default=timezone.now)
    # 创建时间
    activity_create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    # 操作时间
    activity_operate_time = models.DateTimeField(verbose_name='操作时间',auto_now=True)

    def __str__(self):
        return self.activity_name.__str__()

    __unicode__ = __str__

    class Meta:
        app_label = 'wechatapp'
        verbose_name = '活动信息'
        verbose_name_plural = '活动信息管理'


# 活动类型表
class ActivityType(models.Model):
    # 活动类型
    activity_type = models.CharField(verbose_name='活动类型',max_length=16,unique=True)
    # 类型描述
    type_description = models.CharField(
        verbose_name='类型描述', max_length=100,null=True,blank=True)

    def __str__(self):
        return self.activity_type.__str__()

    __unicode__ = '__str__'

    class Meta:
        app_label = 'wechatapp'
        verbose_name = '活动类型'
        verbose_name_plural = '活动类型管理'

# 活动图片表
class ActivityImage(models.Model):
    # 关联活动 ----- 关联活动基础表
    activity = models.ForeignKey('Activity',on_delete=models.CASCADE,related_name='activity_image')
    # 活动图片
    image = StdImageField(verbose_name="活动图片", upload_to='ActivityPoster', variations={
                          'nail': {'width': 100, 'height': 75}}, default='')
    # 图片描述
    image_description = models.CharField(
        verbose_name='图片描述', max_length=100, null=True, blank=True)
    # 图片类型
    IMAGE_TYPE = ((1, 'type1'),(2, 'type2'),(3, 'type3'))
    image_type = models.IntegerField(verbose_name='图片类型',choices=IMAGE_TYPE,default=1)

    def __str__(self):
        return self.image.__str__()

    __unicode__ = '__str__'

    class Meta:
        app_label = 'wechatapp'
        verbose_name = '活动图片'
        verbose_name_plural = '活动图片管理'

    def image_img(self):
        if self.image:
            return str('<img src="%s" />' % self.image.nail.url)
        else:
            return u'上传图片'

    image_img.short_description = '活动海报'
    image_img.allow_tags = True


# 活动文本表
class ActivityText(models.Model):
    # 关联活动 ----- 关联活动基础表
    activity = models.ForeignKey('Activity',on_delete=models.CASCADE,related_name='activity_text')
    # 文本标题
    title = models.CharField(
        verbose_name='文本标题', max_length=100)
    # 文本正文
    text = models.TextField(verbose_name='文本正文')

    def __str__(self):
        return self.title.__str__()

    __unicode__ = '__str__'

    class Meta:
        app_label = 'wechatapp'
        verbose_name = '活动文本'
        verbose_name_plural = '活动文本管理'
