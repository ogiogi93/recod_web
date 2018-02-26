from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from account.forms import login_form
from account.models import CustomUser as User
from competition.entity.team import TeamEntity
from competition.entity.tournament import TournamentEntity
from competition.forms.team import UpsertTeamForm
from competition.models import Member, Participate, Team, Tournament
from competition.repository.tournament import (
    get_next_matches,
    get_new_matches,
    get_future_tournaments,
    get_old_tournaments
)
from competition.repository.team import get_teams, get_belong_teams


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


def team_page(request, team_id):
    return render(request, 'web/team/team.html', context={
        'next_matches': get_next_matches(),
        'login_form': login_form,
        'team': TeamEntity(team=Team.objects.select_related('game__platform', 'game__discipline').get(pk=team_id),
                           user_id=request.user.id or None)
    })


def team_list(request):
    return render(request, 'web/team/team_list.html', context={
        'next_matches': get_next_matches(),
        'login_form': login_form,
        'teams': get_teams(),
    })


@login_required
def upsert_team(request, team_id=None):
    """
    チームの新規作成・修正を行う
    :param request:
    :param int team_id:
    :return:
    """
    if request.method == 'POST':
        # 編集時
        if team_id:
            form = UpsertTeamForm(request.POST, request.FILES, instance=Team.objects.get(pk=team_id))
            if form.is_valid():
                form.save()
                return redirect('/belong_team/')
            return render(request, 'web/team/upsert_team.html', context={
                'members': Member.objects.filter(team_id=team_id).order_by('id').all(),
                'form': form
            })
        # 新規追加
        form = UpsertTeamForm(request.POST, request.FILES)
        if form.is_valid():
            new_team = form.save()

            # Team Organizerとして登録しておく
            user = User.objects.get(pk=request.user.id)
            team = Team.objects.get(pk=new_team.pk)
            Member.objects.add_member(user, team, is_admin=True)
            return redirect('/belong_team/')
        return render(request, 'web/team/upsert_team.html', context={
            'form': form,
        })
    return render(request, 'web/team/upsert_team.html', context={
        'team_id': team_id,
        'form': UpsertTeamForm(instance=Team.objects.get(pk=team_id)) if team_id else UpsertTeamForm()
    })


@login_required
def belong_teams(request):
    """
    指定されたユーザーの所属チームを返す
    :param request:
    :rtype render:
    """
    return render(request, 'web/team/upsert_belong_team.html', context={
        'nickname': User.objects.get(pk=request.user.id).nickname,
        'teams': get_belong_teams(request.user.id)
    })


@login_required
def join_team(request):
    """
    指定されたチームに所属登録する
    :param request:
    :rtype redirect:
    """
    user_id = request.user.id
    if request.method == 'POST':
        user = User.objects.get(pk=user_id)
        team = Team.objects.get(pk=request.POST.get('team_id'))
        if user and team:
            Member.objects.add_member(user, team, is_admin=False)
    return redirect('/user/{}/'.format(user_id))


@login_required
def secession_team(request, team_id):
    """
    チームから脱退する
    :param request:
    :param int team_id:
    :rtype redirect:
    """
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    team = Team.objects.get(pk=team_id)
    if user and team:
        member = Member.objects.filter(user=user).filter(team=team)
        member.delete()
        return redirect('/user/edit/{}/belong_team/'.format(user_id))
    return redirect('/user/edit/{}/belong_team/'.format(user_id))
