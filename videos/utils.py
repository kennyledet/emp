import os
import subprocess
from   emp.settings  import MEDIA_ROOT
from   videos.models import Video
"""
Utility functions to process and complete initial uploaded Video Model here

Workflow:
	'title','description','categories','tags',nsfw','source_file' have been filled out via submitted form
	upload_datetime is filled out automatically
	The source file is attributed to the 'source_file' field and is uploaded to "videos/src/"
	The source file is passed into convert_uploaded_video() for further processing
"""
def process_uploaded_video(uploaded_video, upload_form):
	# Get some basic file info
	filename = str(uploaded_video.source_file.name)
	filesize = uploaded_video.source_file.size

	# Begin filling out Video model data 
	uploaded_video.converted	 = False
	uploaded_video.rating		 = 0
	uploaded_video.favorites     = 0
	uploaded_video.views		 = 0
	# uploaded_video.uploader 	 =
	# uploaded_video.vidtype	 =

	# Create video title slug for usage in URLs
	title_slug					 = str(uploaded_video.title).lower()
	title_slug 					 = title_slug.replace(' ','-')
	uploaded_video.title_slug    = title_slug

	# Commit Video object to DB
	uploaded_video.save()
	# Commit M2M fields to Video object in DB (django-taggit)
	upload_form.save_m2m()
	# CONVERT VIDEO, pass in Video object for further processing
	convert_uploaded_video(filename, uploaded_video)

"""
Utility functions to pass uploaded video data into ffmpeg/mencoder to be converted, as well as
into the utilities necessary to inject metadata (yamdi, flvtool2) and generate thumbnails (ffmpegthumbnailer?)

Also, update additional Video object model properties down here
"""
def convert_uploaded_video(filename, uploaded_video):
	# Get video id to use for filename
	video_id	= uploaded_video.id
	# Set source and destination paths for ffmpeg (and other tools)
	src_path    = MEDIA_ROOT + '/videos/src/' + filename
	dest_path	= MEDIA_ROOT + '/videos/flv/' + str(video_id) + '.flv'
	# Convert file to .flv using ffmpeg
	ffmpeg_call = "ffmpeg -i "+ src_path +" -ar 22050 -ab 96k -r 24 -b 600k -f flv " + dest_path
	os.system(ffmpeg_call)
	# Delete sauce file
	call = subprocess.call(['rm', str(src_path)])
	# Commit additional data to Video object model in db #
	uploaded_video.length 	      = get_video_length(dest_path)
	uploaded_video.converted_file = dest_path
	uploaded_video.source_file    = ""
	uploaded_video.converted  	  = True
	uploaded_video.save()

"""
Utility function to return the length of a video from ffmpeg output 
In this format: 00:00:00.00  h:m:s.ms
"""
def get_video_length(path):
	proc        = subprocess.Popen("ffmpeg -i "+ path +" 2>&1 | grep Duration | awk '{print $2}' | tr -d ,", shell=True, stdout=subprocess.PIPE)
	proc_output = proc.communicate()
	return proc_output[0]
