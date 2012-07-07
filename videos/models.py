import os
from django.db import models
# Import User model
from django.contrib.auth.models import User
# Import django-taggit manager
from taggit.managers import TaggableManager
# Import MEDIA_ROOT
from emp.settings    import MEDIA_ROOT
# Import UserProfile model for some class methods


class Category(models.Model):
	category_title = models.CharField(max_length=255)
	nsfw		   = models.BooleanField(blank=True)

	def __unicode__(self):
		return self.category_title

# TODO: Add model method to calculate hours, minutes, seconds from length 00:00:00.00

class Video(models.Model):
	title 		= models.CharField(max_length=255)
	title_slug  = models.CharField(max_length=255)
	uploader 	= models.ForeignKey(User, editable=False)
	upload_datetime   = models.DateTimeField(auto_now_add=True)
	modified_datetime = models.DateTimeField(auto_now=True)
	length  	= models.CharField(max_length=255, blank=True, editable=False)
	description = models.TextField()
	converted   = models.BooleanField(editable=False)

	rating_choices = ((u'1',u'1'),(u'2',u'2'),(u'3',u'3'),(u'4',u'4'),(u'5',u'5'),(u'0',u'0'))
	rating		= models.IntegerField(choices=rating_choices)
	categories  = models.ManyToManyField(Category)
	tags 		= TaggableManager(blank=True)

	nsfw		= models.BooleanField()
	views 		= models.IntegerField()

	vidtype		= models.CharField(max_length=255, editable=False)
	src_vidtype = models.CharField(max_length=255, editable=False)
	file_size       = models.IntegerField(blank=True, null=True, editable=False)
	src_file        = models.FileField(upload_to="videos/src/")
	src_filename    = models.CharField(max_length=255, editable=False)

	converted_file  = models.CharField(max_length=255, blank=True, null=True, editable=False)

	def __unicode__(self):
		return self.title

	# get list of thumbnail filenames for video
	def _get_thumbs(self):
		thumbs_path = MEDIA_ROOT + '/videos/thumbs/'+ str(self.id) +'/'
		thumbs_list = os.listdir(thumbs_path)
		if '.DS_Store' in thumbs_list:
			thumbs_list.remove('.DS_Store')
		return thumbs_list

	thumbs_list = property(_get_thumbs)

	# get number of favorites (via the # of user profiles which have the video favorited (m2m relation))
	def _get_num_favorites(self):
		favoriters = self.userprofile_set.all()
		return len(favoriters)

	num_favorites = property(_get_num_favorites)

"""
Each video playlist is owned by a single user who created it.
It may be added to a different user's lists of playlists, however:
Each playlist is immutable, and as such a user may only edit (delete/add videos) a playlist
by importing a copy of it, therefore becoming the new owner of that particular instance of the playlist
TODO: To make the above happen, either have the clone/import happen as soon as the user adds the playlist, 
	  OR have it happen the first time a user tries to edit that playlist
"""
class VideoPlaylist(models.Model):
	title  = models.CharField(max_length=255)
	videos = models.ManyToManyField(Video)

	created_datetime  = models.DateTimeField(auto_now_add=True)
	modified_datetime = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(User)
	

	##added_by = models.ManyToManyField(UserProfile, related_name='++')

	def __unicode__(self):
		return self.title














"""
class HTML5Profiles(models.Model):
	title  = models.CharField(max_length=255)
	vcodec = models.CharField(max_length=255)
"""
	