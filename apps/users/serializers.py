
from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
User = get_user_model()

import re
from vueDjangoworkshop.settings import REGEX_MOBILE
from datetime import datetime,timedelta

from  .models import  VerifyCode

class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def validate_code(self, code):
        pass

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")

# 手机验证码
class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)
    def validate_mobile(self, mobile):
        """
                验证手机号码(函数名称必须为validate_ + 字段名)
                """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise  serializers.ValidationError('用户已经存在')
        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE,mobile):
            raise  serializers.ValidationError('手机号码非法')
        # 验证码发送频率
        one_mintes_ago = datetime.now()-timedelta(hours=0,minutes=1,seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago,mobile=mobile).count():
            raise  serializers.ValidationError("距离上一次发送还未超过60s")

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    """
        用户详情序列化
        """
    class Meta:
        model = User
        fields = ("username", "gender", "birthday", "email", "mobile")
