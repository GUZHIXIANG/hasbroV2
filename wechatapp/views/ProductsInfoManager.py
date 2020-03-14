from django.db import transaction
import xlrd
from wechatapp.views import *

# 模型
from wechatapp.models.ProductModel import *
from wechatapp.models.ProductTypeModel import *
from wechatapp.models.AdvModel import AdvPicModel
# 序列器
from wechatapp.serializers.ProductBaseInfoSerializer import *
from wechatapp.serializers.AdvSeralizer import AdvPicSerializer
from wechatapp.serializers.TypeSerializer import *

class items(APIView):
    """
    商品信息相关的接口
    """

    '''GU-非小程序接口'''
    # @swagger_auto_schema(
    # operation_description="添加商品分类借口",
    # request_body=openapi.Schema(
    #     type=openapi.TYPE_OBJECT,
    #     required=['productId','productName','productType','price'],
        # properties={
        #     'productId': openapi.Schema(type=openapi.TYPE_STRING),
        #     'productName': openapi.Schema(type=openapi.TYPE_STRING),
        #     'productType':openapi.Schema(type=openapi.TYPE_STRING),
        #     'systemCode': openapi.Schema(type=openapi.TYPE_INTEGER),
        #     'barCode': openapi.Schema(type=openapi.TYPE_INTEGER),
        #     'color': openapi.Schema(type=openapi.TYPE_STRING),
        #     'norms': openapi.Schema(type=openapi.TYPE_STRING),
        #     'weight': openapi.Schema(type=openapi.TYPE_INTEGER),
        #     'price': openapi.Schema(type=openapi.TYPE_INTEGER),
        #     'descripation': openapi.Schema(type=openapi.TYPE_STRING),
        #     'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),  
        #     'shell': openapi.Schema(type=openapi.TYPE_STRING),  
        # },
    # ),
    # responses={201:"创建成功",
    #            },
    # security=[]
    # )
    # def post(self, request, format=None):
        
    #     productId = request.data.get('productId')
    #     productName = request.data.get('productName')
    #     productType = request.data.get('productType')
    #     systemCode = request.data.get('systemCode')
    #     barCode = request.data.get('barCode')
    #     color = request.data.get('color')
    #     norms = request.data.get('norms')
    #     weight = request.data.get('weight')
    #     price = request.data.get('price')
    #     descripation = request.data.get('descripation')

        
    #     try:
    #         ptype = ProductType.objects.get(typeName=productType)
    #         product = ProductBaseInfo(productType=ptype,
    #         productId=productId,
    #         productName=productName,
    #         systemCode=systemCode,
    #         barCode=barCode,
    #         color=color,
    #         norms=norms,
    #         weight=weight,
    #         price=price,
    #         descripation=descripation
    #         )
    #         product.save()
    #         return Response().successMessage(status=status.HTTP_200_OK)
    #     except Exception as e:
    #         print(e)
    #         return Response().errorMessage(error="无法保存",status=status.HTTP_400_BAD_REQUEST)

    
    @swagger_auto_schema(
    operation_description="get product items from",
    manual_parameters=[
        openapi.Parameter("productId", openapi.IN_QUERY, description="获取商品详情信息",
                                   type=openapi.TYPE_STRING),
    ],
    responses={200:"success"
    },
    security=[]
    )
    # TODO(GU)  序列化器不对
    def get(self, request, format=None):
        product_id = request.GET['productId']
        product = ProductBaseInfo.objects.get(productId=product_id)
        serializer = ProductSerializer(product)
        return Response().successMessage(serializer.data,status=status.HTTP_200_OK)

'''GU-非小程序接口'''
# class itemurl(APIView):
#     """
#     商品图片相关接口
#     """
#     @swagger_auto_schema(
#     operation_description="添加商品图片",
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         required=['productId','url'],
#         properties={
#             'productId': openapi.Schema(type=openapi.TYPE_STRING),
#             'url': openapi.Schema(type=openapi.TYPE_STRING),
#         },
#     ),
#     responses={201:"创建成功",
#                },
#     security=[]
#     )
#     def post(self, request, format=None):
        
