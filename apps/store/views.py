from store import *
# 本view层所需要模型和序列化对象
from .models import *
from .serializers import *



class storelist(APIView):
    '''门店查询'''
    def get(self, request, format=None):
        if Store.objects.all().exists():  # 验证资源是否存在
            stores = Store.objects.all()
            stores_serializer = StoreListSerializer(
                stores, many=True)
            message = "查询成功"
            return Response().successMessage(status=status.HTTP_200_OK,message=message, data=stores_serializer.data)
        else:  # 资源不存在
            message = "查询成功"
            return Response().successMessage(status=status.HTTP_200_OK,message=message, data=[])
