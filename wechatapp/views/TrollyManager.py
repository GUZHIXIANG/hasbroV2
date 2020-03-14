from wechatapp.views import *

# from django.contrib.auth.models import UserProfile
from user.models import UserProfile
from wechatapp.serializers.UserRegisterSerializer import UserWxInfoSerializer,UserBaseInfoSerializer

from wechatapp.models.TrollyModel import MyTrolly
from wechatapp.models.ProductModel import (ProductBaseInfo)

from wechatapp.serializers.TrollySerializer import TrollyAllSerializer



class trolly(APIView):
    
    @swagger_auto_schema(
    operation_description="购物车添加商品，需要用户验证，request header 里需要session_key 参数",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['productId'],
        properties={
            'productId': openapi.Schema(type=openapi.TYPE_STRING),
            'nums': openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    ),
    responses={201:"创建成功",
               203:"用户需要登录"},
    security=[]
    )
    def post(self,request,format=None):

        # 首先要用户验证，如果验证不成功，则要求先登录验证
        
        # --------------------------------------
        # 获取用户key
        user_key = request.META.get("HTTP_SESSION_KEY")
        # 查找用户是否合法
        try:
            user = UserProfile.objects.get(password=user_key)
        except:
            return Response().errorMessage(error="login requried",status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        # 获取用户详情信息
        userpro = user#UserProfile.objects.get(user=user)
        # ----------------------------------------
        
        
        # 先判断获取的商品ID 是不是对滴
        product = ProductBaseInfo.objects.get(productId=request.data.get('productId'))
        if not product:
            return Response().errorMessage(error="product not exists",status=status.HTTP_400_BAD_REQUEST)
      

        try:
            my_item = MyTrolly.objects.get(user=userpro,productbaseinfo=product)
            my_item.nums = my_item.nums + request.data.get('nums')
            my_item.save()

            res = MyTrolly.objects.all().filter(user=userpro)

            # 计算所选商品价格
            checked_goods = MyTrolly.objects.all().filter(user=userpro,checkbox=True)
            checkedGoodsAmount = []
            for i in checked_goods:
                checkedGoodsAmount.append(i.productbaseinfo.price * i.nums)
            checkedGoodsAmount = sum(checkedGoodsAmount)
            
            serializer = TrollyAllSerializer(res,many=True)
            
            return Response().successMessage({"items":serializer.data,"checkedGoodsAmount":checkedGoodsAmount},status=status.HTTP_200_OK)
        except:
            if not request.data.get('nums'):
                trol = MyTrolly(user=userpro,productbaseinfo=product)
            else:
                trol = MyTrolly(user=userpro,productbaseinfo=product,nums=request.data.get('nums'))
            
            trol.save()

            res = MyTrolly.objects.all().filter(user=userpro)
            
            # 计算所选商品价格
            checked_goods = MyTrolly.objects.all().filter(user=userpro,checkbox=True)
            checkedGoodsAmount = []
            for i in checked_goods:
                checkedGoodsAmount.append(i.productbaseinfo.price * i.nums)
            checkedGoodsAmount = sum(checkedGoodsAmount)
            
            serializer = TrollyAllSerializer(res,many=True)

            return Response().successMessage({"items":serializer.data,"checkedGoodsAmount":checkedGoodsAmount},status=status.HTTP_200_OK)

           

    @swagger_auto_schema(
    operation_description="获取商品类别列表",
    manual_parameters=[
        
    ],
    responses={404:"找不到数据",
               203:"用户需要登录",
    },
    security=[]
    )
    def get(self,request,format=None):

        # --------------------------------------
        # 获取用户key
        user_key = request.META.get("HTTP_SESSION_KEY")
        # 查找用户是否合法
        try:
            user = UserProfile.objects.get(password=user_key)
        except:
            return Response().errorMessage(error="login requried",status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        # 获取用户详情信息
        userpro = user#UserProfile.objects.get(user=user)
        # ----------------------------------------
        
        res = MyTrolly.objects.all().filter(user=userpro)

        # 计算所选商品价格
        checked_goods = MyTrolly.objects.all().filter(user=userpro,checkbox=True)
        checkedGoodsAmount = []
        for i in checked_goods:
            checkedGoodsAmount.append(i.productbaseinfo.price * i.nums)
        checkedGoodsAmount = sum(checkedGoodsAmount)

        serializer = TrollyAllSerializer(res,many=True)
      
        return Response().successMessage({"items":serializer.data,"checkedGoodsAmount":checkedGoodsAmount},status=status.HTTP_200_OK)
    
    
    
    @swagger_auto_schema(
    operation_description="删除商品，可以多选，需要传来一个list对象,参数名称productId_list",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['productId'],
        properties={
            'productId': openapi.Schema(type=openapi.TYPE_STRING),
        },
        ),
    responses={404:"找不到数据",
               200:"删除成功",
    },
    security=[]
    )
    def delete(self,request,format=None):

        # --------------------------------------
        # 获取用户key
        user_key = request.META.get("HTTP_SESSION_KEY")
        # 查找用户是否合法
        try:
            user = UserProfile.objects.get(password=user_key)
        except:
            return Response().errorMessage(error="login requried",status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        # 获取用户详情信息
        userpro = user#UserProfile.objects.get(user=user)
        # ----------------------------------------
        
        items_list = request.data.get('productId_list')
        
        for i in items_list:
            item = MyTrolly.objects.filter(user=userpro).filter(productbaseinfo=i)
            item.delete()
        
        res = MyTrolly.objects.all().filter(user=userpro)
        serializer = TrollyAllSerializer(res,many=True)

        # 计算所选商品价格
        checked_goods = MyTrolly.objects.all().filter(user=userpro,checkbox=True)
        checkedGoodsAmount = []
        for i in checked_goods:
            checkedGoodsAmount.append(i.productbaseinfo.price * i.nums)
        checkedGoodsAmount = sum(checkedGoodsAmount)

        return Response().successMessage({"items":serializer.data,"checkedGoodsAmount":checkedGoodsAmount},status=status.HTTP_200_OK)


# 修改购物车商品数量
class trollynum(APIView):

    @swagger_auto_schema(
    operation_description="修改商品购物车数量",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['productId','num'],
        properties={
            'nums': openapi.Schema(type=openapi.TYPE_INTEGER),
            'productId': openapi.Schema(type=openapi.TYPE_STRING),
        },
        ),
    responses={404:"找不到数据",
               200:"删除成功",
    },
    security=[]
    )
    def post(self,request,format=None):

        # 传进来productId 和 nums

        # --------------------------------------
        # 获取用户key
        user_key = request.META.get("HTTP_SESSION_KEY")
        # 查找用户是否合法
        try:
            user = UserProfile.objects.get(password=user_key)
        except:
            return Response().errorMessage(error="login requried",status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        # 获取用户详情信息
        userpro = user#UserProfile.objects.get(user=user)
        # ----------------------------------------
        # 先判断获取的商品ID 是不是对滴
        product = ProductBaseInfo.objects.get(productId=request.data.get('productId'))
        if not product:
            return Response().errorMessage(error="product not exists",status=status.HTTP_400_BAD_REQUEST)
        item = MyTrolly.objects.filter(user=userpro).get(productbaseinfo=product)
        
        if request.data.get('nums') < 1:
            item.nums = 1
            item.save()
        
        item.nums = request.data.get('nums')
        item.save()

        res = MyTrolly.objects.all().filter(user=userpro)
        serializer = TrollyAllSerializer(res,many=True)

        # 计算所选商品价格
        checked_goods = MyTrolly.objects.all().filter(user=userpro,checkbox=True)
        checkedGoodsAmount = []
        for i in checked_goods:
            checkedGoodsAmount.append(i.productbaseinfo.price * i.nums)
        checkedGoodsAmount = sum(checkedGoodsAmount)
        
        return Response().successMessage({"items":serializer.data,"checkedGoodsAmount":checkedGoodsAmount},status=status.HTTP_200_OK)


# 修改选择状态
class trollycheckbox(APIView):

    @swagger_auto_schema(
    operation_description="修改选择商品状态",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['productId','isChecked'],
        properties={
            'productId': openapi.Schema(type=openapi.TYPE_STRING),
            'isChecked': openapi.Schema(type=openapi.TYPE_STRING),
        },
        ),
    responses={
               200:"选择成功",
    },
    security=[]
    )
    def post(self,request,format=None):

        # --------------------------------------
        # 获取用户key
        user_key = request.META.get("HTTP_SESSION_KEY")
        # 查找用户是否合法
        try:
            user = UserProfile.objects.get(password=user_key)
        except:
            return Response().errorMessage(error="login requried",status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        # 获取用户详情信息
        userpro = user#UserProfile.objects.get(user=user)
        # ----------------------------------------

        req = request.data
        
        for i in req:
            trolly = MyTrolly.objects.filter(user=userpro).get(productbaseinfo=i['productId'])
            trolly.checkbox = i['isChecked']
            trolly.save()

        res = MyTrolly.objects.all().filter(user=userpro)
        serializer = TrollyAllSerializer(res,many=True)

        # 计算所选商品价格
        checked_goods = MyTrolly.objects.all().filter(user=userpro,checkbox=True)
        checkedGoodsAmount = []
        for i in checked_goods:
            checkedGoodsAmount.append(i.productbaseinfo.price * i.nums)
        checkedGoodsAmount = sum(checkedGoodsAmount)

        return Response().successMessage({"items":serializer.data,"checkedGoodsAmount":checkedGoodsAmount},status=status.HTTP_200_OK)
    
