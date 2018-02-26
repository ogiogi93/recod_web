from django.conf.urls import url

from competition import views

urlpatterns = [
    url(r'^tournament/(?P<tournament_id>\d+)/$', views.tournament, name='tournament_page'),
    url(r'^tournament/$', views.tournament_list, name='tournament_list_page'),
]
