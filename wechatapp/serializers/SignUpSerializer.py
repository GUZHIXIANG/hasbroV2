import unicodedata
import re

from rest_framework import serializers
from wechatapp.models.SignUpModel import SignUp


class SignUpSerializer(serializers.ModelSerializer):
    activity_name = serializers.CharField(
        source='activity.activity_name')
    activity_start_datetime = serializers.DateTimeField(
        source='activity.activity_start_datetime', format='%Y-%m-%d %H:%M')
    activity_end_datetime = serializers.DateTimeField(
        source='activity.activity_end_datetime',format='%Y-%m-%d %H:%M')
    store_name = serializers.CharField(
        source='store.store_name')
    store_address = serializers.CharField(
        source='store.store_address')

    class Meta:
        model = SignUp
        fields = ("id","activity_id", "activity_name",
                  "activity_start_datetime", "activity_end_datetime", 
                  "store_id", "store_name", "store_address", 
                  "signup_name", "signup_phone")

class SignUpCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignUp
        fields = "__all__"#("activity_id", "store_id", "user_id")

    def create(self, validated_data):
        return SignUp.objects.create(**validated_data)
    
    def validate(self,attrs):
        if SignUp.objects.filter(**attrs).exists():
            raise serializers.ValidationError('该成员已报名')
        return attrs

    def validate_signup_name(self,value):
        res = re.search(r'[^\w\s]', value)
        if res:
            raise serializers.ValidationError('姓名中不得存在特殊符号')
        return value

    def validate_signup_phone(self,value):
        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                pass
            try:
                unicodedata.numeric(s)
                return True
            except (TypeError, ValueError):
                pass
            return False

        def is_phone(phone):
            if phone is None:
                return False
            if is_number(phone):
                phone = str(phone).strip()
                RE_PHONE = re.compile(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
                res = re.search(RE_PHONE, phone)
                if res:
                    return True
                else:
                    return False
            else:
                return False

        if not is_phone(value):
            raise serializers.ValidationError('手机号码输入格式不正确')
        return value

class SignUpUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignUp
        fields = ("store", "signup_name", "signup_phone",)

    def update(self, instance, validated_data):
        for item in validated_data:
            if SignUp._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        instance.save()
        return instance

    def validate_signup_name(self, value):
        res = re.search(r'[^\w\s]', value)
        if res:
            raise serializers.ValidationError('姓名中不得存在特殊符号')
        return value

    def validate_signup_phone(self, value):
        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                pass
            try:
                unicodedata.numeric(s)
                return True
            except (TypeError, ValueError):
                pass
            return False

        def is_phone(phone):
            if phone is None:
                return False
            if is_number(phone):
                phone = str(phone).strip()
                RE_PHONE = re.compile(
                    r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
                res = re.search(RE_PHONE, phone)
                if res:
                    return True
                else:
                    return False
            else:
                return False

        if not is_phone(value):
            raise serializers.ValidationError('手机号码输入格式不正确')
        return value

