from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from account.forms import login_form
from team.entity import TeamEntity
from tournament.api.tournaments import upsert_api_participate, refusal_api_participate
from tournament.entity import TournamentEntity
from tournament.forms import ParticipateTournamentForm
from service_api.models.teams import Team
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


def tournament_page(request, tournament_id):
    return render(request, 'web/tournament/tournament.html', context={
        'login_form': login_form,
        'next_matches': get_next_matches(),
        'tournament': TournamentEntity(Tournament.objects.select_related('game__discipline', 'game__discipline')
                                       .get(pk=tournament_id)),
        'participate_teams': [TeamEntity(p.team) for p in
                              Participate.objects.select_related('team').filter(tournament_id=tournament_id)]
    })


@login_required
def participate_tournament(request, team_id):
    """
    トーナメントに参加する
    :param request:
    :param int team_id:
    :rtype redirect:
    """
    if request.method == 'POST':
        form = ParticipateTournamentForm(request.POST,
                                         initial={'team': Team.objects.get(pk=team_id)})
        # 既に登録済みの大会は除く
        form.fields['tournament'].queryset = Tournament.objects.filter(is_active=True).exclude(
            participate__team__id=team_id)
        if form.is_valid():
            form.instance.team = Team.objects.get(pk=team_id)
            # Toornament APIの方にも登録しておく
            api_participate_id = upsert_api_participate(form.instance.team,
                                                        api_tournament_id=form.instance.tournament.api_tournament_id)
            form.instance.api_participate_id = api_participate_id
            form.save()
            return redirect('/team/{}/'.format(team_id))
        return render(request, 'web/tournament/participate_tournament.html', context={
            'login_form': login_form,
            'form': form,
            'team_id': team_id
        })
    form = ParticipateTournamentForm()
    # 既に登録済みの大会は除く
    form.fields['tournament'].queryset = Tournament.objects.filter(is_active=True).exclude(
        participate__team__id=team_id)
    return render(request, 'web/tournament/participate_tournament.html', context={
        'login_form': login_form,
        'form': form,
        'team_id': team_id
    })


@login_required
def refusal_tournament(request, team_id, tournament_id):
    """
    大会参加を辞退する
    :param request:
    :param int team_id:
    :param int tournament_id:
    :rtype redirect:
    """
    team = Team.objects.get(pk=team_id)
    tournament = Tournament.objects.get(pk=tournament_id)
    if team and tournament:
        participate = Participate.objects.filter(team=team, tournament=tournament).first()
        refusal_api_participate(api_tournament_id=participate.tournament.api_tournament_id,
                                api_participate_id=participate.api_participate_id)
        participate.delete()
    return redirect('/team/{}/'.format(team_id))
