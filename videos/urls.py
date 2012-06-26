from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^play/(\d.*)/$', 'videos.views.video', name='video'),
    url(r'^$',       'videos.views.videos', name='videos'),
    url(r'^search/$', 'videos.views.videos_search', name='videos_search'),
    url(r'^upload/$', 'videos.views.video_upload', name='video_upload'),
    url(r'^upload/success/$', 'videos.views.video_upload_success', name='video_upload_success'),
    # url(r'^categories/$', 'videos.views.categories' name='categories'),
    )