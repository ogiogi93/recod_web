from django.conf.urls import url

from tournament.views import participate_tournament, tournament_page, tournament_list, refusal_tournament

urlpatterns = [
    url(r'^tournament/(?P<tournament_id>\d+)/$', tournament_page, name='tournament_page'),
    url(r'^tournament/$', tournament_list, name='tournament_list_page'),
    url(r'^team/(?P<team_id>\d+)/refusal/tournament/(?P<tournament_id>\d+)/$', refusal_tournament,
        name='refusal_tournament'),
    url(r'^team/(?P<team_id>\d+)/participate/$', participate_tournament, name='participate_tournament'),
]
