from rest_framework import serializers
from wechatapp.models.ProductTypeModel import *


# class ProductSecondCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductSecondCategory
#         fields = "__all__"

# class ProductTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductType
#         fields = "__all__"

# class ProductMainCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductMainCategory
#         fields = "__all__"


'''#######################################'''


class PTypePosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PTypePoster
        fields = '__all__'

class PTypeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PTypeImage
        fields = '__all__'


class PTypeSerializer(serializers.ModelSerializer):

    desc = serializers.SerializerMethodField()
    # url = serializers.CharField(source='type_image.image')
    # banner_url = serializers.CharField(source='type_poster.image')
    banner_name = serializers.CharField(source='type_poster.text')
    typeChildName = serializers.SerializerMethodField()
    typeName = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    banner_url = serializers.SerializerMethodField()

    class Meta:
        model = PType
        fields = ('id', 'typeName', 'typeChildName', 'desc',
                  'url', 'banner_url', 'banner_name')

    def get_url(self,obj):
        if PTypeImage.objects.filter(ptype=obj).exists():
            return '/media/'+PTypeImage.objects.get(ptype=obj).image.__str__()
        else:
            return None

    def get_banner_url(self, obj):
        if PTypePoster.objects.filter(ptype=obj).exists():
            return '/media/'+PTypePoster.objects.get(ptype=obj).image.__str__()
        else:
            return None

    def get_typeChildName(self,obj):
        return obj.name

    def get_typeName(self, obj):
        p = obj.parent
        if p:
            return p.id
        else:
            return None
    
    def get_desc(self, obj):
        return obj.get_desc_display()

    
