from django.db import models
# Import User model
from django.contrib.auth.models import User
# Import django-taggit manager
from taggit.managers import TaggableManager


class Category(models.Model):
	category_title = models.CharField(max_length=255)
	nsfw		   = models.BooleanField(blank=True)

	def __unicode__(self):
		return self.category_title

class Video(models.Model):
	title 		= models.CharField(max_length=255)
	title_slug  = models.CharField(max_length=255)
	uploader 	= models.ForeignKey(User, blank=True, null=True, editable=False) # set blank,null = True temporarily
	upload_datetime   = models.DateTimeField(auto_now_add=True)
	modified_datetime = models.DateTimeField(auto_now=True)
	length  	= models.CharField(max_length=255, blank=True, editable=False)
	description = models.TextField(blank=True, null=True)
	converted   = models.BooleanField(editable=False)

	rating_choices = ((u'1',u'1'),(u'2',u'2'),(u'3',u'3'),(u'4',u'4'),(u'5',u'5'),(u'0',u'0'))
	rating		= models.IntegerField(choices=rating_choices)

	vidtype		= models.CharField(max_length=10, blank=True, editable=False)
	categories  = models.ManyToManyField(Category)
	tags 		= TaggableManager(blank=True)
	favoriters	= models.ManyToManyField(User, related_name='+', blank=True, editable=False)
	favorites   = models.IntegerField(blank=True, null=True)
	nsfw		= models.BooleanField()
	views 		= models.IntegerField()

	source_file = models.FileField(upload_to="videos/src/")
	converted_file = models.CharField(max_length=255, blank=True, null=True, editable=False)

	def __unicode__(self):
		return self.title
