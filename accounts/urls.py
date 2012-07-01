from django.conf      import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('accounts.views',
    url(r'^(?P<username>[A-Za-z0-9_]*)/$', 'profile', name='profile'),

    # url(r'^$',       'accounts.views.profiles', name='profiles'),

    )