from wechatapp.views import *
# 模型
from wechatapp.models.ProductModel import *
# 序列器
from wechatapp.serializers.ProductBaseInfoSerializer import *
from wechatapp.serializers.TypeSerializer import *
from wechatapp.models.ProductTypeModel import PType
from django.db.models import Q
from itertools import chain

# 商品搜索栏支持返回搜索商品用的

class wordsList(APIView):

    def get(self, request, format=None):

        keyword = request.GET['keyword']

        wordlist = []
        try:
            product = ProductBaseInfo.objects.filter(Q(productName__icontains=keyword) | Q(description__icontains=keyword) | Q(brief__icontains=keyword) | Q(brand__icontains=keyword)).order_by("price")
            p_type = PType.objects.filter(name__icontains=keyword)
            for j in p_type:
                wordlist.append(j.name)
            for i in product:
                wordlist.append(i.productName)
            return Response().successMessage({"keywords":wordlist[:10]},status=status.HTTP_200_OK)

        except:
            pass


class itemSearch(APIView):
    

    @swagger_auto_schema(
    operation_description="get product items from",
    manual_parameters=[
        openapi.Parameter("keyword", openapi.IN_QUERY, description="获取商品详情信息",
                                   type=openapi.TYPE_STRING),
        openapi.Parameter("page", openapi.IN_QUERY, description="获取商品详情信息",
                                   type=openapi.TYPE_STRING),
        openapi.Parameter("size", openapi.IN_QUERY, description="获取商品详情信息",
                                   type=openapi.TYPE_STRING),
        openapi.Parameter("sort", openapi.IN_QUERY, description="获取商品详情信息",
                                   type=openapi.TYPE_STRING),
        openapi.Parameter("order", openapi.IN_QUERY, description="获取商品详情信息",
                                   type=openapi.TYPE_STRING),
        openapi.Parameter("categoryId", openapi.IN_QUERY, description="获取商品详情信息",
                                   type=openapi.TYPE_STRING),
    ],
    responses={200:"success"
    },
    security=[]
    )
    def get(self, request, format=None):

        keyword = request.GET['keyword']

        # page = request.GET.get('page')
        # size = request.GET.get('size')
        order = request.GET.get('order')
        sortType = request.GET.get('sort')
        categoryId = request.GET.get('categoryId')

        filterCategory = PType.objects.filter(desc=3)
        channel = PTypeSerializer(filterCategory, many=True)


        # 判断是否sortType 有 category 这个关键字在，说明要根据 类别过滤返回的商品
        if sortType =='category':
            # 当前类别
            try:
                productsQuery = filterCategory.get(id=categoryId).product.filter(Q(productName__icontains=keyword) | Q(description__icontains=keyword) | Q(brief__icontains=keyword) | Q(brand__icontains=keyword)) # 直接搜索商品关键词           

            
            # for i in type_productsQuery:
            #     print(i.product.all())
            
            # TODO(GU)  序列化器不对
                productsQuerySerilizer = ProductSerializer(productsQuery,many=True)
            
            

            # print("商品搜索数",productsQuery.__len__())
            # print("类别搜索数",type_productsQuery)
            

            # goodList = ProductSerializer(goodList,many=True)
            # product = filterCategory.get(id=categoryId).product.filter(tags__name="热门商品")
            
                return Response().successMessage({"goodsList": productsQuerySerilizer.data,"channel":channel.data}, status=status.HTTP_200_OK)
            except:
                return Response().errorMessage({"goodsList":[],"channel":channel.data}, status=status.HTTP_200_OK)

        if sortType=='price':
            
            try:
                if order == "asc":
                    product = ProductBaseInfo.objects.filter(Q(productName__icontains=keyword) | Q(description__icontains=keyword) | Q(brief__icontains=keyword) | Q(brand__icontains=keyword)).order_by("price")
                    goods = ProductSerializer(product,many=True)
                    return Response().successMessage({"goodsList": goods.data,"channel":channel.data}, status=status.HTTP_200_OK)
                elif order == "desc":
                    product = ProductBaseInfo.objects.filter(Q(productName__icontains=keyword) | Q(description__icontains=keyword) | Q(brief__icontains=keyword) | Q(brand__icontains=keyword)).order_by("-price")
                    goods = ProductSerializer(product,many=True)
                    return Response().successMessage({"goodsList": goods.data,"channel":channel.data}, status=status.HTTP_200_OK)
                else:
                    return Response().errorMessage(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response().successMessage({"goodsList":[],"channel":channel.data}, status=status.HTTP_200_OK)

        if sortType=='default':
            product = ProductBaseInfo.objects.filter(Q(productName__icontains=keyword) | Q(description__icontains=keyword) | Q(brief__icontains=keyword) | Q(brand__icontains=keyword))
            goods = ProductSerializer(product, many=True)
            return Response().successMessage({"goodsList": goods.data,"channel":channel.data}, status=status.HTTP_200_OK)
        
        
        # product = ProductBaseInfo.objects.filter(productName__icontains=keyword)
        # serializer = ProductSerializer(product,many=True)
        return Response().successMessage({"goodsList":[],"channel":channel.data},status=status.HTTP_200_OK)


class typeForItem(APIView):

    @swagger_auto_schema(
    operation_description="更具商品类别获取商品类型",
    manual_parameters=[
        openapi.Parameter("productType", openapi.IN_QUERY, description="获取商品详情信息",
                                   type=openapi.TYPE_INTEGER),
    ],
    responses={200:"success"
    },
    security=[]
    )
    def get(self, request, format=None):
        try:
            productType = request.GET['productType']
            product = ProductBaseInfo.objects.filter(productType=productType)
            serializer = ProductSerializer(product,many=True)
            return Response().successMessage({"items":serializer.data},status=status.HTTP_200_OK)
        except:
            return Response().errorMessage(error="wrong Key:" + productType,status=status.HTTP_200_OK)
