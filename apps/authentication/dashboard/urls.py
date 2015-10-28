# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from apps.authentication.dashboard.views import UserDeleteView, UserDetailView, UserUpdateView

urlpatterns = patterns(
    'apps.authentication.dashboard.views',
    url(r'^$', 'index', name='auth_index'),
    url(r'^members/$', 'members_index', name='members_index'),
    url(r'^members/(?P<pk>\d+)/$', 'members_detail', name='members_detail'),
    url(r'^members/new/$', 'members_new', name='members_new'),
    url(r'^groups/$', 'groups_index', name='groups_index'),
    url(r'^groups/(?P<pk>\d+)/$', 'groups_detail', name='groups_detail'),
    url(r'^user/(?P<user_id>\d+)/$', UserDetailView.as_view(), name='dashboard_user_detail'),
    url(r'^user/(?P<user_id>\d+)/edit$', UserUpdateView.as_view(), name='dashboard_user_edit'),
    url(r'^user/(?P<user_id>\d+)/delete', UserDeleteView.as_view(), name='dashboard_user_delete'),
)
