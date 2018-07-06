# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from account.models import Account
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserTest(TestCase):
    def setUp(self):
        User.objects.create_user('cc','cc@cc.com','123')

    def testAccount(self):
        cc = User.objects.get(username='cc')

        # user = authenticate(username=cc.username,password=cc.)
        self.assertEqual(cc.email,'cc@cc.com')

