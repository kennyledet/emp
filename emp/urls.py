from django.conf      import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Authentication
    url(r'^user/login/$', 'django.contrib.auth.views.login'),
    url(r'^user/logout/$', 'django.contrib.auth.views.logout', {'next_page':'/videos/'}),

    url(r'^video/(\d.*)/$', 'videos.views.video', name='video'),
    url(r'^videos/$', 		'videos.views.videos', name='videos'),
    url(r'^videos/search/$', 'videos.views.videos_search', name='videos_search'),
    url(r'^video/upload/$', 'videos.views.video_upload', name='video_upload'),
    url(r'^video/upload/success/$', 'videos.views.video_upload_success', name='video_upload_success'),
    #url(r'^videos/categories/$', 'videos.views.categories' name='categories'),
    
    url(r'^$', 'emp.views.home', name='home'),
    # url(r'^emp/', include('emp.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