#         productId = request.data.get('productId')
#         url = request.data.get('url')
#         try:
#             pid = ProductBaseInfo.objects.get(productId=productId)
#             product = ProductUrl(
#             productbaseinfo=pid,
#             url=url
#             )
#             product.save()
#             return Response().successMessage(status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response().errorMessage(error="无法保存",status=status.HTTP_400_BAD_REQUEST)

    
#     @swagger_auto_schema(
#     operation_description="get product items from",
#     manual_parameters=[
#         openapi.Parameter("productId", openapi.IN_QUERY, description="获取商品图片信息",
#                                    type=openapi.TYPE_STRING),
#     ],
#     responses={200:"success"
#     },
#     security=[]
#     )
#     def get(self, request, format=None):
#         product_id = request.GET['productId']
#         product = ProductUrl.objects.filter(productbaseinfo=product_id)
#         serializer = ProductUrlSerializer(product,many=True)
#         return Response().successMessage(serializer.data,status=status.HTTP_200_OK)

'''GU-非小程序接口'''
# class itemtag(APIView):
#     """
#     商品标签相关
#     """

    
#     @swagger_auto_schema(
#     operation_description="添加商品标签,tag类型限定，h=热门，d=打折，n=新款",
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         required=['productId','tag'],
#         properties={
#             'productId': openapi.Schema(type=openapi.TYPE_STRING),
#             'tag': openapi.Schema(type=openapi.TYPE_STRING),
#         },
#     ),
#     responses={201:"创建成功",
#                },
#     security=[]
#     )
#     def post(self, request, format=None):
        
#         productId = request.data.get('productId')
#         tag = request.data.get('tag')
#         try:
#             pid = ProductBaseInfo.objects.get(productId=productId)
#             product = ProductTag(
#             productbaseinfo=pid,
#             tag=tag
#             )
#             product.save()
#             return Response().successMessage(status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response().errorMessage(error="无法保存",status=status.HTTP_400_BAD_REQUEST)

    
#     @swagger_auto_schema(
#     operation_description="获取商品相关标签",
#     manual_parameters=[
#         openapi.Parameter("productId", openapi.IN_QUERY, description="获取商品标签信息",
#                                    type=openapi.TYPE_STRING),
#     ],
#     responses={200:"success"
#     },
#     security=[]
#     )
#     def get(self, request, format=None):
#         product_id = request.GET['productId']
#         tag = ProductTag.objects.get(productbaseinfo=product_id)
#         serializer = ProductTagSerializer(tag)
#         return Response().successMessage(serializer.data,status=status.HTTP_200_OK)


'''GU-新版替换接口'''
# class hotgoods(APIView):
#     @swagger_auto_schema(
#     operation_description="获取热门商品信息",
#     responses={200:"success"
#     },
#     security=[]
#     )
#     def get(self, request, format=None):
#         tag = ProductTag.objects.filter(tag='h')
#         for hot in tag:
#             h = ProductBaseInfo.objects.filter(productId=hot.productbaseinfo)
#             serializer = ProductAllSerializer(h,many=True)
#         return Response().successMessage({"hotgoods":serializer.data},status=status.HTTP_200_OK)


# class hotgoods2(APIView):
#     @swagger_auto_schema(
#         operation_description="获取热门商品信息*",
#         responses={200: "success"
#                    },
#         security=[]
#     )
#     def get(self, request, format=None):
#         tag = PTag.objects.get(name='热门商品')
#         p = tag.product.all()
#         serializer = ProductAllSerializer(p, many=True)
#         return Response().successMessage({"hotgoods": serializer.data}, status=status.HTTP_200_OK)


'''GU-新版替换接口'''
# class newgoods(APIView):
#     @swagger_auto_schema(
#     operation_description="获取新品商品信息",
#     responses={200:"success"
#     },
#     security=[]
#     )
#     def get(self, request, format=None):
#         tag = ProductTag.objects.filter(tag='n')
#         for n in tag:
#             h = ProductBaseInfo.objects.filter(productId=n.productbaseinfo)
#             serializer = ProductAllSerializer(h,many=True)
           
#         return Response().successMessage({"newgoods":serializer.data},status=status.HTTP_200_OK)


# class newgoods2(APIView):
#     @swagger_auto_schema(
#         operation_description="获取新品商品信息*",
#         responses={200: "success"
#                    },
#         security=[]
#     )
#     def get(self, request, format=None):
#         tag = PTag.objects.get(name='新品上架')
#         p = tag.product.all()
#         serializer = ProductAllSerializer(p, many=True)
#         return Response().successMessage({"newgoods": serializer.data}, status=status.HTTP_200_OK)


'''GU-新版替换接口'''
# class disgoods(APIView):
#     @swagger_auto_schema(
#     operation_description="获取折扣商品信息",
#     responses={200:"success"
#     },
#     security=[]
#     )
#     def get(self, request, format=None):
#         tag = ProductTag.objects.filter(tag='d')
#         for d in tag:
#             h = ProductBaseInfo.objects.filter(productId=d.productbaseinfo)
#             serializer = ProductAllSerializer(h,many=True)
#         return Response().successMessage({"disgoods":serializer.data},status=status.HTTP_200_OK)


