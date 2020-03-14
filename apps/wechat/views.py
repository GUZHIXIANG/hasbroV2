# -*- coding: utf-8 -*-
# 每层view文件必须import
from wechat import *

# 本view层所需要模型和序列化对象
# TODO(GU)  重写用户模型
from user.models import UserWechat
from activity.models import Activity
from store.models import Store
from product.models import *
from .models import *
from .serializers import *
from django.db.models import Sum,F

class advertlist(APIView):
    '''首页轮播广告'''
    def get(self,request,format=None):
        adverts = Advert.objects.filter(is_show=True)
        if adverts.exists():
            adverts_serializer = AdvertListSerializer(adverts,many=True)
            return Response().successMessage(status=status.HTTP_200_OK,data=adverts_serializer.data)
        else:
            return Response().successMessage(status=status.HTTP_200_OK,data=[])


class address(APIView):
    '''地址创建/修改'''
    def post(self, request, format=None):
        # 获取用户key
        user_key = request.META.get("HTTP_SESSION_KEY")
        users = UserWechat.objects.filter(password=user_key)
        if users.exists():
            user = UserWechat.objects.get(password=user_key)
            data = request.data.copy()
            data['user'] = user.id
        else:
            message = "请登录"
            return Response().errorMessage(error="login requried", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, message=message)
        address_id = data.get('id')
        data['province'] = data.pop('province_id')
        data['city'] = data.pop('city_id')
        data['district'] = data.pop('district_id')
        if data.get('is_default') == True:
            old_address = Address.objects.filter(user=user.id)
            if old_address.exists():
                old_address.update(is_default=False)
        if address_id == 0:
            address_serializer = AddressOperateSerializer(
                data=data, partial=True)
        else:
            if Address.objects.filter(id=address_id).exists():
                address = Address.objects.get(id=address_id)
                address_serializer = AddressOperateSerializer(
                    instance=address, data=data, partial=True)
            else:  # 资源不存在异常
                message = "未找到指定资源"
                return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
        if address_serializer.is_valid():  # 验证数据是否合法
            address_serializer.validated_data
            address_serializer.save()
            message = "操作成功"
            return Response().successMessage(status=status.HTTP_200_OK, message=message)
        else:  # 数据非法异常
            message = address_serializer.errors
            return Response().errorMessage(status=status.HTTP_406_NOT_ACCEPTABLE, message=message)

    def delete(self, request, format=None):
        # 获取用户key
        user_key = request.META.get("HTTP_SESSION_KEY")
        users = UserWechat.objects.filter(password=user_key)
        if not users.exists():
            message = "请登录"
            return Response().errorMessage(error="login requried", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, message=message)
        address_id = request.GET.get('id')
        address_id = int(address_id)
        # 删除操作
        if Address.objects.filter(id=address_id).exists():  # 验证资源是否存在
            Address.objects.get(id=address_id).delete()
            message = "删除成功"
            return Response().successMessage(status=status.HTTP_200_OK, message=message)
        else:  # 资源不存在异常
            message = "未找到指定资源"
            return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)

    def get(self, request, format=None):
        # 获取用户key
        user_key = request.META.get("HTTP_SESSION_KEY")
        users = UserWechat.objects.filter(password=user_key)
        if users.exists():
            user = UserWechat.objects.get(password=user_key)
        else:
            message = "请登录"
            return Response().errorMessage(error="login requried", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, message=message)
        if Address.objects.filter(user=user.id).exists():  # 验证资源是否存在
            addresses = Address.objects.filter(user=user.id)
            address_serializer = AddressDetailSerializer(
                addresses, many=True)
            data = address_serializer.data.copy()
            data_new = []
            for d in data:
                d['province_id'] = d.pop('province')
                d['city_id'] = d.pop('city')
                d['district_id'] = d.pop('district')
                d['full_region'] = ''.join(
                    [d.get('province_name'), d.get('city_name'), d.get('district_name')])
                data_new.append(d)
            message = "查询成功"
            return Response().successMessage(status=status.HTTP_200_OK,
                                                message=message, data=data_new)
        else:  # 资源不存在
            message = "查询成功"
            return Response().successMessage(status=status.HTTP_200_OK,
                                                message=message, data=[])


class addressdetail(APIView):
    '''地址详情查询'''

    def get(self, request, format=None):
        # 获取用户key
        user_key = request.META.get("HTTP_SESSION_KEY")
        users = UserWechat.objects.filter(password=user_key)
        if not users.exists():
            message = "请登录"
            return Response().errorMessage(error="login requried", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, message=message)
        address_id = request.GET.get('id')
        address_id = int(address_id)
        if Address.objects.filter(id=address_id).exists():  # 验证资源是否存在
            address = Address.objects.get(id=address_id)
            address_serializer = AddressDetailSerializer(address)
            data = address_serializer.data.copy()
            data['province_id'] = data.pop('province')
            data['city_id'] = data.pop('city')
            data['district_id'] = data.pop('district')
            data['full_region'] = ''.join(
                [data.get('province_name'), data.get('city_name'), data.get('district_name')])
            message = "查询成功"
            return Response().successMessage(status=status.HTTP_200_OK,
                                                message=message, data=data)
        else:  # 资源不存在异常
            message = "未找到指定资源"
            return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)




