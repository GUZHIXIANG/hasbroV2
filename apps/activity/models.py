from django.db import models
from wechat.models import Entity
from store.models import Store
from django.utils import timezone
from stdimage.models import StdImageField
# Create your models here.


class AType(models.Model):
    name = models.CharField(
        verbose_name='类型', max_length=10, unique=True)
    desc = models.CharField(
        verbose_name='描述', max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name.__str__()

    class Meta:
        verbose_name = '活动类型'
        verbose_name_plural = verbose_name


class Activity(Entity):
    atype = models.ForeignKey(
        AType, on_delete=models.CASCADE, blank=False, verbose_name='活动类型')
    store = models.ManyToManyField(
        Store, verbose_name='活动门店',blank=True,related_name='activity')
    image = StdImageField(verbose_name="图片路径", upload_to='Activity/image', variations={
        'nail': {'width': 100, 'height': 75}}, default='',blank=True)
    start_datetime = models.DateTimeField(
        verbose_name='开始时间', default=timezone.now)
    end_datetime = models.DateTimeField(
        verbose_name='结束时间', default=timezone.now)

    def __str__(self):
        return super().name.__str__()

    class Meta:
        verbose_name = '活动信息'
        verbose_name_plural = verbose_name

    def image_img(self):
        if self.image:
            return str('<img src="%s" />' % self.image.nail.url)
        else:
            return u'上传图片'

    image_img.short_description = '预览图'
    image_img.allow_tags = True



class AText(models.Model):
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name='atext', verbose_name='活动')
    title = models.CharField(
        verbose_name='标题', max_length=50)
    text = models.TextField(verbose_name='正文')

    def __str__(self):
        return self.title.__str__()

    class Meta:
        verbose_name = '活动文本'
        verbose_name_plural = verbose_name
