from rest_framework import serializers
from wechatapp.models.StoreModel import *


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ("id","store_name",
                  "store_address",
                  "store_area",
                  "store_telephone",
                  "store_longitude",
                  "store_latitude")


class StoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ("store_name",
                  "store_address",
                  "store_area",
                  "store_telephone",
                  "store_longitude",
                  "store_latitude")

    def create(self, validated_data):
        return Store.objects.create(**validated_data)



class StoreUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ("store_name",
                  "store_address",
                  "store_area",
                  "store_telephone",
                  "store_longitude",
                  "store_latitude")

    def update(self, instance, validated_data):
        for item in validated_data:
            if Store._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        instance.save()
        return instance
