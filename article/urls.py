from django.conf.urls import url

from article import views


urlpatterns = [
    url(r'^article/(?P<article_id>\d+)/$', views.article, name='article'),
    url(r'^article/$', views.article_list, name='article_list'),
]
