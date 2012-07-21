from django.conf      import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('emp.apps.profiles.views',
    url(r'^(?P<username>[A-Za-z0-9_]*)/$', 'user_profile', name='profile'),

    # url(r'^$',       'accounts.views.profiles', name='profiles'),

    )