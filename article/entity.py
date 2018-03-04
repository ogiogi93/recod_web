from recod_web.settings import AWS_S3_CUSTOM_DOMAIN, ENV


class ArticleEntity:
    def __init__(self, article):
        self._article = article

    def id(self):
        return self._article.id

    def title(self):
        return self._article.title

    def url(self):
        return self._article.url or '/article/{}/'.format(self.id())

    def thumbnail_url(self):
        return self._article.thumbnail_url

    def published_date(self):
        return self._article.created_at.date()

    def updated_at(self):
        return self._article.updated_at

    def content(self):
        return self._article.content

    def short_content(self):
        if len(self._article.content) >= 50:
            return self._article.content[:50] + '...'
        return self._article.content

    def game_id(self):
        return self._article.game_id

    def game_name(self):
        return self._article.game.discipline.short_name

    def writer_id(self):
        return self._article.user.id

    def writer_name(self):
        return self._article.user.nickname

    def writer_image(self):
        if ENV == 'develop':
            return 'http://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._article.user.image)
        return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._article.user.image)


class GameEntity:
    def __init__(self, game):
        self._game = game

    def id(self):
        return self._game.id

    def short_name(self):
        return self._game.discipline.short_name
