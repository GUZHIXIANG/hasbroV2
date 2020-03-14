from django.db import models
from wechat.models import Entity
from stdimage.models import StdImageField

# Create your models here.

class PType(models.Model):
    '''商品类型'''
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='父类型')
    name = models.CharField(
        verbose_name='类型', max_length=20, unique=True)
    CHOICES = ((1, '一级分类'), (2, '二级分类'), (3, '三级分类'))
    desc = models.IntegerField(
        verbose_name='属性', choices=CHOICES, blank=True,null=True)


    def __str__(self):
        return self.name.__str__()

    class Meta:
        verbose_name = '商品类型'
        verbose_name_plural = verbose_name


class PTypeImage(models.Model):
    '''商品类型图标'''
    ptype = models.OneToOneField(
        PType, on_delete=models.CASCADE, related_name='ptimage', verbose_name='类型', default=1)
    image = StdImageField(verbose_name="图片路径", upload_to='PType/image/', variations={
                          'nail': (10, 10), 'medium': (20, 20)}, default='')

    def __str__(self):
        return self.image.__str__()

    class Meta:
        verbose_name = '商品类型图标'
        verbose_name_plural = verbose_name

    def image_nail(self):
        if self.image:
            return str(u'<img src="%s" />' % self.image.nail.url)
        else:
            return u'上传图片'

    image_nail.short_description = '缩略图'
    image_nail.allow_tags = True

    def image_medium(self):
        if self.image:
            return str(u'<img src="%s" />' % self.image.medium.url)
        else:
            return u'上传图片'

    image_medium.short_description = '中号图'
    image_medium.allow_tags = True


class PTypePoster(models.Model):
    '''商品类型海报'''
    ptype = models.OneToOneField(
        PType, on_delete=models.CASCADE, related_name='ptposter', verbose_name='商品类型', default=1)
    image = StdImageField(verbose_name="图片路径", upload_to='PType/poster/', variations={
                          'large': (100, 75)}, default='')
    text = models.CharField(verbose_name='配文',
                            max_length=50, blank=False, default='')

    def __str__(self):
        return self.image.__str__()

    class Meta:
        verbose_name = '商品类型海报'
        verbose_name_plural = verbose_name

    def image_large(self):
        if self.image:
            return str(u'<img src="%s" />' % self.image.large.url)
        else:
            return u'上传图片'

    image_large.short_description = '效果图'
    image_large.allow_tags = True



class Product(Entity):
    '''商品信息'''
    ptype = models.ForeignKey(
        PType, on_delete=models.CASCADE, verbose_name='商品分类', blank=False, default=1, related_name="product")
    # 货号
    productId = models.CharField(verbose_name='货号', max_length=100)
    # 系统编码
    systemCode = models.BigIntegerField(
        verbose_name='系统编码', blank=True, null=True)
    # 条形编码
    barCode = models.BigIntegerField(
        verbose_name='条形编码', blank=True, null=True)
    # 品牌
    brand = models.CharField(verbose_name='品牌',max_length=30, blank=True, null=True)
    # 商品简介
    brief = models.TextField(
        verbose_name='商品简介', blank=True, null=True)
    # 缩略图
    image = StdImageField(verbose_name="图片路径", upload_to='Product/preview/', variations={
                             'nail': {'width': 100, 'height': 75}}, blank=True, default='')

    SHELL_CHOICES = (('on', '上架'), ('off', '下架'))
    shell = models.CharField(
        verbose_name='货架', max_length=3, choices=SHELL_CHOICES, default='on', blank=False)

    def __str__(self):
        return super().name.__str__()

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def image_preview(self):
        if self.image:
            return str(u'<img src="%s" />' % self.image.nail.url)
        else:
            return u'上传图片'

    image_preview.short_description = '预览图'
    image_preview.allow_tags = True


class PInfo(models.Model):
    '''商品详情'''
    product = models.ForeignKey(
        Product, related_name='pinfo', verbose_name='商品', null=True, blank=True,on_delete=models.CASCADE)
    color = models.CharField(
        verbose_name='颜色', max_length=255, blank=True, null=True)
    norms = models.CharField(
        verbose_name='规格', max_length=255, blank=True, null=True)
    weight = models.IntegerField(verbose_name='重量', blank=True, null=True)
    price = models.IntegerField(verbose_name='价格', blank=False)
    image = StdImageField(verbose_name="图片路径", upload_to='Product/detail/', variations={
        'nail': {'width': 100, 'height': 75}}, blank=True, default='')
    quantity = models.IntegerField(
        verbose_name="虚拟库存", blank=True, default=10)

    class Meta:
        verbose_name = '商品详情'
        verbose_name_plural = verbose_name


    def image_detail(self):
        if self.image:
            return str(u'<img src="%s" />' % self.image.nail.url)
        else:
            return u'上传图片'

    image_detail.short_description = '效果图'
    image_detail.allow_tags = True



class PTag(models.Model):
    '''商品标签'''
    name = models.CharField(verbose_name='名称', max_length=10,unique=True)
    desc = models.CharField(
        verbose_name='描述', max_length=50, null=True, blank=True)
    product = models.ManyToManyField(
        Product, related_name='ptag', verbose_name='标注商品', blank=True)

    def __str__(self):
        return self.name.__str__()

    class Meta:
        verbose_name = '商品标签'
        verbose_name_plural = verbose_name


class PBanner(models.Model):
    '''商品轮播图'''
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="pbanner", verbose_name='商品')
    image =  StdImageField(verbose_name='图片路径',upload_to='Product/banner/',variations={'nail': {'width': 375, 'height': 400}},default='')

    def __str__(self):
        return self.image.__str__()

    class Meta:
        verbose_name = '商品轮播图'
        verbose_name_plural = verbose_name

    def image_banner(self):
        if self.image:
            return str(u'<img src="%s" />' % self.image.nail.url)
        else:
            return u'上传图片'

    image_banner.short_description = '效果图'
    image_banner.allow_tags = True
