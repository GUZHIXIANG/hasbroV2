# 每层view文件必须import
from wechatapp.views import *

# 本view层所需要模型和序列化对象
from wechatapp.models.ActivityModel import *
from wechatapp.serializers.ActivitySerializer import *

__unicode__ = '__str__'

# class activity_create(APIView):
#     '''活动创建'''
#     @swagger_auto_schema(
#         operation_description="后台用户活动创建接口",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=["activity_name"],
#             properties={
#                 'super_activity': openapi.Schema(type=openapi.TYPE_INTEGER),
#                 'activity_name': openapi.Schema(type=openapi.TYPE_STRING),
#                 'activity_descripation': openapi.Schema(type=openapi.TYPE_STRING),
#                 'activity_type': openapi.Schema(type=openapi.TYPE_INTEGER),
#                 "activity_start_datetime": openapi.Schema(type=openapi.TYPE_STRING),
#                 "activity_end_datetime": openapi.Schema(type=openapi.TYPE_STRING),
#                 "activity_store": openapi.Schema(
#                     type=openapi.TYPE_ARRAY,
#                     items=openapi.Schema(type=openapi.TYPE_OBJECT,
#                                          properties={
#                                              'store': openapi.Schema(type=openapi.TYPE_INTEGER),
#                                          })),
#                 "activity_image": openapi.Schema(
#                     type=openapi.TYPE_ARRAY,
#                     items=openapi.Schema(type=openapi.TYPE_OBJECT,
#                                          properties={
#                                              'image': openapi.Schema(type=openapi.TYPE_STRING),
#                                              'image_type': openapi.Schema(type=openapi.TYPE_INTEGER),
#                                          })),
#                 "activity_text": openapi.Schema(
#                     type=openapi.TYPE_ARRAY,
#                     items=openapi.Schema(type=openapi.TYPE_OBJECT,
#                                          properties={
#                                              'title': openapi.Schema(type=openapi.TYPE_STRING),
#                                              'text': openapi.Schema(type=openapi.TYPE_STRING),
#                                          })),   
#             },
#         ),
#         responses={200: ""},
#         security=[]
#     )
#     def post(self, request, format=None):
#         if request.method == "POST":  # 验证请求方式
#             activity_serializer = ActivityCreateSerializer(
#                 data=request.data, partial=True)
#             if activity_serializer.is_valid():  # 验证数据是否合法
#                 activity_serializer.validated_data
#                 activity_serializer.save()
#             else: # 数据非法异常
#                 message = activity_serializer.errors
#                 return Response().errorMessage(status=status.HTTP_406_NOT_ACCEPTABLE, message=message)
#             message = "创建成功"
#             return Response().successMessage(status=status.HTTP_201_CREATED, message=message)
#         else: # 请求方式异常
#             message = "请求方式错误"
#             return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)


# class activity_delete(APIView):
#     '''活动删除'''
#     @swagger_auto_schema(
#         operation_description="后台用户活动删除接口",
#         manual_parameters=[
#             openapi.Parameter("activity_id", openapi.IN_QUERY, description="活动ID",
#                               type=openapi.TYPE_INTEGER)
#         ],
#         responses={200: ""},
#         security=[]
#     )
#     def get(self, request, format=None):
#         if request.method == "GET": # 验证请求方式
#             activity_id = request.GET.get('activity_id')
#             # 删除操作
#             if Activity.objects.filter(id=activity_id).exists(): # 验证资源是否存在
#                 Activity.objects.get(id=activity_id).delete()
#                 message = "删除成功"
#                 return Response().successMessage(status=status.HTTP_200_OK, message=message)
#             else: # 资源不存在异常
#                 message = "未找到指定资源"
#                 return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
#         else: # 请求方式异常
#             message = "请求方式错误"
#             return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)


