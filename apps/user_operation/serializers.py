from rest_framework import serializers

from  .models import  *




class AddressSerializer(serializers.ModelSerializer):
    # HiddenField的值不依靠输入，而需要设置默认的值，不需要用户自己post数据过来，也不会显式返回给用户，最常用的就是user!!
    # 　　我们在登录情况下，进行一些操作，假设一个用户去收藏了某一门课，那么后台应该自动识别这个用户，然后用户只需要将课程的id
    # post过来，那么这样的功能，我们配合CurrentUserDefault()
    # 实现。# 这样就可以直接获取到当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")

