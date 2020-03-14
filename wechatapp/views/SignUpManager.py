# 每层view文件必须import
from wechatapp.views import *

# 本view层所需要模型和序列化对象
# from wechatapp.models.ActivityModel import Activity
# from wechatapp.models.StoreModel import Store
from wechatapp.models.SignUpModel import *
from wechatapp.serializers.SignUpSerializer import *
# from django.contrib.auth.models import User
from user.models import UserProfile

def check_user(request):
    # 获取用户key
    user_key = request.META.get("HTTP_SESSION_KEY")
    user = UserProfile.objects.filter(password=user_key)
    if user:
        return user


class signup_create(APIView):
    '''报名创建'''
    @swagger_auto_schema(
        operation_description="微信小程序用户活动报名接口",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["activity", "store", "signup_name","signup_phone"],#"user_id"
            properties={
                # 'user_id': openapi.Schema(type=openapi.TYPE_STRING),
                'activity': openapi.Schema(type=openapi.TYPE_INTEGER),
                'store': openapi.Schema(type=openapi.TYPE_INTEGER),
                'signup_name': openapi.Schema(type=openapi.TYPE_STRING),
                'signup_phone': openapi.Schema(type=openapi.TYPE_STRING),
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
            signup_serializer = SignUpCreateSerializer(
                data=data, partial=True)
            if signup_serializer.is_valid(): # 验证数据是否合法
                signup_serializer.validated_data
                signup_serializer.save()
                
                message = "报名成功"
                return Response().successMessage(status=status.HTTP_200_OK, message=message)
            else: # 数据非法异常
                message = signup_serializer.errors
                return Response().errorMessage(status=status.HTTP_406_NOT_ACCEPTABLE,message=message)
        else: # 请求方式异常
            message = "请求方式错误"
            return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)


class signup_update(APIView):
    '''报名修改'''
    @swagger_auto_schema(
        operation_description="微信小程序用户报名活动修改接口",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["signup_id"],
            properties={
                'signup_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'store': openapi.Schema(type=openapi.TYPE_INTEGER),
                'signup_name': openapi.Schema(type=openapi.TYPE_STRING),
                'signup_phone': openapi.Schema(type=openapi.TYPE_STRING),
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
            else:
                message = "请登录"
                return Response().errorMessage(error="login requried",status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,message=message)

            signup_id = data.get('signup_id')
            if SignUp.objects.filter(id=signup_id).exists(): # 验证资源是否存在
                signup = SignUp.objects.get(id=signup_id)
                signup_serializer = SignUpUpdateSerializer(
                    instance=signup, data=request.data, partial=True)
                if signup_serializer.is_valid(): # 验证数据是否合法
                    signup_serializer.validated_data
                    signup_serializer.save()
                    message = "修改成功"
                    return Response().successMessage(status=status.HTTP_200_OK, message=message)
                else: # 数据非法异常
                    message = signup_serializer.errors
                    return Response().errorMessage(status=status.HTTP_406_NOT_ACCEPTABLE, message=message)
            else:  # 资源不存在异常
                message = "未找到指定资源"
                return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
        else: # 请求方式异常
            message = "请求方式错误"
            return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)


class signup_cancel(APIView):
    '''报名取消'''
    @swagger_auto_schema(
        operation_description="微信小程序用户报名活动取消接口",
        manual_parameters=[
            openapi.Parameter("signup_id", openapi.IN_QUERY, description="报名ID",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={200: ""},
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

            signup_id = request.GET.get('signup_id')
            # 删除操作
            if SignUp.objects.filter(id=signup_id).exists():
                SignUp.objects.get(id=signup_id).delete()
                message = "取消成功"
                return Response().successMessage(status=status.HTTP_200_OK, message=message)
            else:  # 资源不存在异常
                message = "未找到指定资源"
                return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
        else: # 请求方式异常
            message = "请求方式错误"
            return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)


class signup_view(APIView):
    '''报名显示'''
    @swagger_auto_schema(
        operation_description="微信小程序用户报名活动显示接口",
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
            # 获取用户key
            user_key = request.META.get("HTTP_SESSION_KEY")
            users = UserProfile.objects.filter(password=user_key)
            if users.exists():
                user = UserProfile.objects.get(password=user_key)
                user_id = user.id
            else:
                message = "请登录"
                return Response().errorMessage(error="login requried",status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,message=message)

            if SignUp.objects.filter(user_id=user).exists(): # 验证资源是否存在
                signups = SignUp.objects.filter(
                    user_id=user_id).order_by('signup_create_time')
                signups_serializer = SignUpSerializer(signups,many=True)
                message = "查询成功"
                return Response().successMessage(status=status.HTTP_200_OK, 
                message=message,data=signups_serializer.data)
            else:  # 资源不存在
                message = "无数据"
                return Response().successMessage(status=status.HTTP_200_OK,
                                                 message=message, data=[])
        else: # 请求方式异常
            message = "请求方式错误"
            return Response().successMessage(status=status.HTTP_405_METHOD_NOT_ALLOWED, message=message)
