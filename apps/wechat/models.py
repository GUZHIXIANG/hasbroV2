from django.db import models
from stdimage.models import StdImageField
from area.models import Areas
# TODO(GU)  重写用户模型
from user.models import UserProfile


class Entity(models.Model):
    '''实体信息'''
    name = models.CharField(verbose_name='名称',max_length=20)
    TYPE_CHOICES = ((1,'商品'),(2,'门店'),(3,'活动'))
    type = models.IntegerField(verbose_name='类型',choices=TYPE_CHOICES)
    # type = models.ForeignKey(EType,verbose_name='类型',on_delete=models.CASCADE,related_name='entity')
    desc = models.CharField(
        verbose_name='描述', max_length=50, blank=True, null=True)
    create_time = models.DateTimeField(
        verbose_name='创建时间', auto_now_add=True)
    operate_time = models.DateTimeField(
        verbose_name='操作时间', auto_now=True)

    def __str__(self):
        return '[{}] - {}'.format(self.get_type_display().__str__(), self.name.__str__())

    class Meta:
        verbose_name = '实体信息'
        verbose_name_plural = verbose_name


class Advert(models.Model):
    '''广告信息'''
    entity = models.ForeignKey(Entity,verbose_name='广告对象',related_name='advert',on_delete=models.CASCADE,blank=False)
    image = StdImageField(verbose_name='图片路径', upload_to='Advert', variations={
                          'nail': {'width': 375, 'height': 400}}, default='')
    desc = models.CharField(verbose_name='备注',max_length=20, blank=True, null=True)
    order = models.IntegerField(verbose_name='序号',blank=False)
    SHOW_CHOICES = ((True,'是'),(False,'否'))
    is_show = models.BooleanField(verbose_name='是否显示', choices=SHOW_CHOICES,default=False)

    def __str__(self):
        return self.image.__str__()


    class Meta:
        verbose_name = '首页广告'
        verbose_name_plural = verbose_name
        ordering = ["order"]

    def image_img(self):
        if self.image:
            return str(u'<img src="%s" />' % self.image.nail.url)

        else:
            return u'上传图片'

    image_img.short_description = '首页广告轮播图'
    image_img.allow_tags = True


class Trolly(models.Model):
    from product.models import PInfo

    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="trolly", verbose_name="用户")
    pinfo = models.ForeignKey(
        PInfo, on_delete=models.CASCADE, related_name="trolly", verbose_name="加购商品")
    nums = models.IntegerField(blank=False, default=1, verbose_name="加购数量")
    CHECK_CHOICES = ((False, '否'), (True, '是'))
    checkbox = models.BooleanField(choices=CHECK_CHOICES, default=False,verbose_name='是否选择')

    def __str__(self):
        return self.user.__str__()

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name


class Address(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False, related_name='address')
    name = models.CharField(verbose_name='联系人', max_length=10, blank=False)
    phone = models.CharField(verbose_name='手机号', max_length=20, blank=False)
    province = models.ForeignKey(
        Areas, on_delete=models.CASCADE, related_name='province',verbose_name='省份')
    city = models.ForeignKey(
        Areas, on_delete=models.CASCADE, related_name='city', verbose_name='城市')
    district = models.ForeignKey(
        Areas, on_delete=models.CASCADE, related_name='district', verbose_name='区域')
    address = models.CharField(
        verbose_name='详细地址', max_length=256, blank=False)
    TYPE_CHOICES = ((False, '否'), (True, '是'))
    is_default = models.BooleanField(
        verbose_name='默认设置', choices=TYPE_CHOICES, default=False)

    def __str__(self):
        return self.user.name.__str__()

    class Meta:
        verbose_name = '收件地址'
        verbose_name_plural = verbose_name



class Join(models.Model):
    from activity.models import Activity
    from store.models import Store

    activity = models.ForeignKey(Activity,on_delete=models.CASCADE,related_name='join',verbose_name='报名活动',blank=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE,
    related_name='join', verbose_name='所选门店', blank=False)
    user = models.ForeignKey(
        UserProfile, related_name='join', on_delete=models.CASCADE, blank=False, verbose_name='用户')
    name = models.CharField(
        verbose_name='参与者姓名', max_length=30, blank=True, null=True)
    phone = models.CharField(
    verbose_name='参与者电话', max_length=20, blank=True,null=True)

    def __str__(self):
        return '{} - {}'.format(self.activity.name, self.user.name)

    class Meta:
        verbose_name = '报名信息'
        verbose_name_plural = verbose_name
