""" Import Django modules """
from django.db import models
""" Import models """
from django.contrib.auth.models import User
from emp.apps.videos.models import Video, VideoPlaylist

class UserChannel(models.Model):
    user = models.OneToOneField(User) # required for associating with a single user
    profile_pic = models.FileField(upload_to='/channels/avatars/', blank=True, null=True)

    birthday  = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True)
    premium = models.BooleanField()

    video_favorites = models.ManyToManyField(Video, blank=True, null=True)

    # location = 
    # gender   =

    def __unicode__(self):
        return u'%s' % (str(self.user),)

    # TODO: Implement these fields when the appropriate models are ready # 
    # gallery_favorites = models.ManyToManyField(Gallery)
    # image_favorites   = models.ManyToManyField(Pic)

""" This either gets a UserChannel or creates a UserChannel automatically 
based on whether or not the UserChannel already exists """
User.channel = property(lambda u: UserChannel.objects.get_or_create(user=u)[0])
