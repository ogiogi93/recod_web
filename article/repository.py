from article.models import Article
from article.entity import ArticleEntity


def get_new_articles(limit=20):
    """
    最新記事を返す
    :param int limit:
    :rtype List[ArticleEntity]:
    """
    return [ArticleEntity(a) for a in Article.objects.select_related('user').order_by('-created_at')[:limit]]
