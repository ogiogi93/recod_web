from recod_web.settings import AWS_S3_CUSTOM_DOMAIN


class MatchEntity:
    def __init__(self, match_teams):
        self._match_teams = match_teams

    def tournament_name(self):
        return self._match_teams[0].match.tournament.name

    def tournament_image(self):
        return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._match_teams[0].match.tournament.image)

    def status(self):
        return self._match_teams[0].match.status

    def start_date(self):
        return self._match_teams[0].match.start_date

    def start_time(self):
        return self._match_teams[0].match.start_time

    def home_team_name(self):
        return self._match_teams[0].team.name

    def home_team_image(self):
        return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._match_teams[0].team.image)

    def home_team_score(self):
        return self._match_teams[0].score

    def away_team_name(self):
        return self._match_teams[1].team.name

    def away_team_image(self):
        return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._match_teams[1].team.image)

    def away_team_score(self):
        return self._match_teams[1].score


