from django.shortcuts import render

from account.forms import login_form
from competition.repository.tournament import get_next_matches
from team.repository import get_teams


def team_list(request):
    return render(request, 'web/team/team_list.html', context={
        'next_matches': get_next_matches(),
        'login_form': login_form,
        'teams': get_teams(),
    })

