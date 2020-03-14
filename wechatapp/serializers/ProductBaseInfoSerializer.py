from rest_framework import serializers
from wechatapp.models.ProductModel import *




class ProductSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = ProductBaseInfo
        fields = "__all__"
    #     fields = ('productId','productName','productType','systemCode','barCode','color','norms','weight','price','descripation')
    
    # def create(self, validated_data):
    #     productType = validated_data.pop('productTyper')
    #     ptype = ProductType.objects.get(typeName=productType)
    #     product = ProductBaseInfo.objects.create(productType=ptype,**validated_data)
    #     product.save()
    #     return product

class ProductUrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductUrl
        fields = ("url",)



# class ProductTagSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ProductTag
#         fields = ("tag",)


class PTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = PTag
        fields = "__all__"


class ProductAllSerializer(serializers.ModelSerializer):
    #url = serializers.StringRelatedField(many=True)
    class Meta:
        model = ProductBaseInfo
        fields = ("productId","productName","smallurl","price")

    
 
class ItemsAllSerializer(serializers.ModelSerializer):
    url = serializers.StringRelatedField(many=True)
    class Meta:
        model = ProductBaseInfo
        fields = ("productId","productName","url","price",'color','norms','weight','descripation','shell',"quantity")


class ProductSerializer2(serializers.ModelSerializer):
    # serializers.CharField(source='productType.parent')
    parent_type = serializers.SerializerMethodField()
    class Meta:
        model = ProductBaseInfo
        fields = "__all__"#("productId", "productName", "smallurl", "price")

    def get_parent_type(self,obj):
        p = obj.productType.parent
        if p:
            return p.id
        else:
            return None
