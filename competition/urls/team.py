from django.conf.urls import url

from competition.views import *

urlpatterns = [
    url(r'^secession_team/(?P<team_id>\d+)/$', secession_team, name='secession_team'),
    url(r'^join_team/(?P<team_id>\d+)/$', join_team, name='join_team'),
    url(r'^belong_team/$', belong_teams, name='belong_team_page'),
    url(r'^team/edit/(?P<team_id>\d+)/$', upsert_team, name='edit_team_page'),
    url(r'^team/create/$', upsert_team, name='create_team_page'),
    url(r'^team/(?P<team_id>\d+)/$', team_page, name='team_page'),
    url(r'^team/$', team_list, name='team_list_page'),
]
