from django.forms import ModelForm
from videos.models import Video
# inherit from ModelForm to mimic Video Model fields and reduce redundancy
class VideoForm(ModelForm):
	class Meta:
		model = Video
		# pass in tuple of fields to display in upload form
		fields = ('title','description','categories','tags','nsfw','src_file')
