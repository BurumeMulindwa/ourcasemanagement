from django.urls import re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

import outwards
from accounts import views as accounts_views
from boards import views
from django.conf import settings

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^landing/$', views.landing, name='landing'),
    re_path(r'^statistics/$', views.statistics, name='statistics'),
    re_path(r'^boards_statistics/$', views.boards_statistics, name='boards_statistics'),
    re_path(r'^boards_statistics_countries/$', views.boards_statistics_countries, name='boards_statistics_countries'),
    re_path(r'^boards_statistics_instrument/$', views.boards_statistics_instrument, name='boards_statistics_instrument'),
    re_path(r'^boards/$', views.boards, name='boards'),

    re_path(r'^boards_pdf/(?P<pk>\d+)/topics_pdf/(?P<topic_pk>\d+)/$', views.board_pdf, name='board_pdf'),
    re_path(r'board_contact', views.board_pdf, name='board_contact'),
    re_path(r'^outwards/$', views.outwards, name='outwards'),
    re_path(r'^signup/$', accounts_views.signup, name='signup'),
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    re_path(r'^settings/account/$', accounts_views.UserUpdateView.as_view(), name='my_account'),

    re_path(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    re_path(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    re_path(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    re_path(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    re_path(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'),
        name='password_change_done'),

    re_path(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    re_path(r'^boards/(?P<pk>\d+)/history/$', views.topic_history, name='topic_history'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/alert/$', views.topic_alerts, name='topic_alerts'),
    re_path(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.topic_posts, name='topic_posts'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),
    re_path(r'^outwards/(?P<pk>\d+)/$', views.outward_cases, name='outward_cases'),
    re_path(r'^outwards_statistics/$', views.outwards_statistics, name='outwards_statistics'),
    re_path(r'^outwards_statistics_countries/$', views.outwards_statistics_countries,
        name='outwards_statistics_countries'),
    re_path(r'^outwards_statistics_instrument/$', views.outwards_statistics_instrument,
        name='outwards_statistics_instrument'),

    re_path(r'^outwards/(?P<pk>\d+)/cases/(?P<case_pk>\d+)/alert/$', views.case_alerts, name='case_alerts'),
    re_path(r'^outwards/(?P<pk>\d+)/new/$', views.new_case, name='new_case'),
    re_path(r'^outwards/(?P<pk>\d+)/cases/(?P<case_pk>\d+)/$', views.case_updates, name='case_updates'),
    re_path(r'^outwards/(?P<pk>\d+)/history/$', views.case_history, name='case_history'),
    re_path(r'^outwards/(?P<pk>\d+)/cases/(?P<case_pk>\d+)/reply/$', views.reply_case, name='reply_case'),
    re_path(r'outwards_pdf/(?P<pk>\d+)/cases_pdf/(?P<case_pk>\d+)/$', views.outward_pdf, name='outward_pdf'),
    re_path(r'outward_contact', views.board_pdf, name='outward_contact'),
    re_path(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)