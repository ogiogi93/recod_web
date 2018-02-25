from team.models import Team, Member
from recod_web.settings import AWS_S3_CUSTOM_DOMAIN


class TeamEntity:
    def __init__(self, team):
        self._team = team

    def id(self):
        return self._team.id

    def name(self):
        return self._team.name

    def members(self):
        return Member.objects.select_related('user').filter(team__id=self._team.id)

    def image(self):
        return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._team.image)


def get_teams():
    """
    各チーム情報を登録順で返す
    :rtype List[Team]:
    """
    return [TeamEntity(t)
            for t in Team.objects.select_related('game', 'game__discipline', 'game__platform').filter(
            game__discipline__is_active=True)]
