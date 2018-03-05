from django.shortcuts import render

from account.forms import login_form
from article.views import get_new_articles
from service_api.models.tournaments import Game
from match.views import get_latest_match, get_new_matches, get_next_matches


def top(request):
    """
    トップページを返す
    :param request:
    :rtype render:
    """
    enabled_games = Game.objects.select_related('discipline').filter(is_active=True)
    new_articles = get_new_articles(set(eg.id for eg in enabled_games))
    # TODO: 直す
    return render(request, 'web/index.html', context={
        'login_form': login_form,
        'topic_articles': new_articles[:3],
        'new_articles': new_articles[:4],
        'media_articles': new_articles[:4],
        'latest_match': get_latest_match(),
        'new_matches': get_new_matches(),
        'next_matches': get_next_matches()
    })


def contact(request):
    return render(request, 'web/contact.html', context={
        'login_form': login_form
    })

