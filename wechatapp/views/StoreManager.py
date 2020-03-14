# 每层view文件必须import
from wechatapp.views import *

# 本view层所需要模型和序列化对象
from wechatapp.models.StoreModel import *
from wechatapp.serializers.StoreSerializer import *


# class store_create(APIView):
#     '''门店创建'''
#     @swagger_auto_schema(
#         operation_description="后台用户门店创建接口",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=["store_name"],
#             properties={
#                 'store_name': openapi.Schema(type=openapi.TYPE_STRING),
#                 'store_address': openapi.Schema(type=openapi.TYPE_STRING),
#                 'store_area': openapi.Schema(type=openapi.TYPE_STRING),
#                 "store_telephone": openapi.Schema(type=openapi.TYPE_STRING),
#                 "store_longitude": openapi.Schema(type=openapi.TYPE_NUMBER),
#                 "store_latitude": openapi.Schema(type=openapi.TYPE_NUMBER),
#             },
#         ),
#         responses={200: ""},
#         security=[]
#     )
#     def post(self, request, format=None):
#         if request.method == "POST": # 验证请求方式
#             store_serializer = StoreCreateSerializer(
#                 data=request.data, partial=True)
#             if store_serializer.is_valid(): # 验证数据是否合法
#                 store_serializer.validated_data
#                 store_serializer.save()
#                 message = "创建成功"
#                 return Response().successMessage(status=status.HTTP_200_OK, message=message)
#             else: # 数据非法异常
#                 message = store_serializer.errors
#                 return Response().errorMessage(status=status.HTTP_406_NOT_ACCEPTABLE, message=message)
#         else: # 请求方式异常
#             message = "请求方式错误"
#             return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)


# class store_delete(APIView):
#     '''门店删除'''
#     @swagger_auto_schema(
#         operation_description="后台用户门店删除接口",
#         manual_parameters=[
#             openapi.Parameter("store_id", openapi.IN_QUERY, description="门店ID",
#                               type=openapi.TYPE_INTEGER)
#         ],
#         responses={200: ""},
#         security=[]
#     )
#     def get(self, request, format=None):
#         if request.method == "GET":  # 验证请求方式
#             store_id = request.GET.get('store_id')
#             # 删除操作
#             if Store.objects.filter(id=store_id).exists(): # 验证资源是否存在
#                 Store.objects.get(id=store_id).delete()
#                 message = "删除成功"
#                 return Response().successMessage(status=status.HTTP_200_OK, message=message)
#             else: # 资源不存在异常
#                 message = "未找到指定资源"
#                 return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
#         else: # 请求方式异常
#             message = "请求方式错误"
#             return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)


# class store_update(APIView):
#     '''活动修改'''
#     @swagger_auto_schema(
#         operation_description="后台用户活动修改接口",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=["store_id"],
#             properties={
#                 'store_id': openapi.Schema(type=openapi.TYPE_INTEGER),
#                 'store_name': openapi.Schema(type=openapi.TYPE_STRING),
#                 'store_address': openapi.Schema(type=openapi.TYPE_STRING),
#                 'store_area': openapi.Schema(type=openapi.TYPE_STRING),
#                 "store_telephone": openapi.Schema(type=openapi.TYPE_STRING),
#                 "store_longitude": openapi.Schema(type=openapi.TYPE_NUMBER),
#                 "store_latitude": openapi.Schema(type=openapi.TYPE_NUMBER),
#             },
#         ),
#         responses={200: ""},
#         security=[]
#     )
#     def post(self, request, format=None):
#         if request.method == "POST": # 验证请求方式
#             store_id = request.data.get('store_id')
#             if Store.objects.filter(id=store_id).exists(): # 验证资源是否存在
#                 store = Store.objects.get(id=store_id)
#                 store_serializer = StoreUpdateSerializer(
#                     instance=store, data=request.data, partial=True)
#                 if store_serializer.is_valid(): # 验证数据是否合法
#                     store_serializer.validated_data
#                     store_serializer.save()
#                     message = "修改成功"
#                     return Response().successMessage(status=status.HTTP_200_OK, message=message)
#                 else: # 数据非法异常
#                     message = store_serializer.errors
#                     return Response().errorMessage(status=status.HTTP_406_NOT_ACCEPTABLE, message=message)
#             else:  # 资源不存在异常
#                 message = "未找到指定资源"
#                 return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
#         else: # 请求方式异常
#             message = "请求方式错误"
#             return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)


class store_view(APIView):
    '''门店查询'''
    @swagger_auto_schema(
        operation_description="后台用户门店显示接口",
        # manual_parameters=[
        #     openapi.Parameter("user_id", openapi.IN_QUERY, description="用户ID",
        #                       type=openapi.TYPE_STRING),
        # ],
        responses={200: "success"
                   },
        security=[]
    )
    def get(self, request, format=None):
        if request.method == "GET": # 验证请求方式
            # user_id = request.GET.get('user_id')
            if Store.objects.filter().exists(): # 验证资源是否存在
                stores = Store.objects.all()
                stores_serializer = StoreSerializer(
                    stores, many=True)
                message = "查询成功"
                return Response().successMessage(status=status.HTTP_200_OK,
                                                message=message, data=stores_serializer.data)
            else:  # 资源不存在
                message = "无数据"
                return Response().successMessage(status=status.HTTP_200_OK,
                                                 message=message, data=[])
        else: # 请求方式异常
            message = "请求方式错误"
            return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)
