from django.shortcuts       import render_to_response
from django.template 		import RequestContext
from django.http 			import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from videos.models			import Video
from videos.forms 			import VideoForm
from videos.tasks			import ProcessVideoTask
"""
Video play page(s)
Workflow:
	Catch the video id in the URL, as well as the video title slug if it exists in the URL
	  (video title slug in the URL is not required by default and is allowed for convenience for 
	  	implementing SEO URLs in the future using these slugs!)
	Use this video ID to get single video object from the database

	Pass video object data to videos/video.html template
"""
def video(request, video_id, video_title_slug=None):
	user = request.user
	video_id = video_id
	video    = Video.objects.get(id=video_id)

	return render_to_response('videos/video.html', locals())

"""
Handle video uploads here
Workflow: 
	User must be logged in
	Process video upload form
	Pass into videos.tasks.ProcessVideoTask Celery task
	Redirect the user to the video upload success page
"""
@login_required(login_url='/accounts/login/')
def video_upload(request):
	csrfContext = RequestContext(request)
	# get user/uploader
	uploader = request.user
	if request.method == 'POST': # if upload form submitted
		# bind submitted data to upload form
		upload_form = VideoForm(request.POST, request.FILES)
		if upload_form.is_valid(): # validate
			# Create a partially complete Video object from form data
			video 			 = upload_form.save(commit=False)
			video.uploader 	 = uploader
			video.converted	 = False
			video.rating	 = 0
			video.favorites  = 0
			video.views		 = 0
			title_slug		 = str(video.title).lower()
		 	title_slug 		 = title_slug.replace(' ','-')
			video.title_slug = title_slug
			# Get some basic file info
			video.src_filename = str(video.src_file.name)
			video.file_size    = video.src_file.size
			video.save()
			# Get id from newly created record for passing into ProcessVideoTask
			video_id = video.id
			# Save m2m fields (necessary for django-taggit)
			upload_form.save_m2m()
			# ProcessVideoTask (CELERY) pass in filename and video id
			ProcessVideoTask.delay(video_id)
			return HttpResponseRedirect('/videos/') # redirect user
	else:
		upload_form = VideoForm()
	return render_to_response('videos/video_upload.html', {'upload_form': upload_form}, csrfContext)

def video_upload_success(request):
	user = request.user
	return render_to_response('videos/video_upload_success.html')


"""
Video results pages
TODO:
	Implement pagination
"""
def videos(request):
	user = request.user
	videos = Video.objects.all().order_by('-upload_datetime')
	return render_to_response('videos/videos.html', locals())


def videos_search(request):
	empty_query = False
	# if ?q=* is in uri
	if 'q' in request.GET:
		query = request.GET['q']
		# if query string is empty
		if not query:
			empty_query = True
		else:
		# perform non-case sensitive search on title column
		# get rows of videos as list of Video objects
			videos = Video.objects.filter(title__icontains=query)
			return render_to_response('videos/search.html', locals())
	# if no query entered or query string is empty, display form
	# if empty_query = True (query string empty) , display error msg
	return render_to_response('videos/search_form.html', locals())