class join(APIView):

    def post(self, request, format=None):
        '''报名创建/修改'''
        # 获取用户key
        user_key = request.META.get("HTTP_SESSION_KEY")
        users = UserWechat.objects.filter(password=user_key)
        if users.exists():
            user = UserWechat.objects.get(password=user_key)
            data = request.data.copy()
            data['user'] = user.id
        else:
            message = "请登录"
            return Response().errorMessage(error="login requried", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, message=message)
        join_id = data.get('signup_id')
        if join_id == 0:
            join_serializer = JoinOperateSerializer(
                data=data, partial=True)
        else:
            if Join.objects.filter(id=join_id).exists():
                join = Join.objects.get(id=join_id)
                join_serializer = JoinOperateSerializer(
                    instance=join, data=data, partial=True)
            else:  # 资源不存在异常
                message = "未找到指定资源"
                return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)
        if join_serializer.is_valid():  # 验证数据是否合法
            join_serializer.validated_data
            join_serializer.save()
            message = "操作成功"
            return Response().successMessage(status=status.HTTP_200_OK, message=message)
        else:  # 数据非法异常
            message = join_serializer.errors
            return Response().errorMessage(status=status.HTTP_406_NOT_ACCEPTABLE, message=message)

    def delete(self, request, format=None):
        '''报名删除'''
        # 获取用户key
        user_key = request.META.get("HTTP_SESSION_KEY")
        users = UserWechat.objects.filter(password=user_key)
        if not users.exists():
            message = "请登录"
            return Response().errorMessage(error="login requried", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, message=message)
        join_id = request.GET.get('signup_id')
        join_id = int(join_id)
        # 删除操作
        if Join.objects.filter(id=join_id).exists():  # 验证资源是否存在
            Join.objects.get(id=join_id).delete()
            message = "删除成功"
            return Response().successMessage(status=status.HTTP_200_OK, message=message)
        else:  # 资源不存在异常
            message = "未找到指定资源"
            return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)

    def get(self, request, format=None):
        '''报名列表查看'''
        # 获取用户key
        user_key = request.META.get("HTTP_SESSION_KEY")
        users = UserWechat.objects.filter(password=user_key)
        if users.exists():
            user = UserWechat.objects.get(password=user_key)
            user_id = user.id
        else:
            message = "请登录"
            return Response().errorMessage(error="login requried", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, message=message)

        if Join.objects.filter(user_id=user).exists():  # 验证资源是否存在
            signups = Join.objects.filter(
                user_id=user_id)
            signups_serializer = JoinListSerializer(signups, many=True)
            message = "查询成功"
            return Response().successMessage(status=status.HTTP_200_OK, message=message, data=signups_serializer.data)
        else:  # 资源不存在
            message = "查询成功"
            return Response().successMessage(status=status.HTTP_200_OK,message=message, data=[])


class joindetail(APIView):
    '''报名详情查询'''

    def get(self, request, format=None):
        # 获取用户key
        user_key = request.META.get("HTTP_SESSION_KEY")
        users = UserWechat.objects.filter(password=user_key)
        if not users.exists():
            message = "请登录"
            return Response().errorMessage(error="login requried", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, message=message)
        join_id = request.GET.get('signup_id')
        join_id = int(join_id)
        if Join.objects.filter(id=join_id).exists():  # 验证资源是否存在
            join = Join.objects.get(id=join_id)
            join_serializer = JoinListSerializer(join)
            data = join_serializer.data.copy()
            message = "查询成功"
            return Response().successMessage(status=status.HTTP_200_OK,
                                             message=message, data=data)
        else:  # 资源不存在异常
            message = "未找到指定资源"
            return Response().errorMessage(status=status.HTTP_404_NOT_FOUND, message=message)


