from django.db import models
from datetime import datetime
from stdimage.models import StdImageField
from wechatapp.models.ProductTypeModel import *

# 商品基础信息表
class ProductBaseInfo(models.Model):

    CHOOSE = (
        ('on','上架'),
        ('off','下架'),
    )

    # 货号 ------- 主键
    productId = models.CharField(
        verbose_name='货号', max_length=100, primary_key=True)
    # 品名
    productName = models.CharField(verbose_name='商品名称', max_length=255)
    # 分类 ------- 关联类目信息
    productType = models.ForeignKey(
        PType, on_delete=models.CASCADE, verbose_name='商品分类',blank=False,default=1,related_name="product")
    # 系统编码
    systemCode = models.BigIntegerField(verbose_name='系统编码', blank=True,null=True)
    # 条形编码
    barCode = models.BigIntegerField(verbose_name='条形编码', blank=True,null=True)
    # 颜色
    color = models.CharField(verbose_name='颜色', max_length=255, blank=True,null=True)
    # 规格
    norms = models.CharField(verbose_name='规格', max_length=255, blank=True,null=True)
    # 重量
    weight = models.IntegerField(verbose_name='重量', blank=True,null=True)
    # 价格  
    price = models.IntegerField(verbose_name='价格', blank=False)
    
    # 商品详情
    description = models.TextField(verbose_name='商品详情', blank=True,null=True)
    # 商品简介
    brief = models.TextField(
        verbose_name='商品简介', blank=True, default="这里是商品简介")
    # 品牌
    brand = models.TextField(verbose_name='品牌', blank=True, default="这里是商品牌")

    # 缩略图
    smallurl = StdImageField(verbose_name="图片路径",upload_to='ProductPreViewPic',variations={'nail': {'width': 100, 'height': 75}},blank=True,default='')
    
    quantity = models.IntegerField(
        verbose_name="虚拟库存", blank=True, default=500)

    shell = models.CharField(
        verbose_name='货架', max_length=3, choices=CHOOSE, default='on', blank=False)
    
    
    
    def __str__(self):
        return self.productId.__str__()+"["+self.productName.__str__()+"]"+"("+self.norms.__str__()+")"

    class Meta:
        app_label = 'wechatapp'
        verbose_name = '商品详情'
        verbose_name_plural = '商品详情管理'

    def image_img(self):
        if self.smallurl:
            return str('<img src="%s" />' % self.smallurl.nail.url)
        else:
            return u'上传图片'

    image_img.short_description = '效果图'
    image_img.allow_tags = True

    
# 商品图片链接表  多个图片链接关联到一个商品上
class ProductUrl(models.Model):

    # 外键关联了
    productbaseinfo = models.ForeignKey(
        ProductBaseInfo, on_delete=models.CASCADE, related_name="url", verbose_name='商品')

    # 图片链接
    url = StdImageField(verbose_name='图片路径',upload_to='img',variations={'product': {'width': 375, 'height': 400}},default='')

    def __str__(self):
        return self.url.__str__()

    class Meta:
        app_label = 'wechatapp'
        verbose_name = '商品详情图片'
        verbose_name_plural = '商品详情图片管理'
    
    def image_img(self):
        if self.url:
            return str('<img src="%s" />' % self.url.product.url)
        else:
            return u'上传图片'

    image_img.short_description = '效果图'
    image_img.allow_tags = True

# class ProductTag(models.Model):

#     tag_type = (
#         ('h', '热门商品'),
#         ('d', '降价促销'),
#         ('n', '新品上架'),
#     )

#     # 外键关联了
#     productbaseinfo = models.OneToOneField(ProductBaseInfo,on_delete=models.CASCADE,primary_key=True)
    
#     # 标签
#     tag = models.CharField(max_length=1, choices=tag_type)

#     def __str__(self):
#         return self.tag.__str__()

#     class Meta:
#         app_label = 'wechatapp'
#         verbose_name = '商品标签管理'
#         verbose_name_plural = '商品标签管理'


'''#######################################'''


class PTag(models.Model):
    '''商品标签'''
    name = models.CharField(verbose_name='标签名称',max_length=10)
    description = models.CharField(verbose_name='标签描述', max_length=100)
    product = models.ManyToManyField(
        ProductBaseInfo, related_name='tags', verbose_name='标注商品', null=True, blank=True)

    def __str__(self):
        return self.name.__str__()

    class Meta:
        app_label = 'wechatapp'
        verbose_name = '商品标签*'
        verbose_name_plural = '商品标签管理*'
