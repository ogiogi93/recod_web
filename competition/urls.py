from django.conf.urls import url

from competition.views import tournament_list

urlpatterns = [
    url(r'^tournament/$', tournament_list, name='tournament_list_page'),
]
