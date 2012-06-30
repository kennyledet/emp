import os
from django.db import models
# Import User model
from django.contrib.auth.models import User
# Import django-taggit manager
from taggit.managers import TaggableManager
# Import MEDIA_ROOT
from emp.settings    import MEDIA_ROOT


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
	favoriters	= models.ManyToManyField(User, related_name='+', blank=True, editable=False)
	favorites   = models.IntegerField()
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

	def _get_thumbs(self):
		thumbs_path = MEDIA_ROOT + '/videos/thumbs/'+ str(self.id) +'/'
		thumbs_list = os.listdir(thumbs_path)
		if '.DS_Store' in thumbs_list:
			thumbs_list.remove('.DS_Store')
		return thumbs_list

	thumbs_list = property(_get_thumbs)


class VideoPlaylist(models.Model):
	videos = models.ManyToManyField(Video)

	created_datetime  = models.DateTimeField(auto_now_add=True)
	modified_datetime = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(User, related_name='+')
	# Come up with a better name for this field!
	added_by = models.ManyToManyField(User, related_name='++')












"""
class HTML5Profiles(models.Model):
	title  = models.CharField(max_length=255)
	vcodec = models.CharField(max_length=255)
"""
	