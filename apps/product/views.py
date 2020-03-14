from rest_framework import mixins
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,filters,pagination

from product import *
from .models import *
from .serializers import *

class PageSet(pagination.PageNumberPagination):
    #页面大小
    page_size = 3
    page_size_query_param = "size"
    max_page_size = 10
    page_query_param = "page"



class ptypelist(APIView):
    """商品类别查看"""
    @swagger_auto_schema(
        operation_description="获取商品分类接口",
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
        for i, x in enumerate(leftlist_data):
            x['order_id'] = i+1
            new_leftlist_data.append(x)

        currentTypeId = request.GET.get('currentTypeId')
        currenttype = PType.objects.get(id=currentTypeId)
        currenttype_serializer = PTypeSerializer(currenttype)

        ptypes = PType.objects.filter(parent=currentTypeId)
        ptypes_serializer = PTypeSerializer(ptypes, many=True)

        message = '查询成功'
        return Response().successMessage(status=status.HTTP_200_OK, message=message, data={"typeList": new_leftlist_data, "currentCategory": ptypes_serializer.data, "banner": currenttype_serializer.data})


class productlist(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name',  'ptype']

    @swagger_auto_schema(
        operation_description="获取商品详情页面",
        responses={200: "success"
                   },
        security=[]
    )
    def get(self, request, format=None):
        products = Product.objects.filter(shell='on')
        products_serializer = ProductListSerializer(products,many=True)

        return Response().successMessage(products_serializer.data, status=status.HTTP_200_OK)



class productdetail(APIView):
    @swagger_auto_schema(
        operation_description="获取商品详情页面",
        manual_parameters=[
            openapi.Parameter("id", openapi.IN_QUERY, description="获取商品详情信息",
                              type=openapi.TYPE_STRING),
        ],
        responses={200: "success"
                   },
        security=[]
    )
    # TODO(GU)  序列化器不对
    def get(self, request, format=None):

        product_id = request.GET['id']
        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)
            pinfo = PInfo.objects.filter(product=product.id)
            url = PBanner.objects.filter(product=product.id)

            url_serializer = PBannerSerializer(url, many=True)
            kiop = {"gallary": url_serializer.data,
                    "goodsinfo": {
                        "name": product.name,
                        "brief": product.brief,
                        "brand": product.brand
                    },
                    "attribute": [{
                        'id':x.id,
                        "price": x.price,
                        "norms": x.norms,
                        "weight": x.weight,
                        "number": x.quantity,
                    } for x in pinfo],
                    "productId": product.productId,
                    "id":product.id
                    }

            return Response().successMessage(kiop, status=status.HTTP_200_OK)
        else:
            return Response().errorMessage(status=status.HTTP_404_NOT_FOUND)


'''================================='''

class PTypeList(mixins.ListModelMixin,
                  generics.GenericAPIView):

    queryset = PType.objects.all()
    serializer_class = PTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductList(mixins.ListModelMixin,
                  generics.GenericAPIView):

    queryset = Product.objects.filter(shell='on')
    serializer_class = ProductListSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_fields = ('ptype','ptag__name')
    search_fields = ('name','=productId')
    ordering_fields = ('price',)
    pagination_class = PageSet

    def list(self,request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page,many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset,many=True)
        return Response().successMessage(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)






class ProductList(mixins.ListModelMixin,
                  generics.GenericAPIView):

    queryset = Product.objects.filter(shell='on')
    serializer_class = ProductListSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_fields = ('ptype','ptag__name')
    search_fields = ('name','=productId')
    ordering_fields = ('price',)
    pagination_class = PageSet

    def list(self,request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page,many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset,many=True)
        return Response().successMessage(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# class ProductDetail(mixins.RetrieveModelMixin,
#                     generics.GenericAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductDetailSerializer

#     def get(self, request, *args, **kwargs):
#         print(kwargs)
#         return self.retrieve(request, *args, **kwargs)