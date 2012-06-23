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
"""
def convert_uploaded_video(filename, ):
	filename_slug = filename.split('.')[0]
	filepath    = MEDIA_ROOT + '/videos/src/' + filename
	destpath	= MEDIA_ROOT + '/videos/flv/' + filename_slug + '.flv'
	# convert file to .flv using ffmpeg
	# store in media/videos/
	ffmpeg_call = "ffmpeg -i "+ filepath +" -ar 22050 -ab 96k -r 24 -b 600k -f flv " + destpath
	os.system(ffmpeg_call)



