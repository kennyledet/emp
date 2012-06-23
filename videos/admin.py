from django.contrib import admin
from videos.models  import Video, Category

class VideoAdmin(admin.ModelAdmin):
	list_display   = ('title', 'uploader', 'upload_datetime', 'length', 'favorites', 'views')
	list_filter    = ('upload_datetime', 'nsfw', 'vidtype', 'categories')
	search_fields  = ('title', 'categories') # add tags here

	date_hierarchy = 'upload_datetime'


admin.site.register(Video, VideoAdmin)
admin.site.register(Category)