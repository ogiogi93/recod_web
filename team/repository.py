from team.models import Team
from team.entity import TeamEntity


def get_teams():
    """
    各チーム情報を登録順で返す
    :rtype List[Team]:
    """
    return [TeamEntity(t)
            for t in Team.objects.select_related('game', 'game__discipline', 'game__platform').filter(
            game__discipline__is_active=True)]
