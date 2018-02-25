from django.utils import timezone

from competition.infrastructure.tournament import MatchTeam, Match, Tournament


class MatchEntity:
    def __init__(self, match_teams):
        self._match_teams = match_teams

    def tournament_name(self):
        return self._match_teams[0].match.tournament.name

    def tournament_image(self):
        return self._match_teams[0].match.tournament.image or 'https://talentech.co.za/assets/img/default-logo.png'

    def status(self):
        return self._match_teams[0].match.status

    def start_date(self):
        return self._match_teams[0].match.start_date

    def start_time(self):
        return self._match_teams[0].match.start_time

    def home_team_name(self):
        return self._match_teams[0].team.name

    def home_team_image(self):
        return self._match_teams[0].team.image or 'https://talentech.co.za/assets/img/default-logo.png'

    def home_team_score(self):
        return self._match_teams[0].score

    def away_team_name(self):
        return self._match_teams[1].team.name

    def away_team_image(self):
        return self._match_teams[1].team.image or 'https://talentech.co.za/assets/img/default-logo.png'

    def away_team_score(self):
        return self._match_teams[1].score


def get_latest_match():
    """
    # FIXME: 用途的にトピックマッチを返したほうが良さそう(動画と共に)
    最新試合情報を返す
    :rtype MatchEntity:
    """
    latest_match_id = Match.objects\
        .filter(is_active=True, status='completed').order_by('-start_date', '-start_time').first().id
    return MatchEntity(MatchTeam.objects.select_related('team', 'match', 'match__tournament')
                       .filter(match_id=latest_match_id))


def get_new_matches(limit=3):
    """　
    最新試合情報を返す
    :param int limit:
    :rtype List[MatchEntity]:
    """
    new_match_ids = Match.objects.values_list('id', flat=True) \
                        .filter(is_active=True, status='completed').order_by('-updated_at')[:limit]
    new_matches = []
    for match_id in new_match_ids:
        new_matches.append(MatchEntity(MatchTeam.objects.select_related('team', 'match', 'match__tournament')
                                       .filter(match_id=match_id)))
    return new_matches


def get_next_matches(limit=3):
    """
    開始前の試合情報を返す
    :param limit:
    :rtypeList[MatchEntity]:
    """
    next_match_ids = Match.objects.values_list('id', flat=True)\
        .filter(is_active=True, status='pending').order_by('-start_date', '-start_time')[:limit]
    next_matches = []
    for match_id in next_match_ids:
        next_matches.append(MatchEntity(MatchTeam.objects.select_related('team', 'match', 'match__tournament')
                                       .filter(match_id=match_id)))
    return next_matches


def get_future_tournaments(limit=5):
    """
    開催前の大会情報を返す
    :param int limit:
    :rtype:
    """
    return Tournament.objects.filter(is_active=True, date_start__gte=timezone.now())[:limit]


def get_old_tournaments(limit=10):
    """
    開催後の大会情報を返す
    :param limit:
    :return:
    """
    return Tournament.objects.filter(is_active=True, date_start__lt=timezone.now())[:limit]
