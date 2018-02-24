from article.models import Article


def get_new_articles(limit=20):
    """
    最新記事を返す
    :param int limit:
    :rtype List[Article]:
    """
    return Article.objects.select_related('user').order_by('-created_at')[:limit]
