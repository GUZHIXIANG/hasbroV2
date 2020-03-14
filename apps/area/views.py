from area import *

from .models import *
from .serializers import *

class area(APIView):
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
        parent_id = request.GET.get('parent_id')
        if Areas.objects.filter(parent_id=parent_id).exists():
            areas = Areas.objects.filter(parent_id=parent_id)
            areas_serializer = AreaSerializer(
                areas, many=True)
            message = "查询成功"
            return Response().successMessage(status=status.HTTP_200_OK, message=message, data=areas_serializer.data)
        else:  # 资源不存在
            message = "查询成功"
            return Response().successMessage(status=status.HTTP_200_OK, message=message, data=[])
