from wechatapp.views import *
# 用户信息模型
# from django.contrib.auth.models import User
from user.models import UserProfile
# 
from wechatapp.serializers.UserRegisterSerializer import UserWxInfoSerializer,UserBaseInfoSerializer
from wechatapp.serializers.ProductBaseInfoSerializer import ProductSerializer

from wechatapp.models.TrollyModel import MyTrolly
from wechatapp.models.ProductModel import (ProductBaseInfo)


class checkOut(APIView):


    def get(self,request,format=None):
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
        userpro = UserProfile.objects.get(user=user)
        # ----------------------------------------
        userTrolly = MyTrolly.objects.filter(user=userpro).filter(checkbox=True)
        checkedGoodsList = list()  # 所选商品列表
        goodsTotalPrice = 0        # 计算商品总价
        goodsTotalNums = 0
        for i in userTrolly:
            productSet = i.productbaseinfo
            goodsTotalPrice += productSet.price * i.nums
            goodsTotalNums += i.nums
            # TODO(GU)  序列化器不对
            serializers = ProductSerializer(productSet)
            checkedGoodsList.append({"productInfo":serializers.data,"nums":i.nums})

        return Response().successMessage({"checkedGoodsList":checkedGoodsList,"goodsTotalPrice":goodsTotalPrice,"goodsTotalNums":goodsTotalNums},status=status.HTTP_200_OK)
