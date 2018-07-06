# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import api_view

from .forms import LoginForm,ChangeForm,ForgetForm,UploadForm
from .models import Account
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializer import AccountSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password


def login_check(request,template_name):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = LoginForm.clean_login(login_form)
            if user:
                login(request, user)
                return HttpResponseRedirect('/index')
            else:
                return HttpResponseRedirect('/fail')
    else:
        login_form = LoginForm()
    return render(request, template_name,locals())


def index(request):
    user = request.user
    account = Account.objects.get(user_id=user.id)
    return render(request, 'account/index.html',locals())


def fail(request):
    return render(request, 'account/fail.html',)


def logout_view(request):
    logout(request)
    return redirect('/')


def change_password(request):
    if request.method == 'POST':
        change_form = ChangeForm(request.POST)
        if change_form.is_valid():
            user = change_form.cleanform(request)
            # data = change_form.cleaned_data
            # old_password = data['old_password']
            # new_password = data['new_password']
            # user = authenticate(username=request.user.username, password=old_password)
            if user:
            #     user.set_password(new_password)
            #     user.save()
                return HttpResponseRedirect('/')
            # else:
            #     return HttpResponseRedirect('/fail')
        # else:
        #     return HttpResponseRedirect('/fail')
    else:
        change_form = ChangeForm()
    return render(request, 'account/change_password.html', locals())


def forget_password(request):
    if request.method == 'POST':
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            data = forget_form.cleaned_data
            username = data['username']
            email = data['email']
            try:
                user = User.objects.get(username=username, email=email)
                send_mail('aaa', 'new password:aaa222', settings.DEFAULT_FROM_EMAIL, [email, ])
                user.set_password('aaa222')
                user.save()
                return HttpResponseRedirect('/')
            except:
                return redirect('account:fail')
            # user = User.objects.get(username=username, email=email)
            # if user:
            #     send_mail('aaa','new password:aaa222',settings.DEFAULT_FROM_EMAIL,[email,])
            #     user.set_password('aaa222')
            #     user.save()
            #     return HttpResponseRedirect('/')
            # else:
            #     return redirect('account:fail')
    else:
        forget_form = ForgetForm()
    return render(request, 'account/forget_password.html', locals())


def upload(request):
    user = request.user
    account = Account.objects.get(user_id=user.id)
    if request.method == 'POST':
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            data = upload_form.cleaned_data
            account.icon = data['icon']
            account.save()
            return HttpResponseRedirect('/index')
    else:
        upload_form = UploadForm()
    return render(request, 'account/upload.html', locals())


@api_view(['GET', 'POST'])
@csrf_exempt
def api(request):
    if request.method == 'GET':
        user = request.user
        account = Account.objects.get(user_id=user.id)
        serializer = AccountSerializer(account,many=False)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def api_control(request,pk):
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AccountSerializer(account)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AccountSerializer(account,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors,status=400)

    elif request.method == 'DELETE':
        account.delete()
        return HttpResponse(status=204)