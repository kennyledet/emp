from django.conf.urls import patterns, include, url

urlpatterns = patterns('videos.views',
    url(r'^play/(?P<video_id>\d.*)/$', 'video'),
    url(r'^play/(?P<video_id>\d.*)/(?P<video_title_slug>[A-Za-z0-9-].*)$', 'video'),

    url(r'^$', 'videos'),
    url(r'^search/$', 'videos_search'),
    url(r'^upload/$', 'video_upload'),
    url(r'^upload/success/$', 'video_upload_success'),
    url(r'^playlist/(?P<playlist_id>\d.*)/$', 'video_playlist'),
    # TODO: implement this as AJAX
    url(r'^favorite/$', 'favorite_video'),
    # url(r'^categories/$', 'videos.views.categories' name='categories'),
    # url(r'^category/$', 'videos.views.category' name='category'),
    )