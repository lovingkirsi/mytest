# -*- coding: utf-8 -*-S
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


def upload_path(self, filename):
    suffix = filename[filename.index('.'):]
    return 'upload/%s.%s/' % (self.username, suffix)


class Account(models.Model):
    username = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    age = models.IntegerField(default=0)
    email = models.EmailField(default=None)
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, primary_key=True)
    icon = models.ImageField(upload_to=upload_path, null=True, blank=True)
    result = models.CharField(max_length=200, default='late')
    url = models.URLField(default='https://baike.baidu.com/pic/手动滑稽/22206680/0/72f082025aafa40f05016cb4a764034f79f01997')
