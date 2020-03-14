# -*- coding: utf-8 -*-
# 每层view文件必须import
from wechatapp.views import *

# 本view层所需要模型和序列化对象
from user.models import UserProfile
from wechatapp.models.AddressModel import *
from wechatapp.serializers.AddressSerializer import *

class address(APIView):
    '''地址创建/修改'''
    @swagger_auto_schema(
        operation_description="小程序用户地址创建/修改接口",
        manual_parameters=[
            openapi.Parameter("id", openapi.IN_QUERY, 
            description="地址ID",
            type=openapi.TYPE_INTEGER)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name","mobile","province_id","city_id","district_id","address","is_default"],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'mobile': openapi.Schema(type=openapi.TYPE_STRING),
                'province_id': openapi.Schema(type=openapi.TYPE_STRING),
                "city_id": openapi.Schema(type=openapi.TYPE_STRING),
                "district_id": openapi.Schema(type=openapi.TYPE_STRING),
                "address": openapi.Schema(type=openapi.TYPE_STRING),
                "is_default": openapi.Schema(type=openapi.TYPE_NUMBER),
            },
        ),
        responses={200: ""},
        security=[]
    )
    def post(self, request, format=None):
        if request.method == "POST": # 验证请求方式
            # 获取用户key
            user_key = request.META.get("HTTP_SESSION_KEY")
            users = UserProfile.objects.filter(password=user_key)
            if users.exists():
                user = UserProfile.objects.get(password=user_key)
                data = request.data.copy()
                data['user'] = user.id
            else:
                message = "请登录"
                return Response().errorMessage(error="login requried",status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,message=message)
            address_id = data.get('id')
            data['province'] = data.pop('province_id')
            data['city'] = data.pop('city_id')
            data['district'] = data.pop('district_id')
            if data.get('is_default')==True:
                old_address = Address.objects.filter(user=user.id)
                if old_address.exists():
                    old_address.update(is_default=False)
            if address_id == 0:
                address_serializer = AddressSerializer(
                    data=data, partial=True)
            else:
                if Address.objects.filter(id=address_id).exists():
                    address = Address.objects.get(id=address_id)
                    address_serializer = AddressSerializer(
                        instance=address, data=data, partial=True)
                else:  # 资源不存在异常
                    message = "未找到指定资源"
                    return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
            if address_serializer.is_valid(): # 验证数据是否合法
                address_serializer.validated_data
                address_serializer.save()
                message = "操作成功"
                return Response().successMessage(status=status.HTTP_200_OK, message=message)
            else: # 数据非法异常
                message = address_serializer.errors
                return Response().errorMessage(status=status.HTTP_406_NOT_ACCEPTABLE, message=message)
        else: # 请求方式异常
            message = "请求方式错误"
            return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)

    '''地址删除'''
    @swagger_auto_schema(
        operation_description="小程序用户地址删除接口",
        manual_parameters=[
            openapi.Parameter("id", openapi.IN_QUERY, 
            description="地址ID",
            type=openapi.TYPE_INTEGER)
        ],
        responses={200: ""},
        security=[]
    )
    def delete(self, request, format=None):
        if request.method == "DELETE":  # 验证请求方式
            # 获取用户key
            user_key = request.META.get("HTTP_SESSION_KEY")
            users = UserProfile.objects.filter(password=user_key)
            if users.exists():
                user = UserProfile.objects.get(password=user_key)
            else:
                message = "请登录"
                return Response().errorMessage(error="login requried",status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,message=message)
            address_id = request.GET.get('id')
            address_id = int(address_id)
            # 删除操作
            if Address.objects.filter(id=address_id).exists(): # 验证资源是否存在
                Address.objects.get(id=address_id).delete()
                message = "删除成功"
                return Response().successMessage(status=status.HTTP_200_OK, message=message)
            else: # 资源不存在异常
                message = "未找到指定资源"
                return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
        else: # 请求方式异常
            message = "请求方式错误"
            return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)

    '''地址列表查询'''
    @swagger_auto_schema(
        operation_description="小程序用户地址列表查询接口",
        responses={200: "success"
                   },
        security=[]
    )
    def get(self, request, format=None):
        if request.method == "GET": # 验证请求方式
            # 获取用户key
            user_key = request.META.get("HTTP_SESSION_KEY")
            users = UserProfile.objects.filter(password=user_key)
            if users.exists():
                user = UserProfile.objects.get(password=user_key)
            else:
                message = "请登录"
                return Response().errorMessage(error="login requried",status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,message=message)
            if Address.objects.filter(user=user.id).exists():  # 验证资源是否存在
                addresses = Address.objects.filter(user=user.id)
                address_serializer = AddressDetailSerializer(
                    addresses, many=True)
                data = address_serializer.data.copy()
                data_new = []
                for d in data:
                    d['province_id'] = d.pop('province')
                    d['city_id'] = d.pop('city')
                    d['district_id'] = d.pop('district')
                    d['full_region'] = ''.join(
                        [d.get('province_name'), d.get('city_name'), d.get('district_name')])
                    data_new.append(d)
                message = "查询成功"
                return Response().successMessage(status=status.HTTP_200_OK,
                                                 message=message, data=data_new)
            else:  # 资源不存在
                message = "无数据"
                return Response().successMessage(status=status.HTTP_200_OK,
                                                 message=message, data=[])
        else: # 请求方式异常
            message = "请求方式错误"
            return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)


