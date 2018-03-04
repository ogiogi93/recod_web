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
from django.conf.urls import include, url

import account.urls as account_urls
import article.urls as article_urls
import team.urls as team_urls
import tournament.urls as tournament_urls
import forum.urls as forum_urls
import video.urls as video_urls
from web.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # Top Page
    url(r'^$', top, name='top_page'),
    url(r'^', include(account_urls)),
    url(r'^', include(article_urls)),
    url(r'^', include(tournament_urls)),
    url(r'^', include(team_urls)),
    url(r'^', include(video_urls)),
    url(r'^', include(forum_urls)),
    # Information Page
    url(r'^contact/$', contact, name='contact_page'),
]
