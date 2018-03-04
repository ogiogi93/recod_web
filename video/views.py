from django.shortcuts import render

from account.forms import login_form
from article.entity import GameEntity
from match.views import get_new_matches, get_next_matches
from service_api.models.videos import Video
from service_api.models.disciplines import Game


def video_list(request):
    enabled_games = Game.objects.select_related('discipline').filter(is_active=True)
    return render(request, 'web/video/video_list.html', context={
        'login_form': login_form,
        'next_matches': get_next_matches(),
        'games': [GameEntity(eg) for eg in enabled_games],
        'default_select_game_id': 2,
        'videos': Video.objects.select_related('attribute', 'attribute__game').filter(
            attribute__game__id__in=set(eg.id for eg in enabled_games))
    })


def live(request):
    return render(request, 'web/video/live.html', context={
        'login_form': login_form,
        'next_matches': get_next_matches(),
        'new_matches': get_new_matches(),
    })
