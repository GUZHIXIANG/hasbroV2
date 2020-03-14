import hashlib
import json
import logging

# tools
import requests
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

#from rest_framework.decorators import api_view
#from rest_framework.response import Response
from wechatapp.views.utils.AjaxResponse import AjaxResponse as Response

# 基本loggin 设置
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s gallant-%(name)s-views-UserManager %(levelname)s %(message)s",
                    datefmt = '%Y-%m-%d  %H:%M:%S %a'    
                    )

__all__ = ["status","Response","APIView","requests","json","openapi","swagger_auto_schema","hashlib","logging"]

# FIXME(GU)   存在会报错，需要调整位置
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
