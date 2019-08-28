"""博客项目 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views
from app02 import views as view
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^click.html/', views.click),

    url(r'^all/(?P<type_id>\d+)/', views.home),
    url(r'^check_code/', views.check_code),
    url(r'^home/', views.home),
    url(r'^home/(?P<user_name>\w+)/', views.home),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^register/', views.register),
    url(r'^blog/s/(?P<blog_name>\w+)/', views.logout),
    url(r'^blog/(?P<site>\w+)/', views.blog),
    url(r'^click.html/', views.click),
    url(r'^wangzhe.html$', views.wangzhe),
    url(r'^upload_img.html$', views.upload),
    # url(r'^(?P<site>\w+)/(?P<key>((tag)|(date)|(category)))/(?P<val>\w+-*\w*)/', views.filter),
    url(r'^(?P<site>\w+)/tag=(?P<tag_id>\d+)/', views.tag),
    url(r'^(?P<site>\w+)/tag=others/', views.tag),
    url(r'^(?P<site>\w+)/category=(?P<category_id>\d+)/', views.category),
    url(r'^(?P<site>\w+)/date_time=(?P<date_time>\d+-\d+)/', views.date_time),
    url(r'^(?P<site>\w+)/article=(?P<art>\d+)/', views.arts),
    url(r'^(?P<site>\w+)/s/article=(?P<art>\d+)/', views.logout),
    url(r'^(?P<site>\w+)/manage-(?P<article_type_id>\d+)-(?P<category_id>\d+)-(?P<tags__nid>\d+).html$', views.manage),
    url(r'^(?P<site>\w+)/new_article/$',views.new_article),

    url(r'^auth.html$',views.login),
    url(r'^test/$',view.foo),

    url(r'^reply.html', views.reply),
    url(r'^', views.home),
    # url(r'^test', views.test),
    # url(r'^', views.home),
]
