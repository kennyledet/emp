from django.conf      import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', 'emp.views.home', name='home'),

    # videos app
    url(r'^videos/', include('videos.urls')),
    # accounts app - holds UserProfile model and user profile views
    url(r'^profiles/', include('accounts.urls')),

    # django admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # allow django server to serve media (for dev environment)
