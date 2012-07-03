from django.contrib import admin
from videos.models  import Video, Category, VideoPlaylist

class VideoAdmin(admin.ModelAdmin):
	list_display   = ('title', 'uploader', 'upload_datetime', 'length', 'views', 'vidtype', 'src_vidtype')
	list_filter    = ('upload_datetime', 'nsfw', 'vidtype', 'categories')
	search_fields  = ('title', 'categories',) # todo: implement proper tag search

	date_hierarchy = 'upload_datetime'

admin.site.register(Video, VideoAdmin)
admin.site.register(Category)
admin.site.register(VideoPlaylist)