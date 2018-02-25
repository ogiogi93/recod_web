from django.conf.urls import url

from team.views import team_list

urlpatterns = [
    url(r'^team/$', team_list, name='team_list_page'),
]
