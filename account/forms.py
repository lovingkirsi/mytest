# -*- coding: utf-8 -*-
from django import forms
import re
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect, HttpResponse


def password_validate(self):
    password_re = re.compile(r'^[a-zA-Z0-9]{6,10}$')
    if not password_re.match(self):
        raise ValidationError('格式错误')


class LoginForm(forms.Form):
    username = forms.CharField(label='username',max_length=100)
    password = forms.CharField(label='password',max_length=100,widget=forms.PasswordInput)

    def clean_login(self):
        username = self.cleaned_data.get('username','')
        password = self.cleaned_data.get('password','')
        print(username,password)
        user = authenticate(username=username, password=password)
        return user


class HttpResponse(object):
    pass


class ChangeForm(forms.Form):
    old_password = forms.CharField(label='old_password',max_length=100,widget=forms.PasswordInput)
    new_password = forms.CharField(label='new_password', max_length=100,validators=[password_validate,],widget=forms.PasswordInput)
    new_password_again = forms.CharField(label='old_password_again', max_length=100,widget=forms.PasswordInput)

    def clean_new_password_again(self):
        data = self.cleaned_data
        new_password_again = data.get('new_password_again', '')
        new_password = data.get('new_password', '')
        if new_password != new_password_again:
            raise ValidationError('error')
        return data

    def cleanform(self,request):
        response = {
            'status': 'fail',
            'msg': ''
        }
        old_password = self.cleaned_data.get('old_password', '')
        user = authenticate(username=request.user.username,password=old_password)
        if user:
            new_password = self.cleaned_data.get('new_password', '')
            user.set_password(new_password)
            user.save()
        else:
            response['msg'] = '错误'
            return response
            # raise ValidationError(u'旧密码错误')
        return user


class ForgetForm(forms.Form):
    username = forms.CharField(label='username',max_length=100)
    email = forms.EmailField(label='email')


class UploadForm(forms.Form):
    icon = forms.ImageField()


