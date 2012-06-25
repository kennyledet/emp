import os
import subprocess
from   emp.settings  import MEDIA_ROOT
from   videos.models import Video
"""
Utility functions to pass uploaded video data into ffmpeg/mencoder to be converted, as well as
into the utilities necessary to inject metadata (yamdi, flvtool2) and generate thumbnails (ffmpegthumbnailer?)

Also, update additional Video object model properties down here
"""
def convert_uploaded_video(filename):
	## TODO: add suppt. for HTML5 video formats 
	# Get video id to use for filename
	video_id	= 'test'
	# Set source and destination paths for ffmpeg (and other tools)
	src_path    = MEDIA_ROOT + '/videos/src/' + filename
	dest_path	= MEDIA_ROOT + '/videos/flv/' + str(video_id) + '.flv'
	# Convert file to .flv using ffmpeg ( very generic for now,should support diff. settings)
	ffmpeg_call = "ffmpeg -i "+ src_path +" -ar 22050 -ab 96k -r 24 -b 600k -f flv " + dest_path
	os.system(ffmpeg_call)
	# Delete sauce file
	call = subprocess.call(['rm', str(src_path)])
	# Commit additional data to Video object model in db #
	"""
	uploaded_video.length 	      = get_video_length(dest_path)
	uploaded_video.converted_file = dest_path
	uploaded_video.source_file    = ""
	uploaded_video.converted  	  = True
	uploaded_video.save()
	"""

"""
Utility function to return the length of a video from ffmpeg output 
In this format: 00:00:00.00  h:m:s.ms
"""
def get_video_length(path):
	proc        = subprocess.Popen("ffmpeg -i "+ path +" 2>&1 | grep Duration | awk '{print $2}' | tr -d ,", shell=True, stdout=subprocess.PIPE)
	proc_output = proc.communicate()
	return proc_output[0]
