from django.conf.urls import url

from account.views import user_page, edit_user, login_page, logout_page, register, register_page


urlpatterns = [
    url(r'^user/(?P<user_id>\d+)/$', user_page, name='user_page'),
    url(r'^user/edit/(?P<user_id>\d+)/$', edit_user, name='edit_user_page'),
    url(r'^auth/login/$', login_page, name='login'),
    url(r'^auth/logout/$', logout_page, name='logout'),
    url(r'^auth/register/$', register, name='register'),
    url(r'^register/$', register_page, name='register_page'),
]
