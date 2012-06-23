import os
# import MEDIA_ROOT folder to store videos in
from   emp.settings import MEDIA_ROOT
# import Video model
from   videos.models import Video
"""
Utility functions to process and complete initial uploaded Video Model here

Workflow:
	'title','description','categories','nsfw','source_file' have been filled out via submitted form
	upload_datetime is filled out automatically
	The uploaded file is attributed to the 'source_file' field and is uploaded to "videos/src/"
"""
def process_uploaded_video(uploaded_video):
	filename = str(uploaded_video.source_file.name)
	filesize = uploaded_video.source_file.size
	## TODO: Fill in methods to commit complete Video Model instance
	# uploaded_video.uploader 	 =
	# uploaded_video.length 	 = 
	uploaded_video.converted	 = False
	uploaded_video.rating		 = 0
	# uploaded_video.vidtype	 =
	uploaded_video.favorites     = 0
	uploaded_video.views		 = 0
	# Commit Video object to DB
	uploaded_video.save()

	# CONVERT VIDEO, pass in Video object for further processing
	convert_uploaded_video(filename, uploaded_video)

"""
Utility functions to pass uploaded video data into ffmpeg/mencoder to be converted, as well as
into the utilities necessary to inject metadata (yamdi, flvtool2) and generate thumbnails (ffmpegthumbnailer?)

Also, update additional Video object model down here

TODO: 
	Implement FFMPEG/mencoder, flvtool2, and perhaps Celery for process handling
	Exiftool: extracts metadata from audio/video/image files, gets codec info
	Source file is deleted by default as of now: allow settings to require otherwise,
		which will prove useful when the HTML5 functionality is added and multiple
		output formats will be used
"""
def convert_uploaded_video(filename, uploaded_video):
	video_id	  = uploaded_video.id
	# filename_slug = filename.split('.')[0]

	src_path    = MEDIA_ROOT + '/videos/src/' + filename
	dest_path	= MEDIA_ROOT + '/videos/flv/' + str(video_id) + '.flv'

	# convert file to .flv using ffmpeg
	# store in media/videos/
	ffmpeg_call = "ffmpeg -i "+ src_path +" -ar 22050 -ab 96k -r 24 -b 600k -f flv " + dest_path
	os.system(ffmpeg_call)

	# Delete sauce file
	os.system("rm " + src_path)

	# Commit data to Video object model in db #
	uploaded_video.converted_file = dest_path
	# Add functionality to allow for admins to re-upload source files and re-convert
	uploaded_video.source_file    = ""
	uploaded_video.converted  	  = True
	uploaded_video.save()

	# uploaded_video.filename_slug  = filename_slug