class trolly(APIView):

    def post(self, request, format=None):
        user_key = request.META.get("HTTP_SESSION_KEY")
        # 查找用户是否合法
        try:
            user = UserWechat.objects.get(password=user_key)
        except:
            return Response().errorMessage(error="login requried", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        pinfo_id = request.data.get('id')
        if Pinfo.objects.filter(id=pinfo_id).exists():
            pinfo = Pinfo.objects.get(id=pinfo_id)
        else:
            return Response().errorMessage(error="product not exists", status=status.HTTP_400_BAD_REQUEST)

        if Trolly.objects.filter(user=user, pinfo=pinfo).exists():
            goods = Trolly.objects.get(user=user, pinfo=pinfo)
            goods.nums += request.data.get('nums')
            goods.save()

        else:
            nums = 1 or request.data.get('nums')
            Trolly.objects.create(user=user, pinfo=pinfo,nums=nums)

        trolly = Trolly.objects.filter(user=user)
        trolly_serializer = TrollyListSerializer(trolly, many=True)

        total = Trolly.objects.filter(user=user, checkbox=True).aggregate(
            amount=Sum(F('pinfo__price')*F('nums')))

        return Response().successMessage({"items": trolly_serializer.data, "checkedGoodsAmount": total['amount']}, status=status.HTTP_200_OK)


    def get(self, request, format=None):

        user_key = request.META.get("HTTP_SESSION_KEY")
        try:
            user = UserWechat.objects.get(password=user_key)
        except:
            return Response().errorMessage(error="login requried", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        userpro = UserWechat.objects.get(user=user)
        res = Trolly.objects.filter(user=userpro)

        total = Trolly.objects.filter(user=user, checkbox=True).aggregate(
            amount=Sum(F('pinfo__price')*F('nums')))

        serializer = TrollyListSerializer(res, many=True)

        return Response().successMessage({"items": serializer.data, "checkedGoodsAmount": total['amount']}, status=status.HTTP_200_OK)


    def delete(self, request, format=None):

        user_key = request.META.get("HTTP_SESSION_KEY")
        try:
            user = UserWechat.objects.get(password=user_key)
        except:
            return Response().errorMessage(error="login requried", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        userpro = UserWechat.objects.get(user=user)

        items_list = request.data.get('productId_list')

        for i in items_list:
            item = Trolly.objects.filter(
                user=userpro,product=i)
            if item.exists():
                item.delete()

        res = Trolly.objects.filter(user=userpro)
        serializer = TrollyListSerializer(res, many=True)

        total = Trolly.objects.filter(user=user, checkbox=True).aggregate(
            amount=Sum(F('pinfo__price')*F('nums')))

        return Response().successMessage({"items": serializer.data, "checkedGoodsAmount": total['amount']}, status=status.HTTP_200_OK)


# 修改购物车商品数量
class trollynum(APIView):

    def post(self, request, format=None):

        user_key = request.META.get("HTTP_SESSION_KEY")
        try:
            user = UserWechat.objects.get(password=user_key)
        except:
            return Response().errorMessage(error="login requried", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        userpro = UserWechat.objects.get(user=user)

        pinfo = Pinfo.objects.filter(
            id=request.data.get('id'))
        if not pinfo.exists():
            return Response().errorMessage(error="product not exists", status=status.HTTP_400_BAD_REQUEST)
        if Trolly.objects.filter(user=userpro,product=product).exists():
            item = Trolly.objects.get(user=userpro,product=product)
            if request.data.get('nums') < 1:
                item.nums = 1
                item.save()

            item.nums = request.data.get('nums')
            item.save()

        res = Trolly.objects.filter(user=userpro)
        serializer = TrollyListSerializer(res, many=True)

        total = Trolly.objects.filter(user=user, checkbox=True).aggregate(
            amount=Sum(F('pinfo__price')*F('nums')))

        return Response().successMessage({"items": serializer.data, "checkedGoodsAmount": total['amount']}, status=status.HTTP_200_OK)


# 修改选择状态
class trollycheckbox(APIView):

    def post(self, request, format=None):

        user_key = request.META.get("HTTP_SESSION_KEY")
        try:
            user = UserWechat.objects.get(password=user_key)
        except:
            return Response().errorMessage(error="login requried", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        userpro = UserWechat.objects.get(user=user)

        req = request.data

        for i in req:
            if Trolly.objects.filter(user=userpro,id=i['id']).exists():
                trolly = Trolly.objects.get(user=userpro,id=i['id'])
                trolly.checkbox = i['isChecked']
                trolly.save()

        res = Trolly.objects.filter(user=userpro)
        serializer = TrollyListSerializer(res, many=True)

        total = Trolly.objects.filter(user=user, checkbox=True).aggregate(
            amount=Sum(F('pinfo__price')*F('nums')))

        return Response().successMessage({"items": serializer.data, "checkedGoodsAmount": total['amount']}, status=status.HTTP_200_OK)


class homepage(APIView):
    @swagger_auto_schema(
        operation_description="获取商品首页所有信息*",
        responses={200: "success"
                   },
        security=[]
    )
    def get(self, request, format=None):
        '''首页信息'''
        type_list = PType.objects.filter(desc=2)
        tag_hot = PTag.objects.get(name='热门商品').product.all()
        tag_new = PTag.objects.get(name='新品上架').product.all()
        tag_discount = PTag.objects.get(name='降价促销').product.all()
        goodsCount = ProductBaseInfo.objects.all().count()
        adverts = Advert.objects.all() 


        channel = PTypeSerializer(type_list, many=True)
        hotgoods = ProductAllSerializer(tag_hot, many=True)
        newgoods = ProductAllSerializer(tag_new, many=True)
        discountgoods = ProductAllSerializer(tag_discount, many=True)        
        rollAdvPic = AdvertListSerializer(adverts, many=True)


        return Response().successMessage({"hotgoods": hotgoods.data,
                                          "newgoods": newgoods.data,
                                          "discountgoods": discountgoods.data,
                                          "rollAdvPic": rollAdvPic.data,
                                          "channel": channel.data,
                                          "goodsCount": goodsCount
                                          }, status=status.HTTP_200_OK)