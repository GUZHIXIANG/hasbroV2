from django.db import models
from wechatapp.models.ProductModel import ProductBaseInfo
from stdimage.models import StdImageField


class AdvPicModel(models.Model):

    order = models.IntegerField('序号',primary_key=True)
    productbaseinfo = models.ForeignKey(ProductBaseInfo,on_delete=models.CASCADE,related_name="products")
    url = StdImageField(verbose_name='首页广告轮播图',upload_to='adv',variations={'product': {'width': 375, 'height': 400}},default='')


    def __str__(self):
        return self.url.__str__()

    class Meta:
        app_label = 'wechatapp'
        verbose_name = '广告轮播管理'
        verbose_name_plural = '广告轮播管理'
        ordering = ["order"]
    
    def image_img(self):
        if self.url:
            return str('<img src="%s" />' % self.url.product.url)

        else:
            return u'上传图片'

    image_img.short_description = '首页广告轮播图'
    image_img.allow_tags = True