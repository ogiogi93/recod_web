from recod_web.settings import AWS_S3_CUSTOM_DOMAIN, ENV

from service_api.models.teams import Member


class UserEntity:
    def __init__(self, user):
        self._user = user

    def id(self):
        return self._user.id

    def username(self):
        return self._user.username

    def nickname(self):
        return self._user.nickname

    def description(self):
        return self._user.description

    def image(self):
        if ENV == 'develop':
            return 'http://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._user.image)
        return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._user.image)

    def teams(self):
        """
        所属チームを返す
        :rtype List[Team]:
        """
        return [m.team for m in Member.objects.select_related('team').filter(user_id=self._user.id, is_active=True)]