# class activity_update(APIView):
#     '''活动修改'''
#     @swagger_auto_schema(
#         operation_description="后台用户活动修改接口",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=["activity_id"],
#             properties={
#                 'activity_id': openapi.Schema(type=openapi.TYPE_INTEGER), 
#                 'activity_name': openapi.Schema(type=openapi.TYPE_STRING),
#                 'activity_descripation': openapi.Schema(type=openapi.TYPE_STRING),
#                 'activity_type': openapi.Schema(type=openapi.TYPE_INTEGER),
#                 "activity_start_datetime": openapi.Schema(type=openapi.TYPE_STRING),
#                 "activity_end_datetime": openapi.Schema(type=openapi.TYPE_STRING),
#                 'super_activity': openapi.Schema(type=openapi.TYPE_INTEGER),
#                 "activity_store": openapi.Schema(
#                     type=openapi.TYPE_ARRAY,
#                     items=openapi.Schema(type=openapi.TYPE_OBJECT,
#                                          properties={
#                                              'store': openapi.Schema(type=openapi.TYPE_INTEGER),
#                                          })),
#                 "activity_image": openapi.Schema(
#                     type=openapi.TYPE_ARRAY,
#                     items=openapi.Schema(type=openapi.TYPE_OBJECT,
#                                          properties={
#                                              'image': openapi.Schema(type=openapi.TYPE_STRING),
#                                              'image_type': openapi.Schema(type=openapi.TYPE_INTEGER),
#                                          })),
#                 "activity_text": openapi.Schema(
#                     type=openapi.TYPE_ARRAY,
#                     items=openapi.Schema(type=openapi.TYPE_OBJECT,
#                                          properties={
#                                              'title': openapi.Schema(type=openapi.TYPE_STRING),
#                                              'text': openapi.Schema(type=openapi.TYPE_STRING),
#                                          })),
#             },
#         ),
#         responses={200: ""},
#         security=[]
#     )
#     def post(self, request, format=None):
#         if request.method == "POST": # 验证请求方式
#             activity_id = request.data.get('activity_id')
#             if Activity.objects.filter(id=activity_id).exists(): # 验证资源是否存在
#                 activity = Activity.objects.get(id=activity_id)
#                 activity_serializer = ActivityUpdateSerializer(
#                     instance=activity, data=request.data, partial=True)
#                 if activity_serializer.is_valid(): # 验证数据是否合法
#                     activity_serializer.validated_data
#                     activity_serializer.save()
#                 else: # 数据非法异常
#                     message = activity_serializer.errors
#                     return Response().errorMessage(status=status.HTTP_406_NOT_ACCEPTABLE, message=message)
#                 message = "修改成功"
#                 return Response().successMessage(status=status.HTTP_200_OK, message=message)
#             else: # 资源不存在异常
#                 message = "未找到指定资源"
#                 return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
#         else: # 请求方式异常
#             message = "请求方式错误"
#             return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)


class activity_view(APIView):
    '''活动查询'''
    @swagger_auto_schema(
        operation_description="后台用户活动显示接口",
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
            if Activity.objects.filter().exists(): # 验证资源是否存在
                activitys = Activity.objects.all()
                activitys_serializer = ActivitySerializer(
                    activitys, many=True)
                message = "查询成功"
                return Response().successMessage(status=status.HTTP_200_OK,
                                                message=message, data=activitys_serializer.data)
            else: # 资源不存在
                message = "无数据"
                return Response().successMessage(status=status.HTTP_200_OK,
                                                 message=message, data=[])
        else: # 请求方式异常
            message = "请求方式错误"
            return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)
        

