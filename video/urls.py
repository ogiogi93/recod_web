from django.conf.urls import url

from video import views


urlpatterns = [
    url(r'^live/$', views.live, name='live_page'),
    url(r'^video/$', views.video_list, name='video_list_page'),
]
