from competition.models import Member, Team
from competition.entity.team import TeamEntity


def get_teams():
    """
    各チーム情報を登録順で返す
    :rtype List[TeamEntity]:
    """
    return [TeamEntity(t)
            for t in Team.objects.select_related('game', 'game__discipline', 'game__platform').filter(
            game__discipline__is_active=True)]


def get_belong_teams(user_id):
    """
    指定されたユーザが所属するチーム情報を返す
    :param user_id:
    :rtype List[TeamEntity]:
    """
    return [TeamEntity(team=m.team, user_id=user_id) for m in
            Member.objects.select_related('team', 'team__game__discipline', 'team__game__platform').filter
            (user_id=user_id, is_active=True)]
