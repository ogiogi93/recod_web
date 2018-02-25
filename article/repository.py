from article.models import Article
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


def get_new_articles(limit=20):
    """
    最新記事を返す
    :param int limit:
    :rtype List[ArticleEntity]:
    """
    return [ArticleEntity(a) for a in Article.objects.select_related('user').order_by('-created_at')[:limit]]
