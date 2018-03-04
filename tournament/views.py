from django.shortcuts import render
from django.utils import timezone

from account.forms import login_form
from team.entity import TeamEntity
from tournament.entity import TournamentEntity
from service_api.models.tournaments import Tournament, Participate
from match.views import get_next_matches, get_new_matches


def get_future_tournaments(limit=5):
    """
    開催前の大会情報を返す
    :param int limit:
    :rtype:
    """
    return [TournamentEntity(t)
            for t in Tournament.objects.filter(is_active=True, date_start__gte=timezone.now())[:limit]]


def get_old_tournaments(limit=10):
    """
    開催後の大会情報を返す
    :param limit:
    :return:
    """
    return [TournamentEntity(t)
            for t in Tournament.objects.filter(is_active=True, date_start__lt=timezone.now())[:limit]]


def tournament_list(request):
    return render(request, 'web/tournament/tournament_list.html', context={
        'login_form': login_form,
        'next_matches': get_next_matches(),
        'new_matches': get_new_matches(),
        'future_tournaments': get_future_tournaments(),
        'old_tournaments': get_old_tournaments()
    })


def tournament(request, tournament_id):
    return render(request, 'web/tournament/tournament.html', context={
        'login_form': login_form,
        'next_matches': get_next_matches(),
        'tournament': TournamentEntity(Tournament.objects.select_related('game__discipline', 'game__discipline')
                                       .get(pk=tournament_id)),
        'participate_teams': [TeamEntity(p.team) for p in
                              Participate.objects.select_related('team').filter(tournament_id=tournament_id)]
    })
