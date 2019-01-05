"""vueDjangoworkshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path,include,re_path
# 导入django自带的server
from  django.views.static import serve
from  vueDjangoworkshop.settings import MEDIA_ROOT

# rest_framework
# 自动化文档
from rest_framework.documentation import include_docs_urls

from  rest_framework.authtoken import views

import xadmin

from rest_framework.routers import DefaultRouter
# 实例化restful对象
router = DefaultRouter()

# jwt
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [

    # 后台管理配置
    path('xadmin/', xadmin.site.urls),
    # 富文本配置
    path('ueditor/', include('DjangoUeditor.urls')),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT }),
    # api连接地址
    re_path('api/', include(router.urls)),
    # 自动化文档
    path('docs/', include_docs_urls(title='mtianyan超市文档')),
    # 调试授权
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # drf自带的token授权登录,获取token需要向该地址post数据
    # path('api-token-auth/', views.obtain_auth_token),
    # path('jwt-auth/', obtain_jwt_token),
    path('login/', obtain_jwt_token),

]



