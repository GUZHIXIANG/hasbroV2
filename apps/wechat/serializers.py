from rest_framework import serializers
from .models import *
from product.models import Product
import re

# TODO(GU)  更名
class AddressOperateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ("id", "user", "name", "phone", "province",
                  "city", "district", "address", "is_default")

    def create(self, validate_data):
        return Address.objects.create(**validate_data)

    def update(self, instance, validated_data):
        for item in validated_data:
            if Address._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        instance.save()
        return instance

    def validate(self, attrs):
        attrs_ = attrs.copy()
        attrs_.pop('is_default')
        if Address.objects.filter(**attrs_).exists():
            raise serializers.ValidationError('该地址已存在')
        return attrs

    def validate_name(self, value):
        res = re.search(r'[^\w\s]', value)
        if res:
            raise serializers.ValidationError('姓名中不得存在特殊符号')
        return value

# TODO(GU)  更名
class AddressDetailSerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source='province.name')
    city_name = serializers.CharField(source='city.name')
    district_name = serializers.CharField(source='district.name')

    class Meta:
        model = Address
        fields = ("id", "name", "phone", "province", "city", "district",
                  "province_name", "city_name", "district_name", "address", "is_default")


# TODO(GU)  更名，结构有变，需通知前端
class TrollyListSerializer(serializers.ModelSerializer):
    productInfo = serializers.SerializerMethodField()

    def get_productInfo(self, obj):
        res = {}
        query_set = obj.pinfo.all()
        for x in query_set:
            res['color'] = x.color
            res['norms'] = x.norms
            res['weight'] = x.weight
            res['price'] = x.price
            res['quantity'] = x.quantity
            res['image'] = '/media/' + x.image.__str__()
            res['id'] = x.id

            base = x.product
            res['ptype_id'] = base.ptype
            res['ptype'] = base.ptype.name
            res['productId'] = base.productId
            res['name'] = base.name

        return res

    class Meta:
        model = Trolly
        fields = ("productInfo", "nums", "checkbox")


# TODO(GU)  更名
class JoinListSerializer(serializers.ModelSerializer):
    activity_name = serializers.CharField(
        source='activity.name')
    activity_start_datetime = serializers.DateTimeField(
        source='activity.start_datetime', format='%Y-%m-%d %H:%M')
    activity_end_datetime = serializers.DateTimeField(
        source='activity.end_datetime', format='%Y-%m-%d %H:%M')
    store_name = serializers.CharField(
        source='store.name')
    store_address = serializers.CharField(
        source='store.address')

    class Meta:
        model = Join
        fields = ("id", "activity_id", "activity_name",
                  "activity_start_datetime", "activity_end_datetime",
                  "store_id", "store_name", "store_address",
                  "signup_name", "signup_phone")


# TODO(GU)  更名，结构有变，需通知前端
class JoinOperateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Join
        fields = ('activity','store','user','name','phone')

    def create(self, validated_data):
        return Join.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        for item in validated_data:
            if Join._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        instance.save()
        return instance


    def validate(self, attrs):
        if Join.objects.filter(**attrs).exists():
            raise serializers.ValidationError('该成员已报名')
        return attrs

    def validate_name(self, value):
        res = re.search(r'[^\w\s]', value)
        if res:
            raise serializers.ValidationError('姓名中不得存在特殊符号')
        return value


# TODO(GU)  结构有变，需通知前端
class AdvertListSerializer(serializers.ModelSerializer):
    eid = serializers.CharField(source='entity.id')
    ename = serializers.CharField(source='entity.name')
    ekeyword = serializers.SerializerMethodField()

    def get_ekeyword(self, obj):
        etype_type = obj.entity.get_type_display()
        if etype_type == '商品':
            return 'product'
        elif etype_type == '活动':
            return 'activity'
        elif etype_type == '门店':
            return 'store'
        else:
            return None
    

    class Meta:
        model = Advert
        fields = ('ekeyword', 'eid', 'ename',
                  'image', 'order', 'is_show')
