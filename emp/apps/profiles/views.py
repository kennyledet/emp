from django.shortcuts       import render_to_response
from django.template 		import RequestContext
from django.http 			import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models 	import User

from emp.apps.profiles.models 			import UserProfile
from emp.apps.videos.models				import VideoPlaylist

def user_profile(request, username):
	user = request.user
	# if the logged in user is the owner of the requested user profile
	if str(user) == username:
		user_owns_profile = True
	else:
		user_owns_profile = False

	# retrieve profile user
	profile_user 	= User.objects.get(username=str(username))
	# retrieve user profile using profile_user object and User.profile attribute
	user_profile 	= profile_user.profile
	# retrieve user profile video favorites (m2m field defined in UserProfile)
	video_favorites = user_profile.video_favorites.all()
	# retrieve user's owned playlists (foreign key field defined in VideoPlaylist)
	video_playlists = profile_user.videoplaylist_set.all()


	# templates/accounts/user_profile.html <- accounts template folder is NOT part of django-registration
	return render_to_response('profiles/user_profile.html', locals())