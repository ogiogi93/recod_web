from recod_web.settings import AWS_S3_CUSTOM_DOMAIN, ENV


class MatchEntity:
    def __init__(self, match_teams):
        self._match_teams = match_teams

    def tournament_name(self):
        if self._match_teams:
            return self._match_teams[0].match.tournament.name
        return ''

    def tournament_image(self):
        if self._match_teams:
            if ENV == 'develop':
                return 'http://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._match_teams[0].match.tournament.image)
            return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._match_teams[0].match.tournament.image)
        return ''

    def status(self):
        if self._match_teams:
            return self._match_teams[0].match.status
        return ''

    def start_date(self):
        if self._match_teams:
            return self._match_teams[0].match.start_date
        return ''

    def start_time(self):
        if self._match_teams:
            return self._match_teams[0].match.start_time
        return ''

    def home_team_name(self):
        if self._match_teams:
            return self._match_teams[0].team.name
        return ''

    def home_team_image(self):
        if self._match_teams:
            if ENV == 'develop':
                return 'http://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._match_teams[0].team.image)
            return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._match_teams[0].team.image)
        return ''

    def home_team_score(self):
        if self._match_teams:
            return self._match_teams[0].score
        return ''

    def away_team_name(self):
        if self._match_teams:
            return self._match_teams[1].team.name
        return ''

    def away_team_image(self):
        if self._match_teams:
            if ENV == 'develop':
                return 'http://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._match_teams[1].team.image)
            return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._match_teams[1].team.image)
        return ''

    def away_team_score(self):
        if self._match_teams:
            return self._match_teams[1].score
        return ''
