from django.shortcuts import render

from account.forms import login_form
from article.entity import ArticleEntity, GameEntity
from article.repository import get_new_articles
from article.models import Article
from competition.models import Game
from competition.repository.tournament import get_next_matches


def article_list(request):
    enabled_games = Game.objects.select_related('discipline').filter(is_active=True)
    return render(request, 'web/article/article_list.html', context={
        'login_form': login_form,
        'games': [GameEntity(eg) for eg in enabled_games],
        'default_select_game_id': 1,
        'articles': get_new_articles(set(eg.id for eg in enabled_games)),
    })


def article(request, article_id):
    return render(request, 'web/article/article.html', context={
        'login_form': login_form,
        'article': ArticleEntity(Article.objects.select_related('user').get(pk=article_id)),
        'next_matches': get_next_matches()
    })


