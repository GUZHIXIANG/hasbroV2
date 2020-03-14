from rest_framework import serializers
from user.models import UserProfile

class UserBaseInfoSerializer(serializers.ModelSerializer):
   class Meta:
        model = UserProfile
        fields = ("username","password")
   def create(self, validated_data):
        return User.objects.create(**validated_data)

class UserWxInfoSerializer(serializers.ModelSerializer):
   
   user = UserBaseInfoSerializer()
   
   class Meta:
        model = UserProfile
        fields = ('avatarUrl','nickName','gender','country','province','city','language','user')
        
   def create(self, validated_data):
        profile = validated_data.pop('user')
        user  = UserProfile.objects.create(**profile)
        user.save()
        userinfo = UserProfile.objects.create(user=user,**validated_data)
        userinfo.save()
        return userinfo




