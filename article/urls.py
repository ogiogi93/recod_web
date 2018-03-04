from django.conf.urls import url

from article.views import article, article_list


urlpatterns = [
    url(r'^article/(?P<article_id>\d+)/$', article, name='article'),
    url(r'^article/$', article_list, name='article_list'),
]
