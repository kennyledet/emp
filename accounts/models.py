from django.db import models
# Import User model
from django.contrib.auth.models import User
# Import Video and VideoPlaylist
from videos.models 				import Video, VideoPlaylist

""" UserProfile model holds additional user data outside of default Django authentication fields and some ForeignKeys (video->uploader)
Such as: birthdate, video favorites, video playlists, image favorites """

class UserProfile(models.Model):
	user = models.OneToOneField(User) # required for associating with a single user
	profile_pic = models.FileField(upload_to='profiles/pics/', blank=True, null=True)

	birthday  = models.DateField(blank=True, null=True)
	website = models.URLField(blank=True)
	premium = models.BooleanField()

	video_favorites = models.ManyToManyField(Video, blank=True, null=True)
	video_playlists = models.ManyToManyField(VideoPlaylist, blank=True, null=True)

	# location = 
	# gender   =

	def __unicode__(self):
		return u'%s' % (str(self.user),)

	# TODO: Implement these fields when the appropriate models are ready # 
	# gallery_favorites = models.ManyToManyField(Gallery)
	# image_favorites   = models.ManyToManyField(Pic)

""" This either gets a UserProfile or creates a UserProfile automatically 
based on whether or not the UserProfile already exists """
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
