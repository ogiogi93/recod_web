from account.models import Forum, Topic, Thread
from recod_web.settings import AWS_S3_CUSTOM_DOMAIN


class ForumEntity:
    def __init__(self, forum):
        self._forum = forum
        self._topic = Topic.objects.select_related('user').filter(forum=forum, is_active=True).order_by('-updated_at')

    def id(self):
        return self._forum.id

    def title(self):
        return self._forum.title

    def description(self):
        return self._forum.description

    def short_description(self):
        if len(self._forum.description) > 50:
            return self._forum.description[:50]
        return self._forum.description

    def topic_count(self):
        if self._topic:
            return str(len(self._topic))
        return '0'

    def active_topic_user(self):
        if self._topic:
            return self._topic[0].user.nickname
        return ''

    def active_topic_image(self):
        if self._topic:
            return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._topic[0].user.image)
        return ''

    def active_topic_title(self):
        if self._topic:
            return self._topic[0].title
        return ''

    def active_topic_datetime(self):
        if self._topic:
            return self._topic[0].updated_at
        return ''


class TopicEntity:
    def __init__(self, topic):
        self._topic = topic
        self._threads = Thread.objects.select_related('user', 'topic__forum').filter(topic=topic, is_active=True).order_by('-updated_at')

    def id(self):
        return self._topic.id

    def title(self):
        return self._topic.title

    def description(self):
        return self._topic.description

    def short_description(self):
        if len(self._topic.description) > 50:
            return self._topic.description[:50]
        return self._topic.description

    def thread_count(self):
        if self._threads:
            return len(self._threads)
        return '0'

    def active_thread_user(self):
        if self._threads:
            return self._threads[0].user.nickname
        return ''

    def active_thread_image(self):
        if self._threads:
            return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._threads[0].user.image)
        return ''

    def active_thread_title(self):
        if self._threads:
            return self._threads[0].title
        return ''

    def active_thread_datetime(self):
        if self._threads:
            return self._threads[0].updated_at
        return ''


class ThreadEntity:
    def __init__(self, thread):
        self._thread = thread

    def id(self):
        return self._thread.id

    def nick_name(self):
        return self._thread.user.nickname

    def user_id(self):
        return self._thread.user.id

    def user_image(self):
        return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._thread.user.image)

    def user_joined_date(self):
        return self._thread.user.date_joined

    def description(self):
        return self._thread.description

    def post_date(self):
        return self._thread.created_at
