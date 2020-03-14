# 每层view文件必须import
from activity import *

from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# 本view层所需要模型和序列化对象
from .models import *
from .serializers import *
from datetime import datetime

class activitylist(APIView):
    '''活动查询'''
    @swagger_auto_schema(
        operation_description="后台用户活动显示接口",
        responses={200: "success"
                   },
        security=[]
    )
    def get(self, request, format=None):
        if Activity.objects.filter().exists():  # 验证资源是否存在
            now = datetime.now()
            activitys = Activity.objects.filter(end_datetime__gte=now)
            activitys_serializer = ActivityListSerializer(
                activitys, many=True)
            message = "查询成功"
            return Response().successMessage(status=status.HTTP_200_OK,
                                                message=message, data=activitys_serializer.data)
        else:  # 资源不存在
            message = "查询成功"
            return Response().successMessage(status=status.HTTP_200_OK,
                                                message=message, data=[])


class activitydetail(APIView):
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
        activity_id = request.GET.get('activity_id')
        if Activity.objects.filter(id=activity_id).exists():  # 验证资源是否存在
            activity = Activity.objects.get(id=activity_id)
            activity_serializer = ActivityDetailSerializer(activity)
            message = "查询成功"
            return Response().successMessage(status=status.HTTP_200_OK,
                                                message=message, data=activity_serializer.data)
        else:  # 资源不存在异常
            message = "未找到指定资源"
            return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
 

'''-------------------------------------'''

class ActivityList(mixins.ListModelMixin,
                  generics.GenericAPIView):

    queryset = Activity.objects.filter(end_datetime__gte=datetime.now())
    serializer_class = ActivityListSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_fields = ('atype',)
    search_fields = ('name','=id')
    ordering_fields = ('start_datetime','end_datetime')

    def list(self,request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset,many=True)
        return Response().successMessage(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)