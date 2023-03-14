"""
该部分为企业专家区别于普通用户和专家的属性，与企业User为一对一关系
"""

from django.db import models


class Enterprise_info(models.Model):
    create_time = models.DateTimeField(auto_now=True, null=True)
    #企业名
    name = models.CharField(max_length=100, blank=True, null=True)
    #地址
    address = models.CharField(max_length=100, blank=True, null=True)
    #官网
    website = models.CharField(max_length=50, blank=True, null=True)
    #简介
    instruction = models.CharField(max_length=200, blank=True, null=True)
    #电话
    phone = models.CharField(max_length=20, blank=True, null=True)
    #法定代表人
    legal_representative = models.CharField(max_length=100)
    #注册资本
    register_capital = models.IntegerField()
    #主营业务
    field = models.CharField(max_length=100)
    #营业执照
    business_license = models.ImageField(upload_to="images/%Y%m/%d/icons",
                                         default='images/default_user_icon.jpg')
    #法人身份证
    legal_person_ID = models.ImageField(upload_to="images/%Y%m/%d/icons",
                                        default='images/default_user_icon.jpg')