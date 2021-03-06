from django.conf.urls import patterns, include, url
""" Generic Views """
from django.views.generic.list_detail import object_list
from voting.views import xmlhttprequest_vote_on_object
""" Models """
from emp.apps.videos.models import Video, VideoCategory

categories_list_dict = {
    'queryset': VideoCategory.objects.all(),
    'template_object_name': 'category',
    'template_name': 'videos/video_categories.html'

}

urlpatterns = patterns('emp.apps.videos.views',
    url(r'^play/(?P<video_id>\d+)/$', 'video'),
    url(r'^play/(?P<video_id>\d+)/(?P<video_title_slug>[-\w]+)/$', 'video'),

    url(r'^$', 'videos'),
    url(r'^search/$', 'videos_search'),
    url(r'^categories/$', object_list, categories_list_dict),
    url(r'^category/(?P<category_id>\d+)/$', 'video_category'),
    url(r'^upload/$', 'video_upload'),
    url(r'^upload/success/$', 'video_upload_success'),
    url(r'^playlist/(?P<playlist_id>\d+)/$', 'video_playlist'),
    url(r'^playlist/(?P<playlist_id>\d+)/(?P<playlist_title_slug>[-\w]+)/$', 'video_playlist'),
    url(r'^playlist/add/$', 'add_to_playlist'),
    url(r'^playlist/create/$', 'create_video_playlist'),
    url(r'^playlist/import/$', 'import_playlist'),
    url(r'^favorite/$', 'favorite_video'),
    url(r'^vote/(?P<object_id>\d+)/(?P<direction>up|down|clear)$', xmlhttprequest_vote_on_object, {'model': Video}),
    
    )