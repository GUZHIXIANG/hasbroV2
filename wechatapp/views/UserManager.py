# 每层view文件必须import
from wechatapp.views import *

# 本view层所需要模型和序列化对象
# from django.contrib.auth.models import User
from user.models import UserProfile
from wechatapp.serializers.UserRegisterSerializer import UserWxInfoSerializer,UserBaseInfoSerializer


class user_register(APIView):
    # System Requrie WechatApp provide User Code
    # 该接口仅仅为微信用户授权注册使用 返回成功或者失败
    # 初次用户注册时记录数据 并且计算gsession_key
    # 非初次用户gsession_key 过期情况下使用该接口更新新gsession_key
    # test_param = openapi.Parameter("id", openapi.IN_QUERY, description="test manual param",
    #                                type=openapi.TYPE_INTEGER)

    # @swagger_auto_schema(operation_description="partial_update description override",
    #                      responses={404: 'id not found'},
    #                      manual_parameters=[test_param])
    # def get(self, request, format=None):
        
    #     return Response().successMessage("hello world",status=status.HTTP_200_OK)

    @swagger_auto_schema(
    operation_description="微信小程序用户验证接口",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['code', "gender","city","province","country","language","avatarUrl","nickName"],
        properties={
            'nickName': openapi.Schema(type=openapi.TYPE_STRING),
            'gender': openapi.Schema(type=openapi.TYPE_STRING),
            'city': openapi.Schema(type=openapi.TYPE_STRING),
            'province': openapi.Schema(type=openapi.TYPE_STRING),
            'country': openapi.Schema(type=openapi.TYPE_STRING),
            'language': openapi.Schema(type=openapi.TYPE_STRING),
            'avatarUrl': openapi.Schema(type=openapi.TYPE_STRING),
            'code': openapi.Schema(type=openapi.TYPE_STRING),

        },
    ),
    responses={200:""},
    security=[]
    )
    def post(self, request, format=None): 
        wechat_user_code = request.data.get('code')
        
        if not wechat_user_code:
            return Response().errorMessage(message="USER CODE NULL", status=status.HTTP_400_BAD_REQUEST)
        
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format("wx2d34d6cbf1442dfb", '98fb02af464be7a252f0768ff2359400', wechat_user_code)
        
        user_wx_keys = json.loads(requests.get(url).text)
        openid = user_wx_keys['openid'] if 'openid' in user_wx_keys else None
        session_key = user_wx_keys['session_key'] if 'session_key' in user_wx_keys else None
        if not openid:
            return Response().errorMessage(message="SERVER CAN'T GET OPENID", status=status.HTTP_404_NOT_FOUND)
        
        def __get_gsession_key__(openid,session_key):
            # 生成session数字签名
            sha = hashlib.sha1()
            sha.update(openid.encode())
            sha.update(session_key.encode())
            digest = sha.hexdigest()
            return digest
        
        # create / update 
        try:
            # 1. checking if user is exist let's update our new gsession_key
            user = User.objects.get(username=openid)

            userpro = user
            serializer = UserWxInfoSerializer(userpro)
            # 2. update new key    this.password = session_key
            logging.debug("caculate session_key,{}".format(__get_gsession_key__(openid,session_key)))
            user.password = __get_gsession_key__(openid,session_key)
            user.save()
            
          
            return Response().successMessage({'userinfo':serializer.data,'session_key':__get_gsession_key__(openid,session_key)},status=status.HTTP_200_OK)

        except Exception:   
            
            # 2. creating if user is new 
            try:
                data = {"username":openid,"password":__get_gsession_key__(openid,session_key)}
                request.data['user'] = data
                serializer_userinfo = UserWxInfoSerializer(data=request.data)

                if serializer_userinfo.is_valid():
                    serializer_userinfo.validated_data
                    serializer_userinfo.save()

                return Response().successMessage({'userinfo':serializer_userinfo.data,'session_key':__get_gsession_key__(openid,session_key)},status=status.HTTP_200_OK)
            except Exception:
                return Response().errorMessage(status=status.HTTP_406_NOT_ACCEPTABLE)