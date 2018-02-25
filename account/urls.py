from django.conf.urls import url

from account import views


urlpatterns = [
    url(r'^user/(?P<user_id>\d+)/', views.user_page, name='user_page'),
    url(r'^auth/login/$', views.login_page, name='login'),
    url(r'^auth/logout/$', views.logout_page, name='logout'),
    url(r'^auth/register/$', views.register, name='register'),
    url(r'^register/$', views.register_page, name='register_page'),
]
