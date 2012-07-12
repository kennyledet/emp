""" Import Django modules """
from django.http 			import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts       import render_to_response
from django.template 		import RequestContext
from django.contrib.auth.decorators import login_required

""" Import Models """
from videos.models 			import Video, VideoPlaylist
from accounts.models 		import UserProfile
from django.contrib.auth.models 	import User

""" Import forms """
from videos.forms 			import VideoForm
""" Import tasks """
from videos.tasks			import ProcessVideoTask


""" Video play page(s) """
def video(request, video_id, video_title_slug=None): # Catch the video id in the URL, as well as the video title slug if entered

	video = Video.objects.get(id=video_id) # retrieve video object by id

	video.views = video.views + 1 # increment video's # of views
	video.save()

	video_tags = video.tags.all() # get video's defined tags
	user = request.user
	if user.is_authenticated(): # if a user is logged in
		user_profile = request.user.profile
		if user_profile.video_favorites.filter(title=video.title): # if user has already favorited this video
			user_favorited = True
		else:
			user_favorited = False
		user_playlists = VideoPlaylist.objects.filter(owner=user) # get user's playlists
	else:
		user_favorited = False

	csrfContext = RequestContext(request) # necessary to make Django's CSRF protection middleware happy
	return render_to_response('videos/video.html', locals(), csrfContext)

""" Handle video uploads here """
@login_required(login_url='/accounts/login/') # a user must be logged in to upload a video
def video_upload(request):
	
	uploader = request.user # get user/uploader

	if request.method == 'POST': # if upload form submitted
		upload_form = VideoForm(request.POST, request.FILES) # bind submitted data to upload form
		if upload_form.is_valid(): # validate
			# Create a partially complete Video object from form data
			video 			 = upload_form.save(commit=False)
			# Set some basic model info
			video.uploader 	 = uploader
			video.views		 = 0

			video.converted	 = False
			# Get some basic file info
			video.src_filename = str(video.src_file.name)
			video.file_size    = video.src_file.size
			video.save()
			# Save m2m fields (necessary for django-taggit)
			upload_form.save_m2m()
			# Pass video id into Celery task ProcessVideoTask for further processing (such as video conversion)
			ProcessVideoTask.delay(video.id)

			return HttpResponseRedirect('/videos/') # should redirect user to video upload success page here
	else:
		upload_form = VideoForm()

	csrfContext = RequestContext(request)
	return render_to_response('videos/video_upload.html', locals(), csrfContext)


def video_upload_success(request):
	return render_to_response('videos/video_upload_success.html')

""" Video listings """
def videos(request):
	videos = Video.objects.all().order_by('-upload_datetime')

	return render_to_response('videos/videos.html', locals())

""" Video search """
def videos_search(request):
	empty_query = False
	if 'q' in request.GET: # if ?q=* is in uri
		query = request.GET['q']
		if not query: # if query string is empty
			empty_query = True
		else:
			videos = Video.objects.filter(title__icontains=query) # get videos from non-case sensitive search on title column
			return render_to_response('videos/search.html', locals())

	# If no query entered or query string is empty, display search form with appropriate error msg
	return render_to_response('videos/search_form.html', locals())


""" Video playlist page view """
def video_playlist(request, playlist_id, playlist_title_slug=None):
	playlist = VideoPlaylist.objects.get(id=playlist_id) # get playlist by id
	playlist_videos = playlist.videos.all() # retrieve list of playlist's videos

	return render_to_response('videos/video_playlist.html', locals())
	

""" AJAXified favoriting view """
def favorite_video(request):
	if request.is_ajax(): # request is sent through favoriteForm submit through jQuery AJAX 
		# video_id - The id of the video to be favorited by the current request.user
		# fav_type - Either 'Add to Favorites' or 'Remove from Favorites', self explanatory
		if request.POST['video_id'] and request.POST['fav_type']:
			video = Video.objects.get(id=request.POST['video_id'])
			user_profile = request.user.profile
			
			# Video either gets added or removed from the UserProfile's video_favorites ManyToMany field
			if request.POST['fav_type'] == 'Add to Favorites':
				user_profile.video_favorites.add(video)
				return HttpResponse('Added') # let AJAX caller know the video was added to favorites
			elif request.POST['fav_type'] == 'Remove from Favorites':
				user_profile.video_favorites.remove(video)
				return HttpResponse('Removed') # let AJAX caller know the video was removed from favorites
	else:
		return HttpResponse('Not Ajax')

""" AJAXified playlist adding/removing video view """
def add_to_playlist(request):
	if request.is_ajax():
		if request.POST['video_id'] and request.POST['playlist_id']:
			video = Video.objects.get(id=request.POST['video_id']) # get video to add, by id
			playlist = VideoPlaylist.objects.get(id=request.POST['playlist_id']) # get playlist to add video to
			
			if video in playlist.videos.all(): # if the video is already in the playlist
				return HttpResponse("Exists")  # let AJAX caller know it exists
			else:
				playlist.videos.add(video) 	   # if the video was successfully added to the playlist
				return HttpResponse('Added')   # let AJAX caller know it was added
	else:
		return HttpResponse('Not AJAX')


