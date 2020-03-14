from rest_framework import serializers
from wechatapp.models.TrollyModel import MyTrolly
from wechatapp.models.ProductModel import ProductBaseInfo


class ProductItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBaseInfo
        fields = "__all__"

class TrollyAllSerializer(serializers.ModelSerializer):
    productbaseinfo = ProductItemsSerializer(read_only=True)
    #total_item_prices_sum = serializers.SerializerMethodField()
    class Meta:
        model = MyTrolly
        fields = ("productbaseinfo","nums","checkbox")
    
    # def get_total_item_prices_sum(self,obj):
    #     result = []
        
    #     #print(obj)
    #     return result