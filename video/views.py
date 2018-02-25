from django.shortcuts import render

from account.forms import login_form
from article.repository import get_new_articles
from competition.repository.tournament import get_new_matches, get_next_matches


def video_list(request):
    return render(request, 'web/video/video_list.html', context={
        'login_form': login_form,
        'articles': get_new_articles(),
        'next_matches': get_next_matches()
    })


def live(request):
    return render(request, 'web/video/live.html', context={
        'login_form': login_form,
        'next_matches': get_next_matches(),
        'new_matches': get_new_matches(),
    })
