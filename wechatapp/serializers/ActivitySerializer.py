from rest_framework import serializers
from wechatapp.models.ActivityModel import *

class ActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityImage
        fields = ('image', 'image_type')

class ActivityTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityText
        fields = ('title', 'text')


class ActivitySerializer(serializers.ModelSerializer):
    activity_start_datetime = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M')
    activity_end_datetime = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M')
    activity_type = serializers.CharField(
        source='activity_type.activity_type')

    activity_image = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = '__all__'

    def get_activity_image(self, obj):
        query_set = obj.activity_image.all()
        return [{'image': '/media/'+obj.image.__str__(), 'image_description': obj.image_description, 'image_type': obj.get_image_type_display()} for obj in query_set]


class ActivityDetailSerializer(serializers.ModelSerializer):
    activity_start_datetime = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M')
    activity_end_datetime = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M')
    activity_type = serializers.CharField(
        source='activity_type.activity_type')

    activity_image = serializers.SerializerMethodField()
    activity_text = serializers.SerializerMethodField()
    activity_store = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = "__all__"

    def get_activity_image(self, obj):
        query_set = obj.activity_image.all()
        return [{'image': '/media/'+obj.image.__str__(), 'image_description': obj.image_description, 'image_type': obj.get_image_type_display()} for obj in query_set]
    
    def get_activity_text(self, obj):
        query_set = obj.activity_text.all()
        return [{'title': obj.title, 'text': obj.text} for obj in query_set]

    def get_activity_store(self, obj):
        query_set = obj.activity_store.all()
        return [{'store_id': obj.id, 'store_name': obj.store_name, 
        'store_area': obj.store_area,'store_address': obj.store_address, 'store_telephone': obj.store_telephone,} for obj in query_set]
