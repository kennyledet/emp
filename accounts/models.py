from django.db import models
# Import User model
from django.contrib.auth.models import User

class UserProfile(models.Model):
	# required for associating with a single user
	user = models.OneToOneField(User)

	website = URLField(blank=True, null=True)
	premium = BooleanField()
	# playlists = ManyToMany
	# video_bookmarks = OneToMany
	# gallery_bookmarks = 
	# image_bookmarks   =


