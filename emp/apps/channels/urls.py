from django.conf      import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('emp.apps.channels.views',
    url(r'^(?P<username>[A-Za-z0-9_]*)/$', 'user_channel', name='channel'),

    )