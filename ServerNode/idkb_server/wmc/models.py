from django.db import models

# Create your models here.



from django.contrib.auth.models import AbstractUser
import pickle
import uuid



"""
username: 用户名字段，用于登录和唯一标识用户。
first_name: 用户的名字。
last_name: 用户的姓氏。
email: 用户的电子邮件地址。
password: 用户的密码（以哈希形式存储）。
is_staff: 一个布尔字段，指示用户是否是员工。通常用于控制用户是否可以访问后台管理界面。
is_active: 一个布尔字段，指示用户是否处于活动状态。可以使用此字段来禁用或启用用户账号。
date_joined: 用户加入系统的日期时间。
"""
class User(AbstractUser):
    """
    该类包含了较为完整的用户数据，且可以直接用于用户验证。
    并且提供了parms存储每个用户的数据参数字段，以及简易的函数直接调用
    is_user_has_key：用户的parm有key字段返回True，否则False
    are_users_has_key：所有传入用户的parm都有key字段返回True，否则False
    get_user_dict：返回传入用户的parms的参数dict
    get_users_dict：返回传入用户的parms的参数dict的字典{id:parms}
    get_users_dict_value：返回传入用户的parms的key的值的字典{id:value}
    update_user_dict：更新用户的parms字段
    update_users_dict：更新多个用户的parms字段
    pop_user_dict_value：删除用户的parms字段
    pop_users_dict_value：删除多个用户的parms字段
    """
    MAX_BYTES=10485760
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    DEFAULT_PARMS={}
    avatar=models.ImageField(upload_to='user/avatar/',default='user/default_avatar.jpg')
    parms=models.BinaryField(verbose_name='Binary Data', max_length=MAX_BYTES,default=pickle.dumps(DEFAULT_PARMS))

    PERMISSION_CHOICES = (
        (-1, 'banned'),
        (0, 'unauth'),
        (5, 'low1'),
        (6, 'low2'),
        (7, 'low3'),
        (10, 'high1'),
        (11, 'high2'),
        (12, 'high3'),
        (21, 'admin'),
        (99, 'root'),
    )
    permisson=models.IntegerField(choices=PERMISSION_CHOICES,default=0)
    # 重写保存
    # def save(self,*args, **kwargs):
    #     if self.permission > 99:
    #         self.is_staff = True
    #         self.is_superuser = True
    #     elif self.permisson>20:
    #         self.is_staff = True
    #     else:
    #         self.is_staff = False
    #     super().save(*args, **kwargs)

    @classmethod
    def bin2dict(self,bin):
        return pickle.loads(bin)
    @classmethod
    def dict2bin(self,dict):
        return pickle.dumps(dict)
    @classmethod
    def is_user_has_key(self, user,key):
        data_dict = self.bin2dict(user.parms)
        return key in data_dict
    @classmethod
    def are_users_has_key(self, users,key):
        return all([self.is_user_has_key(user,key) for user in users])
    @classmethod
    def get_user_dict(self,user):
        return self.bin2dict(user.parms)
    @classmethod
    def get_users_dict(self,users):
        return {user.username:self.bin2dict(user.parms) for user in users}
    @classmethod
    def get_users_dict_value(self,users,key):
        return {user.username:self.bin2dict(user.parms)[key] for user in users}
    @classmethod
    def update_user_dict(self,user,key,value):
        """
        :param user:
        :param key:
        :param value:
        :return: None
        """
        parms=self.bin2dict(user.parms)
        parms[key]=value
        user.parms=self.dict2bin(parms)
        user.save()
    @classmethod
    def update_users_dicts(self,users,key,value):
        [self.update_user_dict(user,key,value) for user in users]
    @classmethod
    def drop_user_dict_value(self,user,key):
        parms=self.bin2dict(user.parms)
        parms.pop(key)
        user.parms=self.dict2bin(parms)
        user.save()
    @classmethod
    def drop_users_dict_value(self,users,key):
        [self.drop_user_dict_value(user,key) for user in users]

class AppData:
    MAX_BYTES=1024*1024*1024
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    DEFAULT_PARMS={}
    parms=models.BinaryField(verbose_name='Binary Data', max_length=MAX_BYTES,default=pickle.dumps(DEFAULT_PARMS))

    STATE_CHOICES = (
        (-1, 'banned'),
        (0, 'normal'),
    )
    staus=models.IntegerField(choices=STATE_CHOICES,default=0)

    @classmethod
    def bin2dict(self,bin):
        return pickle.loads(bin)
    @classmethod
    def dict2bin(self,dict):
        return pickle.dumps(dict)
    @classmethod
    def is_user_has_key(self, user,key):
        data_dict = self.bin2dict(user.parms)
        return key in data_dict
    @classmethod
    def are_users_has_key(self, users,key):
        return all([self.is_user_has_key(user,key) for user in users])
    @classmethod
    def get_user_dict(self,user):
        return self.bin2dict(user.parms)
    @classmethod
    def get_users_dict(self,users):
        return {user.username:self.bin2dict(user.parms) for user in users}
    @classmethod
    def get_users_dict_value(self,users,key):
        return {user.username:self.bin2dict(user.parms)[key] for user in users}
    @classmethod
    def update_user_dict(self,user,key,value):
        """
        :param user:
        :param key:
        :param value:
        :return: None
        """
        parms=self.bin2dict(user.parms)
        parms[key]=value
        user.parms=self.dict2bin(parms)
        user.save()
    @classmethod
    def update_users_dicts(self,users,key,value):
        [self.update_user_dict(user,key,value) for user in users]
    @classmethod
    def drop_user_dict_value(self,user,key):
        parms=self.bin2dict(user.parms)
        parms.pop(key)
        user.parms=self.dict2bin(parms)
        user.save()
    @classmethod
    def drop_users_dict_value(self,users,key):
        [self.drop_user_dict_value(user,key) for user in users]


