from recod_web.settings import AWS_S3_CUSTOM_DOMAIN


class ArticleEntity:
    def __init__(self, article):
        self._article = article

    def id(self):
        return self._article.id

    def title(self):
        return self._article.title

    def url(self):
        return self._article.url

    def thumbnail_url(self):
        return self._article.thumbnail_url

    def published_date(self):
        return self._article.created_at.date()

    def content(self):
        return self._article.content

    def writer_id(self):
        return self._article.user.id

    def writer_name(self):
        return self._article.user.nickname

    def writer_image(self):
        return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._article.user.image)
