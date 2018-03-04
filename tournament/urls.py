from django.conf.urls import url

from tournament.views import participate_tournament, tournament, tournament_list

urlpatterns = [
    url(r'^tournament/(?P<tournament_id>\d+)/$', tournament, name='tournament_page'),
    url(r'^tournament/$', tournament_list, name='tournament_list_page'),
    url(r'^team/(?P<team_id>\d+)/participate/$', participate_tournament, name='participate_tournament'),
]