# class disgoods2(APIView):
#     @swagger_auto_schema(
#         operation_description="获取折扣商品信息*",
#         responses={200: "success"
#                    },
#         security=[]
#     )
#     def get(self, request, format=None):
#         tag = PTag.objects.get(name='降价促销')
#         p = tag.product.all()
#         serializer = ProductAllSerializer(p, many=True)
#         return Response().successMessage({"disgoods": serializer.data}, status=status.HTTP_200_OK)


'''GU-新版替换接口'''
# class homepage(APIView):
#     @swagger_auto_schema(
#     operation_description="获取商品首页所有信息",
#     responses={200:"success"
#     },
#     security=[]
#     )
#     def get(self, request, format=None):

#         # 首页信息
#         type_list = ProductSecondCategory.objects.all() 
#         advpic = AdvPicModel.objects.all()
#         tag_hot = ProductBaseInfo.objects.filter(producttag__tag__contains='h')
#         tag_new = ProductBaseInfo.objects.filter(producttag__tag__contains='n')
#         tag_discount = ProductBaseInfo.objects.filter(producttag__tag__contains='d')
#         goodsCount = ProductBaseInfo.objects.all()
        
#         rollAdvPic = AdvPicSerializer(advpic,many=True)
#         channel = ProductSecondCategorySerializer(type_list,many=True)
#         hotgoods = ProductAllSerializer(tag_hot,many=True)
#         newgoods = ProductAllSerializer(tag_new,many=True)
#         discountgoods = ProductAllSerializer(tag_discount,many=True)
#         goodsCount = len(goodsCount)
        
        
#         return Response().successMessage({"hotgoods":hotgoods.data,
#                                           "newgoods":newgoods.data,
#                                           "discountgoods":discountgoods.data,
#                                           "rollAdvPic":rollAdvPic.data,
#                                           "channel":channel.data,
#                                           "goodsCount":goodsCount
#                                         },status=status.HTTP_200_OK)


class homepage2(APIView):
    @swagger_auto_schema(
        operation_description="获取商品首页所有信息*",
        responses={200: "success"
                   },
        security=[]
    )
    def get(self, request, format=None):
        '''首页信息'''
        # 已优化
        type_list = PType.objects.filter(desc=2)
        tag_hot = PTag.objects.get(name='热门商品').product.all()
        tag_new = PTag.objects.get(name='新品上架').product.all()
        tag_discount = PTag.objects.get(name='降价促销').product.all()
        goodsCount = ProductBaseInfo.objects.all().count()

        channel = PTypeSerializer(type_list, many=True)
        hotgoods = ProductAllSerializer(tag_hot, many=True)
        newgoods = ProductAllSerializer(tag_new, many=True)
        discountgoods = ProductAllSerializer(tag_discount, many=True)

        # TODO(GU)  未优化
        advpic = AdvPicModel.objects.all() 
        
        rollAdvPic = AdvPicSerializer(advpic, many=True)


        return Response().successMessage({"hotgoods": hotgoods.data,
                                          "newgoods": newgoods.data,
                                          "discountgoods": discountgoods.data,
                                          "rollAdvPic": rollAdvPic.data,
                                          "channel": channel.data,
                                          "goodsCount": goodsCount
                                          }, status=status.HTTP_200_OK)
   
class itemsdetail(APIView):
    @swagger_auto_schema(
    operation_description="获取商品详情页面",
    manual_parameters=[
        openapi.Parameter("productId", openapi.IN_QUERY, description="获取商品详情信息",
                                   type=openapi.TYPE_STRING),
    ],
    responses={200:"success"
    },
    security=[]
    )
    def get(self,request,format=None):
        
        product_id = request.GET['productId']
        product = ProductBaseInfo.objects.get(productId=product_id)
        url     = ProductUrl.objects.filter(productbaseinfo=product)

        url_seri = ProductUrlSerializer(url,many=True)
        kiop = {"gallary":url_seri.data,
                "goodsinfo":{
                    "name":product.productName,
                    "price":product.price,
                    "brief":product.brief,
                    "brand":product.brand
                    },
                "attribute":{
                        "norms":product.norms,
                        "weight":product.weight
                },
                "number":product.quantity,
                "productId":product.productId
                }
        
        return Response().successMessage(kiop,status=status.HTTP_200_OK)


