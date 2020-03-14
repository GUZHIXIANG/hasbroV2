"""gallant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

import xadmin
xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

from django.views.static import serve
from gallant.settings import MEDIA_ROOT

schema_view = get_schema_view(
   openapi.Info(
      title="Hasbro API",
      default_version='v1',
      description="Test description",
      terms_of_service="None",
      contact=openapi.Contact(email="digital_boundary@163.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

V2_ROOT = 'api/v2/'
from product.views import *
from activity.views import *
from wechat.views import *
from user.views import *
from area.views import *
from store.views import *

urlpatterns = [
    #path('xadmin/', xadmin.site.urls),
    path('admin/', xadmin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),
    # path('api/wxapp/v1/', include('wechatapp.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    # api/v2
    path(V2_ROOT+'user/register', user_register.as_view(), name='user-register'),
    path(V2_ROOT+'home', homepage.as_view(),name='home'),
    path(V2_ROOT+'product', ProductList.as_view(),name='products'),
    path(V2_ROOT+'product/ptype', ptypelist.as_view(),name='product-ptypes'),
    path(V2_ROOT+'product/detail', productdetail.as_view(),name='product-detail'),
    path(V2_ROOT+'activity', ActivityList.as_view(),name='activities'),
    path(V2_ROOT+'activity/detail', activitydetail.as_view(),name='activity-detail'),
    path(V2_ROOT+'areas', area.as_view(), name='areas'),
    path(V2_ROOT+'address', address.as_view(), name='addresses'),
    path(V2_ROOT+'address/detail', addressdetail.as_view(), name='address-detail'),
    path(V2_ROOT+'store', storelist.as_view(), name='stores'),
    path(V2_ROOT+'join', join.as_view(), name='joins'),
    path(V2_ROOT+'join/detail', joindetail.as_view(), name='join-detail'),
    path(V2_ROOT+'trolly/item', trolly.as_view(), name='trolly'),
    path(V2_ROOT+'trolly/num', trollynum.as_view(), name='trolly'),
    path(V2_ROOT+'trolly/checkbox', trollycheckbox.as_view(), name='trolly')

]

