#coding=utf-8
from django.contrib.auth.models import User


#看某个用户名是否存在
def user_exist(username):
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        return False
    return True