class activitydetail_view(APIView):
    '''活动详情查询'''
    @swagger_auto_schema(
        operation_description="小程序用户活动详情显示接口",
        manual_parameters=[
            openapi.Parameter("activity_id", openapi.IN_QUERY, description="活动ID",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={200: "success"
                   },
        security=[]
    )
    def get(self, request, format=None):
        if request.method == "GET": # 验证请求方式
            activity_id = request.GET.get('activity_id')
            if Activity.objects.filter(id=activity_id).exists(): # 验证资源是否存在
                activity = Activity.objects.get(id=activity_id)
                activity_serializer = ActivityDetailSerializer(activity)
                message = "查询成功"
                return Response().successMessage(status=status.HTTP_200_OK,
                                                message=message, data=activity_serializer.data)
            else:  # 资源不存在异常
                message = "未找到指定资源"
                return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
        else: # 请求方式异常
            message = "请求方式错误"
            return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)

# class activitystore_view(APIView):
#     '''活动查询'''
#     @swagger_auto_schema(
#         operation_description="后台用户活动显示接口",
#         # manual_parameters=[
#         #     openapi.Parameter("user_id", openapi.IN_QUERY, description="用户ID",
#         #                       type=openapi.TYPE_STRING),
#         # ],
#         responses={200: "success"
#                    },
#         security=[]
#     )
#     def get(self, request, format=None):
#         if request.method == "GET":
#             # user_id = request.GET.get('user_id')
#             activitystores = ActivityStore.objects.all()
#             activitystores_serializer = ActivityStoreSerializer(
#                 activitystores, many=True)
#             message = "查询成功"
#             return Response().successMessage(status=status.HTTP_200_OK,
#                                              message=message, data=activitystores_serializer.data)


'''################### 活动类型 ###################'''

# class activitytype_create(APIView):
#     '''活动类型创建'''
#     @swagger_auto_schema(
#         operation_description="后台用户活动类型创建接口",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=["activity_type"],
#             properties={
#                 'activity_type': openapi.Schema(type=openapi.TYPE_STRING),
#             },
#         ),
#         responses={200: ""},
#         security=[]
#     )
#     def post(self, request, format=None):
#         if request.method == "POST": # 验证请求方式
#             activitytype_serializer = ActivityTypeCreateSerializer(
#                 data=request.data)
#             if activitytype_serializer.is_valid(): # 验证数据是否合法
#                 activitytype_serializer.validated_data
#                 activitytype_serializer.save()
#                 message = "创建成功"
#                 return Response().successMessage(status=status.HTTP_200_OK, message=message)
#             else: # 数据非法异常
#                 message = activitytype_serializer.errors
#                 return Response().errorMessage(status=status.HTTP_406_NOT_ACCEPTABLE, message=message)
#         else: # 请求方式异常
#             message = "请求方式错误"
#             return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)

# class activitytype_delete(APIView):
#     '''活动类型删除'''
#     @swagger_auto_schema(
#         operation_description="后台用户活动类型删除接口",
#         manual_parameters=[
#             openapi.Parameter("activitytype_id", openapi.IN_QUERY, description="活动类型ID",
#                               type=openapi.TYPE_INTEGER)
#         ],
#         responses={200: ""},
#         security=[]
#     )
#     def get(self, request, format=None):
#         if request.method == "GET": # 验证请求方式
#             activitytype_id = request.GET.get('activitytype_id')
#             # 删除操作
#             if ActivityType.objects.filter(id=activitytype_id).exists(): # 验证资源是否存在
#                 ActivityType.objects.get(id=activitytype_id).delete()
#                 message = "删除成功"
#                 return Response().successMessage(status=status.HTTP_200_OK, message=message)
#             else: # 资源不存在异常
#                 message = "未找到指定资源"
#                 return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
#         else: # 请求方式异常
#             message = "请求方式错误"
#             return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)

# class activitytype_update(APIView):
#     '''活动类型修改'''
#     @swagger_auto_schema(
#         operation_description="后台用户活动类型修改接口",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=["activitytype_id", "activity_type"],
#             properties={
#                 'activitytype_id': openapi.Schema(type=openapi.TYPE_INTEGER),
#                 'activity_type': openapi.Schema(type=openapi.TYPE_INTEGER),
#             },
#         ),
#         responses={200: ""},
#         security=[]
#     )
#     def post(self, request, format=None):
#         if request.method == "POST": # 验证请求方式
#             activitytype_id = request.data.get('activitytype_id')
#             if ActivityType.objects.filter(id=activitytype_id).exists(): # 验证资源是否存在
#                 activitytype = ActivityType.objects.get(id=activitytype_id)
#                 activitytype_serializer = ActivityTypeUpdateSerializer(
#                     instance=activitytype, data=request.data)
#                 if activitytype_serializer.is_valid(): # 验证数据是否合法
#                     activitytype_serializer.validated_data
#                     activitytype_serializer.save()
#                     message = "修改成功"
#                     return Response().successMessage(status=status.HTTP_200_OK, message=message)
#                 else: # 数据非法异常
#                     message = activitytype_serializer.errors
#                     return Response().errorMessage(status=status.HTTP_406_NOT_ACCEPTABLE, message=message)
#             else: # 资源不存在异常
#                 message = "未找到指定资源"
#                 return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
#         else: # 请求方式异常
#             message = "请求方式错误"
#             return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)

# class activitytype_view(APIView):
#     '''活动类型查询'''
#     @swagger_auto_schema(
#         operation_description="后台用户活动类型显示接口",
#         # manual_parameters=[
#         #     openapi.Parameter("user_id", openapi.IN_QUERY, description="用户ID",
#         #                       type=openapi.TYPE_STRING),
#         # ],
#         responses={200: "success"
#                    },
#         security=[]
#     )
#     def get(self, request, format=None):
#         if request.method == "GET": # 验证请求方式
#             # user_id = request.GET.get('user_id')
#             if ActivityType.objects.filter().exists(): # 验证数据是否存在
#                 activitytypes = ActivityType.objects.all()
#                 activitytypes_serializer = ActivityTypeSerializer(
#                     activitytypes, many=True)
#                 message = "查询成功"
#                 return Response().successMessage(status=status.HTTP_200_OK,
#                                                 message=message, data=activitytypes_serializer.data)
#             else:  # 资源不存在异常
#                 message = "未找到指定资源"
#                 return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
#         else: # 请求方式异常
#             message = "请求方式错误"
#             return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)
