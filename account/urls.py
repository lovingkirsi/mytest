from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns =[
    url(r'^$', views.login_check, {'template_name':'account/login_check.html'},name='login_check'),
    url(r'^index',views.index, name='index'),
    url(r'^fail',views.fail, name='fail'),
    url(r'^logout',views.logout_view,name='logout_view'),
    url(r'^change_password',views.change_password,name='change_password'),
    url(r'^forget_password',views.forget_password,name='forget_password'),
    url(r'^upload',views.upload,name='upload'),
    url(r'^api/$',views.api,name='api'),
    url(r'^api/(?P<pk>[0-9]+)/$',views.api_control,name='api_control')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)