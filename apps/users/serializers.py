
from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
User = get_user_model()

import re
from vueDjangoworkshop.settings import REGEX_MOBILE
from datetime import datetime,timedelta

from  .models import  VerifyCode

class UserRegSerializer(serializers.ModelSerializer):
    # write_only = True这个字段不显示
    # error_messages：出错时，信息提示。
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     # UniqueValidator: 指定某一个对象是唯一的，如，用户名只能存在唯一：
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        # style: 说明字段的类型，这样看可能比较抽象，看下面例子：
        # help_text: 在指定字段增加一些提示文字，这两个字段作用于api页面比较有用
        # label: 字段显示设置
        # 它是write_only，需要用户传进来，但我们不能对它进行save()
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]
            # 有效期为5分钟
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    # 添加和删除字段
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")

# 手机验证码
class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)
    # 单独的Validate，重载validte+字段名
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
