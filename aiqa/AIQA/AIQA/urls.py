"""AIQA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls.conf import include
from django.urls import path
import xadmin
xadmin.autodiscover()


urlpatterns = [
    path('', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),
    
    # **机器人配置
    path('AIQA/v1/', include('robot.urls')),

    # **后台管理
    path('mgbase/', include('mgbase.urls')),

    # **通用功能配置
    path('common/', include('common.urls')),
]
