
from wechatapp.views import *
from wechatapp.models.ProductTypeModel import *
from wechatapp.serializers.TypeSerializer import *


'''GU-新版替换接口'''
# class itemtype(APIView):
#     """
#     商品类别管理接口
#     """
#     @swagger_auto_schema(
#     operation_description="获取商品分类接口设定",
#     manual_parameters=[
#         openapi.Parameter("currentTypeId", openapi.IN_QUERY, description="test manual param",
#                                    type=openapi.TYPE_STRING),
#     ],
#     responses={200:"success"
#     },
#     security=[]
#     )
#     def get(self,request,format=None):

#         currentTypeId = request.GET.get('currentTypeId')
       
#         # productType = ProductType.objects.all() 总类目前这一级别不做
#         productSecondCategory = ProductSecondCategory.objects.all()

#         try:
#             currentCategory = ProductSecondCategory.objects.get(id=currentTypeId)
#         except:
#             return Response().errorMessage(error="没有该类别",status=status.HTTP_400_BAD_REQUEST)
        
#         productCurrentCategory = ProductType.objects.filter(typeChildName=currentCategory)

#         p_second = ProductSecondCategorySerializer(productSecondCategory,many=True)
#         currentCategoryList = ProductTypeSerializer(productCurrentCategory,many=True)
#         banner = ProductSecondCategorySerializer(currentCategory)
        
#         return Response().successMessage({"typeList":p_second.data,"currentCategory":currentCategoryList.data,"banner":banner.data},status=status.HTTP_200_OK)
       

class itemtype2(APIView):
    """
    商品类别管理接口
    """
    @swagger_auto_schema(
        operation_description="获取商品分类接口设定2",
        manual_parameters=[
            openapi.Parameter("currentTypeId", openapi.IN_QUERY, description="父ID",
                              type=openapi.TYPE_STRING),
        ],
        responses={200: "success"
                   },
        security=[]
    )
    # TODO(GU)  等小魏调试
    def get(self, request, format=None):

        leftlist = PType.objects.filter(desc=2)
        leftlist_serializer = PTypeSerializer(leftlist, many=True)
        leftlist_data = leftlist_serializer.data.copy()
        
        
        new_leftlist_data = []
        for i,x in enumerate(leftlist_data):
            x['order_id'] = i+1
            new_leftlist_data.append(x)

        currentTypeId = request.GET.get('currentTypeId')
        currenttype = PType.objects.get(id=currentTypeId)
        currenttype_serializer = PTypeSerializer(currenttype)

        ptypes = PType.objects.filter(parent=currentTypeId)
        ptypes_serializer = PTypeSerializer(ptypes, many=True)

        message = '查询成功'
        return Response().successMessage(status=status.HTTP_200_OK, message=message, data={"typeList": new_leftlist_data, "currentCategory": ptypes_serializer.data, "banner": currenttype_serializer.data})
        
