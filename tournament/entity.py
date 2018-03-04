from django.utils import timezone

from recod_web.settings import AWS_S3_CUSTOM_DOMAIN, ENV


class TournamentEntity:
    def __init__(self, tournament):
        self._tournament = tournament

    def id(self):
        return self._tournament.id

    def name(self):
        return self._tournament.name

    def date_start(self):
        return self._tournament.date_start

    def description(self):
        return self._tournament.description

    def rules(self):
        return self._tournament.rules

    def prize(self):
        return self._tournament.prize

    def image(self):
        if ENV == 'develop':
            return 'http://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._tournament.image)
        return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._tournament.image)

    def website(self):
        return self._tournament.website

    def game(self):
        return self._tournament.game.discipline.name

    def platform(self):
        return self._tournament.game.platform.display_name

    def is_finished(self):
        if timezone.now().date() > self._tournament.date_start:
            return True
        return False
