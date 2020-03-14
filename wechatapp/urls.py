from django.urls import path
from wechatapp.views.UserManager import user_register
from wechatapp.views.SignUpManager import *
from wechatapp.views.ActivityManager import *
from wechatapp.views.StoreManager import *
from wechatapp.views.AddressManager import *
from wechatapp.views.ProductsInfoManager import *
from wechatapp.views.TrollyManager import trolly,trollynum,trollycheckbox
from wechatapp.views.SearchManager import itemSearch,typeForItem,wordsList
from wechatapp.views.TypeManager import *
from wechatapp.views.CheckOutManager import checkOut
from wechatapp.views.GoodsListManager import goodsList

urlpatterns = [

    # ok
    path('user/register', user_register.as_view(), name='user_register'),
    # path('test/helloworld', donothing.as_view(), name='donothing'),
    # ok
    path('signup/signup_create', signup_create.as_view(), name='signup_create'),
#     path('signup/signup_update',
#          signup_update.as_view(), name='signup_update'),
     # ok
    path('signup/signup_cancel',
         signup_cancel.as_view(), name='signup_cancel'),
     # ok 
    path('signup/signup_view',
         signup_view.as_view(), name='signup_view'),

     # 门店信息
#     path('store/store_view',
#          store_view.as_view(), name='store_view'),

     # 活动信息
     # ok
    path('activity/activity_view',
         activity_view.as_view(), name='activity_view'),
     # ok
    path('activity/activitydetail_view',
         activitydetail_view.as_view(), name='activitydetail_view'),

       # 商品种类
     # ok
     # path('product/itemtype', itemtype.as_view(), name='itemtype'),
     path('product/itemtype', itemtype2.as_view(), name='itemtype'),
     path('product/items', items.as_view(), name='items'),
     # path('product/itemspic', itemurl.as_view(), name='itemsurl'),
     # path('product/itemtag', itemtag.as_view(), name='itemtag'),

     # 商品标签
     path('product/goodsList', goodsList.as_view(), name='goodsList'),
     
     
     # 首页
     # ok
     # path('home/all', homepage.as_view(), name='homepage'),
     # path('home/hotgoods', hotgoods.as_view(), name='hot'),
     # path('home/newgoods', newgoods.as_view(), name='new'),
     # path('home/disgoods', disgoods.as_view(), name='dis'),
     # new_version
     # path('home/hotgoods', hotgoods2.as_view(), name='hot'),
     # path('home/newgoods', newgoods2.as_view(), name='new'),
     # path('home/disgoods', disgoods2.as_view(), name='dis'),
     path('home/all', homepage2.as_view(), name='homepage'),

     # 商品详情
     # ok
     path('items/detail', itemsdetail.as_view(), name='itemsdetail'),

     # 购物车
     # ok
     path('trolly/item', trolly.as_view(), name='trolly'),
     # ok
     path('trolly/num', trollynum.as_view(), name='trolly'),
     # ok
     path('trolly/checkbox', trollycheckbox.as_view(), name='trolly'),

     # 订单相关信息
     path('checkout/checked', checkOut.as_view(), name='checked'),
     

     # 搜索查询
     # ok
     path('search/items', itemSearch.as_view(), name='search'),
     # ok
     path('search/typeForItem', typeForItem.as_view(), name='typeForItem'),
     path('search/keywords', wordsList.as_view(), name='keywords'),
     
     # 省市区查询
     # path('areas', area_view.as_view(), name='areas'),
     # ok
     path('areas2', area_view2.as_view(), name='areas2'),

     # 地址管理
     # ok 
     path('address', address.as_view(), name='address'),
     # ok
     path('address/detail', address_detail.as_view(), name='address_detail'),

]  
