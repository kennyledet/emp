from django.shortcuts       import render_to_response
from django.template        import RequestContext
from django.http            import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User

from emp.apps.channels.models           import UserChannel
from emp.apps.videos.models             import VideoPlaylist

def user_channel(request, username):

    # retrieve profile user
    channel_user    = User.objects.get(username=str(username))
    # retrieve user profile using profile_user object and User.profile attribute
    user_channel    = channel_user.channel
    # retrieve user profile video favorites (m2m field defined in UserChannel)
    video_favorites = user_channel.video_favorites.all()
    # retrieve user's owned playlists (foreign key field defined in VideoPlaylist)
    video_playlists = channel_user.videoplaylist_set.all()


    # templates/accounts/user_profile.html <- accounts template folder is NOT part of django-registration
    return render_to_response('channels/user_channel.html', locals())