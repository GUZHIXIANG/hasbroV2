from rest_framework import serializers
from wechatapp.models.AddressModel import *

class AddressDetailSerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source='province.name')
    city_name = serializers.CharField(source='city.name')
    district_name = serializers.CharField(source='district.name')

    class Meta:
        model = Address
        fields = ("id", "name", "mobile", "province", "city", "district",
                  "province_name", "city_name", "district_name", "address", "is_default")


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ("id","user","name","mobile","province","city","district","address","is_default")
    
    def create(self,validate_data):
        return Address.objects.create(**validate_data)
    
    def update(self, instance, validated_data):
        for item in validated_data:
            if Address._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        instance.save()
        return instance


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Areas
        fields = '__all__'
