from django.shortcuts       import render_to_response
from django.template 		import RequestContext
from django.http 			import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models 	import User

from accounts.models 			import UserProfile
from videos.models				import VideoPlaylist

def profile(request, username):
	user = request.user
	# if the logged in user is the owner of the requested profile
	if str(user) == username:
		user_owns_profile = True
	else:
		user_owns_profile = False

	# retrieve profile user
	profile_user 	= User.objects.get(username=str(username))
	# retrieve profile using profile_user object
	profile 		= UserProfile.objects.get(user=profile_user)
	# retrieve profile video bookmarks (m2m field defined in UserProfile)
	video_bookmarks = profile.video_bookmarks.all()
	# retrieve profile playlists (m2m field defined in UserProfile)
	# playlists 		= profile.playlists.all()
	playlists = profile_user.videoplaylist_set.all()

	# templates/accounts/user_profile.html <- accounts template folder is NOT part of django-registration
	return render_to_response('accounts/user_profile.html', locals())