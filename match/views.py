from service_api.models.tournaments import MatchTeam, Match
from match.entity import MatchEntity


def get_latest_match():
    """
    # FIXME: 用途的にトピックマッチを返したほうが良さそう(動画と共に)
    最新試合情報を返す
    :rtype MatchEntity:
    """
    latest_match_id = Match.objects \
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
    next_match_ids = Match.objects.values_list('id', flat=True) \
                         .filter(is_active=True, status='pending').order_by('-start_date', '-start_time')[:limit]
    next_matches = []
    for match_id in next_match_ids:
        next_matches.append(MatchEntity(MatchTeam.objects.select_related('team', 'match', 'match__tournament')
                                        .filter(match_id=match_id)))
    return next_matches
