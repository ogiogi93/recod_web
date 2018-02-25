from django.shortcuts import render

from account.forms import login_form
from article.repository import get_new_articles
from competition.repository.tournament import get_latest_match, get_new_matches, get_next_matches


def top(request):
    """
    トップページを返す
    :param request:
    :rtype render:
    """
    new_articles = get_new_articles()
    return render(request, 'web/index.html', context={
        'login_form': login_form,
        'topic_articles': new_articles[:3],
        'new_articles': new_articles[:4],
        'media_articles': new_articles[:4],
        'latest_match': get_latest_match(),
        'new_matches': get_new_matches(),
        'next_matches': get_next_matches()
    })


def forum(request):
    return render(request, 'web/forum.html', context={
        'login_form': login_form,
    })


def contact(request):
    return render(request, 'web/contact.html', context={
        'login_form': login_form
    })


