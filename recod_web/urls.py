"""gaming_site URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from web.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # Authenticate
    url(r'^auth/login/$', login_page, name='login'),
    url(r'^auth/logout/$', logout_page, name='logout'),
    url(r'^auth/register/$', register, name='register'),
    url(r'^register/$', register_page, name='register_page'),
    # Top Page
    url(r'^$', top_page, name='top_page'),
    # List Page
    url(r'^news_list/$', news_list_page, name='news_list_page'),
    url(r'^team_list/$', team_list_page, name='team_list_page'),
    url(r'^video_list/$', video_list_page, name='video_list_page'),
    # Main Page
    url(r'^article/$', article_page, name='article_page'),
    url(r'^user/$', user_page, name='user_page'),
    url(r'^forum/$', forum_page, name='forum_page'),
    url(r'^competition/$', competition_page, name='competition_page'),
    url(r'^live/$', live_page, name='live_page'),
    # Information Page
    url(r'^contact/$', contact_page, name='contact_page'),
]
