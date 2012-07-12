from django.forms import ModelForm
from videos.models import Video, VideoPlaylist

""" Form for creating new Video (upload) """
class VideoForm(ModelForm):
	class Meta:
		model = Video
		# fields to display in upload form
		fields = ('title','description','categories','tags','src_file')

""" Form for creating new VideoPlaylist """
class VideoPlaylistForm(ModelForm):
	class Meta:
		model = VideoPlaylist
		fields = ('title',) # maybe allow playlists to relate to categories?
