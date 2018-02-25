from django.shortcuts import render

from account.forms import login_form
from competition.repository.tournament import (
    get_next_matches,
    get_new_matches,
    get_future_tournaments,
    get_old_tournaments
)


def tournament_list(request):
    return render(request, 'web/tournament/tournament.html', context={
        'login_form': login_form,
        'next_matches': get_next_matches(),
        'new_matches': get_new_matches(),
        'future_tournaments': get_future_tournaments(),
        'old_tournaments': get_old_tournaments()
    })


