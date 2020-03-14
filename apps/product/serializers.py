from rest_framework import serializers
from .models import *

# XXX(GU)  应当禁用
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class PBannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = PBanner
        fields = ("image",)

# TODO(GU)  更名，结构有变，需通知前端
class ProductListSerializer(serializers.ModelSerializer):
    # prices = serializers.SlugRelatedField(many=True,read_only=True,slug_field='price')
    smallurl = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_smallurl(self,obj):
        if obj.image:
            return '/media/' + obj.image.__str__()
        else:
            return None

    def get_price(self,obj):
        pinfos = obj.pinfo.all()
        if pinfos:
            return min([x.price for x in pinfos])
        else:
            return None
    
    class Meta:
        model = Product
        fields = ("productId", "name", "smallurl", "price",'ptype')

# TODO(GU)  结构有变，需通知前端
class ProductDetailSerializer(serializers.ModelSerializer):
    url = PBannerSerializer(many=True)
    details = serializers.SerializerMethodField()

    def get_details(self,obj):
        query_set = obj.pinfo.all()
        details = [{'color': x.color, 
                    'norms': x.norms, 
                    'weight': x.weight, 
                    'price': x.price, 
                    'quantity': x.quantity, 
                    'image': x.image
                    }for x in query_set]
        return details

    class Meta:
        model = Product
        fields = ('id',"productId", "name", "url","details")



class PTypeSerializer(serializers.ModelSerializer):

    desc = serializers.SerializerMethodField()
    banner_name = serializers.SerializerMethodField()
    typeChildName = serializers.CharField(source='name')
    typeName = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    banner_url = serializers.SerializerMethodField()

    class Meta:
        model = PType
        fields = ('id', 'typeName', 'typeChildName', 'desc',
                  'url', 'banner_url', 'banner_name')

    def get_url(self, obj):
        if PTypeImage.objects.filter(ptype=obj).exists():
            return '/media/'+PTypeImage.objects.get(ptype=obj).image.__str__()
        else:
            return None

    def get_banner_name(self, obj):
        if PTypePoster.objects.filter(ptype=obj).exists():
            return PTypePoster.objects.get(ptype=obj).text.__str__()
        else:
            return None

    def get_banner_url(self, obj):
        if PTypePoster.objects.filter(ptype=obj).exists():
            return '/media/'+PTypePoster.objects.get(ptype=obj).image.__str__()
        else:
            return None

    def get_typeName(self, obj):
        p = obj.parent
        if p:
            return p.id
        else:
            return None

    def get_desc(self, obj):
        return obj.get_desc_display()
