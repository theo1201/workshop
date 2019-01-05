from django.shortcuts import render
from  django.db.models import Q
# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from rest_framework import viewsets,mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
# 发送验证码是创建model中一条记录的操作
from rest_framework.mixins import CreateModelMixin
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework import status
from rest_framework.response import Response

from .serializers import *

from random import choice



User = get_user_model()
class CustomBackend(ModelBackend):
    """
    自定义用户验证规则
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因
            # 后期可以添加邮箱验证
            user = User.objects.get(
                Q(username=username) | Q(mobile=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     mobile = serializer.validated_data["mobile"]
    #     # 云片网设置



class UserViewset(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    # jwt认证的ViewSet的类里面设置
    # 并在列表页中添加单独的auth认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 用户注册之后自动帮他登录了
    # 重写create方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        # 在新建用户保存到数据库之后
        tmp_dict = serializer.data
        # 生成JWT Token
        payload = jwt_payload_handler(user)
        tmp_dict['token'] = jwt_encode_handler(payload)
        headers = self.get_success_headers(serializer.data)
        return Response(tmp_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 动态Serializer配置
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegSerializer

        return UserDetailSerializer