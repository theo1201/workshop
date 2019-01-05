from django.shortcuts import render

# Create your views here.

from  .models import *
from .serializers import *

from rest_framework import viewsets,mixins,filters
# 引入分页类
from rest_framework.pagination import PageNumberPagination

# 缓存
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from django_filters.rest_framework import DjangoFilterBackend

# # 设置登录与未登录限速
# from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# 设置自定义filter类
from goods.filters import GoodsFilter

# 基础引入
from rest_framework.response import Response

# jWT用户认证模式
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from rest_framework.authentication import SessionAuthentication



# 商品列表分页类
class GoodsPagination(PageNumberPagination):
    # 指定每一页的个数
    page_size = 12
    # 可以让前端来设置page_szie参数来指定每页个数
    page_size_query_param = 'page_size'
    # 设置页码的参数
    page_query_param = 'page'
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
       商品列表页，分页，搜索，过滤，排序,取某一个具体商品的详情
       """
    serializer_class = GoodsSerializer
    queryset = Goods.objects.all()

    # 设置三大常用过滤器之DjangoFilterBackend, SearchFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 过滤
    # 设置filter的类为我们自定义的类
    filter_class = GoodsFilter
    # 设置排序
    ordering_fields = ('sold_num', 'shop_price')
    # 设置我们的search字段
    search_fields = ('name', 'goods_brief', 'goods_desc')

    # 设置分页
    pagination_class = GoodsPagination

    # 用户认证
    # authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 商品点击数+1
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
      list:
          商品分类列表数据
      retrieve:
          获取商品分类详情
      """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer

class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer

class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer


