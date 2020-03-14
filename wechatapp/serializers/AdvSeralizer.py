from rest_framework import serializers
from wechatapp.models.AdvModel import AdvPicModel


class AdvPicSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvPicModel
        fields = "__all__"