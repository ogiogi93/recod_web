from service_api.models.teams import Member
from recod_web.settings import AWS_S3_CUSTOM_DOMAIN


class TeamEntity:
    def __init__(self, team, user_id=None):
        self._team = team
        self._user_id = user_id

    def id(self):
        return self._team.id

    def name(self):
        return self._team.name

    def description(self):
        return self._team.description

    def members(self):
        return [m.user for m in Member.objects.select_related('user').filter(team__id=self._team.id)]

    def website(self):
        return self._team.website or ''

    def is_active(self):
        if self._team.is_active:
            return 'active'
        return 'inactive'

    def game(self):
        return self._team.game.discipline.name

    def platform(self):
        return self._team.game.platform.display_name

    def image(self):
        return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._team.image)

    def is_admin(self):
        admin_team_ids = list(Member.objects.values_list('team_id', flat=True)
                              .filter(user_id=self._user_id, is_active=True))
        if self._team.id in admin_team_ids:
            return True
        return False
