from article.models import Article
from article.entity import ArticleEntity


def get_new_articles(enabled_game_ids, limit=20):
    """
    有効なゲームの最新記事を返す
    :param Set(int) enabled_game_ids:
    :param int limit:
    :rtype List[ArticleEntity]:
    """
    return [ArticleEntity(a) for a in Article.objects.select_related('user').filter(
        game_id__in=enabled_game_ids, is_active=True).order_by('-created_at')[:limit]]
