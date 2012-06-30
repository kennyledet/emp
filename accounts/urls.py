from django.conf      import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^([A-Za-z0-9_]*)/$', 'accounts.views.profile', name='profile'),

    # url(r'^$',       'accounts.views.profiles', name='profiles'),

    )