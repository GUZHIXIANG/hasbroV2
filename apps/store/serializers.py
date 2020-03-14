from rest_framework import serializers
from .models import *


class StoreListSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='name')
    store_address = serializers.CharField(source='address')
    store_area = serializers.CharField(source='area')
    store_telephone = serializers.CharField(source='phone')

    class Meta:
        model = Store
        fields = ("id", "store_name",
                  "store_address",
                  "store_area",
                  "store_telephone")
