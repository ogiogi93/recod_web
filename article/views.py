from django.shortcuts import render

from account.forms import login_form
from article.repository import get_new_articles
from article.models import Article
from competition.repository.tournament import get_next_matches


def article_list(request):
    return render(request, 'web/article/article_list.html', context={
        'login_form': login_form,
        'articles': get_new_articles(),
        'next_matches': get_next_matches()
    })


def article(request, article_id):
    return render(request, 'web/article/article.html', context={
        'login_form': login_form,
        'article': Article.objects.select_related('user').get(pk=article_id),
        'next_matches': get_next_matches()
    })


