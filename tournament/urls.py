from django.conf.urls import url

from tournament.views import tournament, tournament_list

urlpatterns = [
    url(r'^tournament/(?P<tournament_id>\d+)/$', tournament, name='tournament_page'),
    url(r'^tournament/$', tournament_list, name='tournament_list_page'),
]
