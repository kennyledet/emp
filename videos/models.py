""" Import Python modules """
import os
""" Import Django modules """
from django.db 		 import models
""" Import Django settings """
from emp.settings    import MEDIA_ROOT
""" Import Models """
from django.contrib.auth.models import User
""" Import from 3rd party Django modules """
from taggit.managers 	  import TaggableManager # django-taggit taggable manager
from djangoratings.fields import RatingField 	 # django-ratings field type


class Category(models.Model):
	category_title = models.CharField(max_length=255)
	nsfw		   = models.BooleanField(blank=True)

	def __unicode__(self):
		return self.category_title

class Video(models.Model):
	title 		= models.CharField(max_length=255)
	uploader 	= models.ForeignKey(User, editable=False)
	upload_datetime   = models.DateTimeField(auto_now_add=True)
	modified_datetime = models.DateTimeField(auto_now=True)
	length  	= models.CharField(max_length=255, blank=True, editable=False)
	description = models.TextField()
	converted   = models.BooleanField(editable=False)
	views 		= models.IntegerField(editable=True)

	categories  = models.ManyToManyField(Category)
	tags 		= TaggableManager(blank=True) # django-taggit handles tagging
	rating 		= RatingField(range=5) # 5 possible rating choices
	nsfw		= models.BooleanField() # (Not Safe for Work)

	vidtype		= models.CharField(max_length=255, editable=False)
	src_vidtype = models.CharField(max_length=255, editable=False)
	file_size       = models.IntegerField(blank=True, null=True, editable=False)
	src_file        = models.FileField(upload_to="videos/src/")
	src_filename    = models.CharField(max_length=255, editable=False)

	converted_file  = models.CharField(max_length=255, blank=True, null=True, editable=False)

	def __unicode__(self):
		return self.title

	""" Get list of thumbnail filenames for video """
	def _get_thumbs(self):
		thumbs_path = MEDIA_ROOT + '/videos/thumbs/'+ str(self.id) +'/'
		thumbs_list = os.listdir(thumbs_path)
		if '.DS_Store' in thumbs_list:
			thumbs_list.remove('.DS_Store')
		return thumbs_list

	thumbs_list = property(_get_thumbs)

	""" Get number of favorites (via the # of user profiles which have the video favorited (m2m relation)) """
	def _get_num_favorites(self):
		favoriters = self.userprofile_set.all()
		return len(favoriters)

	num_favorites = property(_get_num_favorites)

	""" Generate a video title slug based on the video title for use in URLS """
	def _get_video_title_slug(self):
		title_slug		 = str(self.title).lower()
		title_slug 		 = title_slug.replace(' ','-')
		return title_slug

	title_slug = property(_get_video_title_slug)

	""" Get hours, minutes, seconds from length field, as a list of integers """
	def _get_length_list(self):
		init_length_list = self.length.split(':')
		hours   = int(init_length_list[0])
		minutes = int(init_length_list[1])
		seconds = int(init_length_list[2].split('.')[0])
		length_list = [hours, minutes, seconds]
		return length_list

	length_list = property(_get_length_list)

	""" Get total seconds (useful when need to order by total length) """
	def _get_total_seconds(self):
		hours   = self.length_list[0]
		minutes = self.length_list[1]
		seconds = self.length_list[2]

		seconds_in_hours   = hours * 60 * 60
		seconds_in_minutes = minutes * 60
		total_seconds = seconds_in_hours + seconds_in_minutes + seconds
		return total_seconds

	total_seconds = property(_get_total_seconds)

""" Each video playlist is owned by a single user who created it.
It may be added to a different user's lists of playlists, however:
Each playlist is immutable, and as such a user may only edit (delete/add videos) a playlist
by importing a copy of it, therefore becoming the new owner of that particular instance of the playlist
TODO: To make the above happen, either have the clone/import happen as soon as the user adds the playlist, 
	  OR have it happen the first time a user tries to edit that playlist """
class VideoPlaylist(models.Model):
	title  = models.CharField(max_length=255)
	videos = models.ManyToManyField(Video)

	created_datetime  = models.DateTimeField(auto_now_add=True)
	modified_datetime = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(User)

	def __unicode__(self):
		return self.title














"""
class HTML5Profiles(models.Model):
	title  = models.CharField(max_length=255)
	vcodec = models.CharField(max_length=255)
"""
	