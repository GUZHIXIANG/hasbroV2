# 每层view文件必须import
from user import *

# 本view层所需要模型和序列化对象
# TODO(GU)  重写用户模型
# from django.contrib.auth.models import User
from .models import UserWechat
from .serializers import UserWechatSerializer



class user_register(APIView):

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

        def __get_gsession_key__(openid, session_key):
            '''生成session数字签名'''
            sha = hashlib.sha1()
            sha.update(openid.encode())
            sha.update(session_key.encode())
            digest = sha.hexdigest()
            return digest

        if UserWechat.objects.filter(username=openid).exists():
            userpro = UserWechat.objects.filter(username=openid)
            logging.debug("caculate session_key,{}".format(__get_gsession_key__(openid,session_key)))
            userpro.password = __get_gsession_key__(openid,session_key)
            userpro.save()
            serializer = UserWechatSerializer(userpro)

            return Response().successMessage({'userinfo': serializer.data, 'session_key': __get_gsession_key__(openid, session_key)}, status=status.HTTP_200_OK)
        else:
            data = request.data.copy()
            data["username"] = openid
            data["password"] = __get_gsession_key__(openid, session_key)
            data['type'] = 1             
            user_serializer = UserWechatSerializer(data=data)

            if user_serializer.is_valid():
                user_serializer.validated_data
                user_serializer.save()
                return Response().successMessage({'userinfo': user_serializer.data, 'session_key': __get_gsession_key__(openid, session_key)}, status=status.HTTP_200_OK)
            else:
                return Response().errorMessage(status=status.HTTP_406_NOT_ACCEPTABLE)
