from rest_framework import serializers
from .models import UserWechat

# TODO(GU)  重写用户模型，需通知前端
class UserWechatSerializer(serializers.ModelSerializer):

   class Meta:
       model = UserWechat
       fields = ("username", "password", 'avatarUrl', 'nickName', 'gender', 'country',
                 'province', 'city', 'language','type')

   def create(self, validated_data):
       return User.objects.create(**validated_data)
