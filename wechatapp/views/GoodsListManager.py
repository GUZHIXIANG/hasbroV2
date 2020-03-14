from wechatapp.views import *
# 模型
from wechatapp.models.ProductModel import (ProductBaseInfo,ProductUrl,PTag)
# 序列器
from wechatapp.serializers.ProductBaseInfoSerializer import *
from wechatapp.serializers.TypeSerializer import *


from wechatapp.models.ProductTypeModel import PType
class goodsList(APIView):
    @swagger_auto_schema(
        operation_description="测试*",
        responses={200: "success"
                   },
        manual_parameters=[
            openapi.Parameter("isHot", openapi.IN_QUERY, description="热门",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter("isNew", openapi.IN_QUERY, description="新品",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter("isDis", openapi.IN_QUERY, description="降价",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter("order", openapi.IN_QUERY, description="排序方法",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter("sort", openapi.IN_QUERY, description="搜索类型",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter("categoryId", openapi.IN_QUERY, description="类别Id 从 channel里拿",
                              type=openapi.TYPE_INTEGER),
        ],
        security=[]
    )
    def get(self, request, format=None):
        
        isHot = request.GET.get('isHot')
        isNew = request.GET.get('isNew')
        isDis = request.GET.get('isDis')
        # page = request.GET.get('page')
        # size = request.GET.get('size')
        order = request.GET.get('order')
        sortType = request.GET.get('sort')
        categoryId = request.GET.get('categoryId')

        #（这里要返回所有3级分类的标签）
        
        filterCategory = PType.objects.filter(desc=3)
        channel = PTypeSerializer(filterCategory, many=True)

        if isHot == '1' and isNew == '0' and isDis == '0':
            tag_name = '热门商品'
        elif isHot == '0' and isNew == '1' and isDis == '0':
            tag_name = '新品上架'
        elif isHot == '0' and isNew == '0' and isDis == '1':
            tag_name = '降价促销'
        else:
            tag_name = ''


       # TODO(GU)   貌似用的序列化器不对
        # 热门
        if isHot == '1' and isNew == '0' and isDis == '0':
            
            # 判断是否sortType 有 category 这个关键字在，说明要根据 类别过滤返回的商品
            if sortType =='category':
                # 当前类别
                try:
                    product = filterCategory.get(id=categoryId).product.filter(tags__name="热门商品")
                    hotgoods = ProductSerializer(product,many=True)
                    return Response().successMessage({"goodsList": hotgoods.data,"channel":channel.data}, status=status.HTTP_200_OK)
                except:
                    return Response().successMessage({"goodsList":[],"channel":channel.data}, status=status.HTTP_200_OK)

            if sortType=='price':
                
                try:
                    if order == "asc":
                        product = ProductBaseInfo.objects.filter(tags__name="热门商品").order_by("price")
                        hotgoods = ProductSerializer(product,many=True)
                        return Response().successMessage({"goodsList": hotgoods.data,"channel":channel.data}, status=status.HTTP_200_OK)
                    elif order == "desc":
                        product = ProductBaseInfo.objects.filter(tags__name="热门商品").order_by("-price")
                        hotgoods = ProductSerializer(product,many=True)
                        return Response().successMessage({"goodsList": hotgoods.data,"channel":channel.data}, status=status.HTTP_200_OK)
                    else:
                        return Response().errorMessage(status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response().successMessage({"goodsList":[],"channel":channel.data}, status=status.HTTP_200_OK)

            if sortType=='default':
                hotProducts = PTag.objects.get(name='热门商品').product.all()
                hotgoods = ProductSerializer2(hotProducts, many=True)
                return Response().successMessage({"goodsList": hotgoods.data,"channel":channel.data}, status=status.HTTP_200_OK)


        
        # 新品

        if isHot == '0' and isNew == '1' and isDis == '0':
            # 判断是否sortType 有 category 这个关键字在，说明要根据 类别过滤返回的商品
            if sortType =='category':
                # 当前类别
                try:
                    product = filterCategory.get(id=categoryId).product.filter(tags__name="新品上架")
                    hotgoods = ProductSerializer(product,many=True)
                    return Response().successMessage({"goodsList": hotgoods.data,"channel":channel.data}, status=status.HTTP_200_OK)
                except:
                    return Response().successMessage({"goodsList":[],"channel":channel.data}, status=status.HTTP_200_OK)

            if sortType=='price':
                
                try:
                    if order == "asc":
                        product = ProductBaseInfo.objects.filter(tags__name="新品上架").order_by("price")
                        hotgoods = ProductSerializer(product,many=True)
                        return Response().successMessage({"goodsList": hotgoods.data,"channel":channel.data}, status=status.HTTP_200_OK)
                    elif order == "desc":
                        product = ProductBaseInfo.objects.filter(tags__name="新品上架").order_by("-price")
                        hotgoods = ProductSerializer(product,many=True)
                        return Response().successMessage({"goodsList": hotgoods.data,"channel":channel.data}, status=status.HTTP_200_OK)
                    else:
                        return Response().errorMessage(status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response().successMessage({"goodsList":[],"channel":channel.data}, status=status.HTTP_200_OK)

            if sortType=='default':
                hotProducts = PTag.objects.get(name='新品上架').product.all()
                hotgoods = ProductSerializer2(hotProducts, many=True)
                return Response().successMessage({"goodsList": hotgoods.data,"channel":channel.data}, status=status.HTTP_200_OK)
        
        # 降价促销
        if isHot == '0' and isNew == '0' and isDis == '1':
            # 判断是否sortType 有 category 这个关键字在，说明要根据 类别过滤返回的商品
            if sortType =='category':
                # 当前类别
                try:
                    product = filterCategory.get(id=categoryId).product.filter(tags__name="降价促销")
                    hotgoods = ProductSerializer(product,many=True)
                    return Response().successMessage({"goodsList": hotgoods.data,"channel":channel.data}, status=status.HTTP_200_OK)
                except:
                    return Response().successMessage({"goodsList":[],"channel":channel.data}, status=status.HTTP_200_OK)

            if sortType=='price':
                
                try:
                    if order == "asc":
                        product = ProductBaseInfo.objects.filter(tags__name="降价促销").order_by("price")
                        hotgoods = ProductSerializer(product,many=True)
                        return Response().successMessage({"goodsList": hotgoods.data,"channel":channel.data}, status=status.HTTP_200_OK)
                    elif order == "desc":
                        product = ProductBaseInfo.objects.filter(tags__name="降价促销").order_by("-price")
                        hotgoods = ProductSerializer(product,many=True)
                        return Response().successMessage({"goodsList": hotgoods.data,"channel":channel.data}, status=status.HTTP_200_OK)
                    else:
                        return Response().errorMessage(status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response().successMessage({"goodsList":[],"channel":channel.data}, status=status.HTTP_200_OK)

            if sortType=='default':
                hotProducts = PTag.objects.get(name='降价促销').product.all()
                hotgoods = ProductSerializer2(hotProducts, many=True)
                return Response().successMessage({"goodsList": hotgoods.data,"channel":channel.data}, status=status.HTTP_200_OK)