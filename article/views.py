from django.shortcuts import render

from account.forms import login_form
from article.entity import ArticleEntity, GameEntity
from service_api.models.articles import Article
from service_api.models.disciplines import Game
from tournament.views import get_next_matches


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


def get_new_articles(enabled_game_ids, limit=20):
    """
    有効なゲームの最新記事を返す
    :param Set(int) enabled_game_ids:
    :param int limit:
    :rtype List[ArticleEntity]:
    """
    return [ArticleEntity(a) for a in Article.objects.select_related('user').filter(
        game_id__in=enabled_game_ids, is_active=True).order_by('-created_at')[:limit]]
