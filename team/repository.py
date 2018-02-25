from team.models import Team, Member


def get_teams():
    """
    各チーム情報を登録順で返す
    :rtype List[Team]:
    """
    teams = Team.objects.select_related('game', 'game__discipline', 'game__platform') \
        .filter(game__discipline__is_active=True)
    # メンバー情報も取得しておく
    # TODO: Teamに詰め込むのは:no_good:
    for team in teams:
        team.members = Member.objects.select_related('user').filter(team=team)
    return teams
