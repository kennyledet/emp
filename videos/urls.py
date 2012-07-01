from django.conf.urls import patterns, include, url

urlpatterns = patterns('videos.views',
    url(r'^play/(?P<video_id>\d.*)/$', 'video', name='video'),
    url(r'^$', 'videos', name='videos'),
    url(r'^search/$', 'videos_search', name='videos_search'),
    url(r'^upload/$', 'video_upload', name='video_upload'),
    url(r'^upload/success/$', 'video_upload_success', name='video_upload_success'),
    # url(r'^categories/$', 'videos.views.categories' name='categories'),
    )