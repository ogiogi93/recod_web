from django.conf.urls import url

from forum.views import (
    upsert_forum, delete_forum,
    upsert_thread, delete_thread,
    upsert_topic, delete_topic,
    thread_list, topic_list,
    forum_list
)


urlpatterns = [
    url(r'^forum/(?P<forum_id>\d+)/(?P<topic_id>\d+)/edit/(?P<thread_id>\d+)/$', upsert_thread, name='edit_thread'),
    url(r'^forum/(?P<forum_id>\d+)/(?P<topic_id>\d+)/delete/(?P<thread_id>\d+)/$', delete_thread, name='delete_thread'),
    url(r'^forum/(?P<forum_id>\d+)/(?P<topic_id>\d+)/create/$', upsert_thread, name='create_thread'),
    url(r'^forum/(?P<forum_id>\d+)/(?P<topic_id>\d+)/$', thread_list, name='thread_page'),
    url(r'^forum/(?P<forum_id>\d+)/edit/(?P<topic_id>\d+)/$', upsert_topic, name='edit_topic'),
    url(r'^forum/(?P<forum_id>\d+)/delete/(?P<topic_id>\d+)/$', delete_topic, name='delete_topic'),
    url(r'^forum/(?P<forum_id>\d+)/create/$', upsert_topic, name='create_topic'),
    url(r'^forum/(?P<forum_id>\d+)/$', topic_list, name='topic_page'),
    url(r'^forum/edit/(?P<forum_id>\d+)/$', upsert_forum, name='edit_forum'),
    url(r'^forum/delete/(?P<forum_id>\d+)/$', delete_forum, name='delete_forum'),
    url(r'^forum/create/$', upsert_forum, name='create_forum'),
    url(r'^forum/$', forum_list, name='forum_page'),
]