class address_detail(APIView):
    '''地址详情查询'''
    # @swagger_auto_schema(
    #     operation_description="小程序用户地址详情显示接口",
    #     manual_parameters=[
    #         openapi.Parameter("address_id", openapi.IN_QUERY, description="地址ID",type=openapi.TYPE_STRING),
    #     ],
    #     responses={200: "success"},
    #     security=[]
    # )
    def get(self,request,format=None):
        if request.method == 'GET': # 验证请求方式
            # 获取用户key
            user_key = request.META.get("HTTP_SESSION_KEY")
            users = UserProfile.objects.filter(password=user_key)
            if users.exists():
                user = UserProfile.objects.get(password=user_key)
            else:
                message = "请登录"
                return Response().errorMessage(error="login requried",status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,message=message)
            address_id = request.GET.get('id')
            address_id = int(address_id)
            if Address.objects.filter(id=address_id).exists(): # 验证资源是否存在
                address = Address.objects.get(id=address_id)
                address_serializer = AddressDetailSerializer(address)
                data = address_serializer.data.copy()
                data['province_id'] = data.pop('province')
                data['city_id'] = data.pop('city')
                data['district_id'] = data.pop('district')
                data['full_region'] = ''.join(
                    [data.get('province_name'), data.get('city_name'), data.get('district_name')])
                message = "查询成功"
                return Response().successMessage(status=status.HTTP_200_OK,
                                                message=message, data=data)
            else: # 资源不存在异常
                message = "未找到指定资源"
                return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
        else: # 请求方式异常
            message = "请求方式错误"
            return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)


'''####################################'''

# import json
# import os
# settings_dir = os.path.dirname(__file__)
# PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
# JSONFILES_FOLDER = os.path.join(PROJECT_ROOT, 'json_files/')


# class area_view(APIView):
#     '''活动详情查询'''
#     @swagger_auto_schema(
#         operation_description="省市区信息查询接口",
#         manual_parameters=[
#             openapi.Parameter("parent_id", openapi.IN_QUERY, description="父ID",
#                               type=openapi.TYPE_STRING),
#         ],
#         responses={200: "success"
#                    },
#         security=[]
#     )
#     def get(self, request, format=None):
#         if request.method == "GET":  # 验证请求方式
#             parent_id = request.GET.get('parent_id')
#             try:
#                 path = JSONFILES_FOLDER + "areas.json"
#                 with open(path, 'r') as f:
#                     areas = json.loads(f.read())
#                 areas = [x for x in areas if x['parent_id'] == parent_id]
#                 message = "查询成功"
#                 return Response().successMessage(status=status.HTTP_200_OK,
#                                                  message=message, data=areas)
#             except Exception as e:  # 资源不存在异常
#                 message = "未找到指定资源"
#                 return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
#         else:  # 请求方式异常
#             message = "请求方式错误"
#             return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)

class area_view2(APIView):
    '''活动详情查询'''
    @swagger_auto_schema(
        operation_description="省市区信息查询接口",
        manual_parameters=[
            openapi.Parameter("parent_id", openapi.IN_QUERY, description="父ID",
                              type=openapi.TYPE_STRING),
        ],
        responses={200: "success"
                   },
        security=[]
    )
    def get(self, request, format=None):
        if request.method == "GET":  # 验证请求方式
            parent_id = request.GET.get('parent_id')
            if Areas.objects.filter(parent_id=parent_id).exists():
                areas = Areas.objects.filter(parent_id=parent_id)
                areas_serializer = AreaSerializer(
                    areas, many=True)
                message = "查询成功"
                return Response().successMessage(status=status.HTTP_200_OK,message=message, data=areas_serializer.data)
            else:  # 资源不存在
                message = "查询成功"
                return Response().successMessage(status=status.HTTP_200_OK, message=message, data=[])
        else:  # 请求方式异常
            message = "请求方式错误"
            return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)


