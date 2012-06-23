from django.shortcuts       import render_to_response
from django.template 		import RequestContext
from django.http 			import HttpResponse, Http404, HttpResponseRedirect
from videos.models			import Video
from videos.forms 			import VideoForm
from videos.utils 			import *

"""
Video play page(s)
"""
def video(request, vid):
	vid = vid
	return render_to_response('videos/video.html', locals())

"""
Handle video uploads here
Workflow: 
	Process partial video upload form
	Pass into video proc. function as validated, partially complete video upload form 
	  as an uncommitted Model instance to be saved
	Redirect the user to the video upload success page
"""
def video_upload(request):
	csrfContext = RequestContext(request)
	if request.method == 'POST': # if upload form submitted
		upload_form = VideoForm(request.POST, request.FILES) # bind form data for vif form.is_valid():alidation
		if upload_form.is_valid(): # validate
			# save partially complete Video model from form data
			uploaded_video = upload_form.save(commit=False)
			# further process Video to fill in missing data
			process_uploaded_video(uploaded_video)
			return HttpResponseRedirect('/video/upload/success/') # redirect user
	else:
		upload_form = VideoForm()
	return render_to_response('videos/video_upload.html', {'upload_form': upload_form}, csrfContext)

"""
Video results pages
"""
def videos(request):
	return render_to_response('videos/videos.html', locals())

def videos_search(request):
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
