from django.db import models
# Import User model
from django.contrib.auth.models import User

class UserProfile(models.Model):
	# required for associating with a single user
	user = models.OneToOneField(User)
	join_date = models.DateField(auto_now_add=True)
	birthday  = models.DateField()


	website = models.URLField(blank=True, null=True)
	premium = models.BooleanField()

	profile_pic = models.ImageField(upload_to('profiles/pics/'))



	video_bookmarks = models.ManyToManyField(Video)
	playlists 		= models.ManyToManyField(VideoPlaylist)

	# TODO: Implement these fields when the appropriate models are ready # 
	"""

	gallery_bookmarks = models.ManyToManyField(Gallery)
	image_bookmarks   = models.ManyToManyField(Pic)
	"""