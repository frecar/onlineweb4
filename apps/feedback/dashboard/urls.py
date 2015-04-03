# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('apps.feedback.dashboard.views',
    url(r'^$', 'index', name='dashboard_feedback_index'),
    url(r'^new/$', 'new', name='dashboard_feedback_new'),
    url(r'^(?P<feedback_pk>\d+)/$', 'details', name='dashboard_feedback_details'),
    url(r'^new/textquestion/(?P<feedback_pk>\d+)$', 'new_textquestion', name='dashboard_feedback_new_textquestion'),
    url(r'^edit/textquestion/(?P<feedback_pk>\d+)/(?P<question_pk>\d+)$', 'edit_textquestion', name='dashboard_feedback_edit_textquestion'),
    url(r'^delete/textquestion/(?P<feedback_pk>\d+)/(?P<question_pk>\d+)$', 'delete_textquestion', name='dashboard_feedback_delete_textquestion'),
    url(r'^new/ratingquestion/(?P<feedback_pk>\d+)$', 'new_ratingquestion', name='dashboard_feedback_new_ratingquestion'),
    url(r'^edit/ratingquestion/(?P<feedback_pk>\d+)/(?P<question_pk>\d+)$', 'edit_ratingquestion', name='dashboard_feedback_edit_ratingquestion'),
    url(r'^delete/ratingquestion/(?P<feedback_pk>\d+)/(?P<question_pk>\d+)$', 'delete_ratingquestion', name='dashboard_feedback_delete_ratingquestion'),
    url(r'^new/mcquestion/(?P<feedback_pk>\d+)$', 'new_mcquestion', name='dashboard_feedback_new_mcquestion'),
    url(r'^edit/mcquestion/(?P<feedback_pk>\d+)/(?P<question_pk>\d+)$', 'edit_mcquestion', name='dashboard_feedback_edit_mcquestion'),
    url(r'^delete/mcquestion/(?P<feedback_pk>\d+)/(?P<question_pk>\d+)$', 'delete_mcquestion', name='dashboard_feedback_delete_mcquestion'),
)
