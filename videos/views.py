from django.shortcuts       import render_to_response
from django.template 		import RequestContext
from django.http 			import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from videos.models			import Video
from videos.forms 			import VideoForm
from videos.utils 			import *
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
	Process partial video upload form
	Pass into video proc. function as validated, partially complete video upload form 
	  as an uncommitted Model instance to be saved
	Redirect the user to the video upload success page
"""
@login_required(login_url='/user/login/')
def video_upload(request):
	csrfContext = RequestContext(request)
	# get user
	user = request.user
	if request.method == 'POST': # if upload form submitted
		upload_form = VideoForm(request.POST, request.FILES) # bind form data for vif form.is_valid():alidation
		if upload_form.is_valid(): # validate
			# save partially complete Video model from form data
			uploaded_video = upload_form.save(commit=False)
			uploaded_video.uploader 	 = user
			uploaded_video.converted	 = False
			uploaded_video.rating		 = 0
			uploaded_video.favorites     = 0
			uploaded_video.views		 = 0
			title_slug					 = str(uploaded_video.title).lower()
		 	title_slug 					 = title_slug.replace(' ','-')
			uploaded_video.title_slug    = title_slug
			# Get some basic file info
			filename = str(uploaded_video.source_file.name)
			# filesize = uploaded_video.source_file.size
			uploaded_video.save()
			# further process Video to fill in missing data / + upload_form to save m2m (django-taggit)
			upload_form.save_m2m()
			# process_uploaded_video(uploaded_video, upload_form)
			ProcessVideoTask.delay(filename)
			return HttpResponseRedirect('/video/upload/success/') # redirect user
	else:
		upload_form = VideoForm()
	return render_to_response('videos/video_upload.html', {'upload_form': upload_form}, csrfContext)

def video_upload_success(request):
	user = request.user
	return render_to_response('videos/video_upload_success.html')


"""
Video results pages
"""
def videos(request):
	user = request.user
	return render_to_response('videos/videos.html', locals())

def videos_search(request):
	user = request.user
	query_empty = False
	no_query    = False
	if request.GET['query']:
		query = request.GET['query']
		if not query:
			query_empty = True
		else:
			videos = Video.objects.filter(title__icontains=query).order_by(('-upload_time',))
			return render_to_response('videos/videos_search_results.html', locals())
	else:
		no_query = True
	return render_to_response('videos/videos_search_results.html', locals())
