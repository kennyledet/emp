from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Authentication
    url(r'^user/login/$', 'django.contrib.auth.views.login'),

    url(r'^video/(\d.*)/$', 'videos.views.video', name='video'),
    url(r'^videos/$', 		'videos.views.videos', name='videos'),
    url(r'^videos/search/$', 'videos.views.videos_search', name='videos_search'),
    url(r'^video/upload/$', 'videos.views.video_upload', name='video_upload'),
    url(r'^video/upload/success/$', 'videos.views.video_upload_success', name='video_upload_success'),
    #url(r'^videos/categories/$', 'videos.views.categories' name='categories'),
    
    # url(r'^$', 'emp.views.home', name='home'),
    # url(r'^emp/', include('emp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
