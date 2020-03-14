from rest_framework import serializers
from .models import *

# TODO(GU)  更名，结构有变，需通知前端
class ActivityListSerializer(serializers.ModelSerializer):
    activity_start_datetime = serializers.DateTimeField(source='start_datetime',format='%Y-%m-%d %H:%M')
    activity_end_datetime = serializers.DateTimeField(source='end_datetime',format='%Y-%m-%d %H:%M')
    activity_type = serializers.CharField(source='atype.name')
    activity_image = serializers.SerializerMethodField() 
    activity_name = serializers.CharField(source='name')
    # activity_id = serializers.CharField(source='id')

    def get_activity_image(self,obj):
        return '/media/' + obj.image.__str__()

    class Meta:
        model = Activity
        fields = ('id', 'activity_name','activity_image',
                  'activity_type', 'activity_start_datetime', 'activity_end_datetime')

# TODO(GU)  结构有变，需通知前端
class ActivityDetailSerializer(serializers.ModelSerializer):
    activity_start_datetime = serializers.DateTimeField(
        source='start_datetime', format='%Y-%m-%d %H:%M')
    activity_end_datetime = serializers.DateTimeField(
        source='end_datetime', format='%Y-%m-%d %H:%M')
    activity_type = serializers.CharField(source='atype.name')
    activity_name = serializers.CharField(source='name')
    activity_descripation = serializers.CharField(source='desc')

    activity_image = serializers.SerializerMethodField() 
    activity_text = serializers.SerializerMethodField()
    activity_store = serializers.SerializerMethodField()
    # activity_id = serializers.CharField(source='id')

    class Meta:
        model = Activity
        fields = ('id','activity_image','activity_name','activity_descripation','activity_type','activity_start_datetime','activity_end_datetime','activity_text','activity_store')

    def get_activity_image(self,obj):
        return '/media/' + obj.image.__str__()

    def get_activity_text(self, obj):
        query_set = obj.atext.all()
        return [{'title': obj.title, 'text': obj.text} for obj in query_set]

    def get_activity_store(self, obj):
        query_set = obj.store.all()
        return [{'store_id': obj.id, 
                 'store_name': obj.name,
                 'store_area': obj.area, 
                 'store_address': obj.address, 'store_telephone': obj.phone, 
                 } for obj in query_set]
