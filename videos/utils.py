import os
import subprocess
import json

from   emp.settings  import MEDIA_ROOT
from   videos.models import Video

"""
Utility functions to pass uploaded video data into ffmpeg/mencoder to be converted, as well as
into the utilities necessary to inject metadata (yamdi, flvtool2) and generate thumbnails (ffmpegthumbnailer?)

Also, update additional Video object model properties down here
Note: Data is safe to pass into cmds, the necessary data validation is handled further back in the stack
"""
def convert_uploaded_video(video_id):
	# Retrieve video from db by id
	video = Video.objects.get(id=video_id)

	# Set source and destination paths for ffmpeg (and other tools)
	src_path    = MEDIA_ROOT + '/videos/src/' + video.src_filename
	dest_path	= MEDIA_ROOT + '/videos/flv/' + str(video_id) + '.flv'
	
	# Get src video codec
	video.src_vidtype = str(get_vid_type(src_path, 'src'))

	# Convert file to .flv using ffmpeg ( very generic for now,should support diff. settings)
	ffmpeg_call = "ffmpeg -i "+ src_path +" -ar 22050 -ab 96k -r 24 -b 600k -f flv " + dest_path
	os.system(ffmpeg_call)

	# Delete sauce file
	call = subprocess.call(['rm', str(src_path)])

	# Commit additional data of processed video to db #
	video.length 	      = get_video_length(dest_path)
	video.vidtype         = str(get_vid_type(dest_path, 'dest'))
	video.converted_file  = dest_path
	# video.src_file        = ""
	video.converted       = True
	video.save()

"""
Utility function to return the length of a video from ffmpeg output 
In this format: 00:00:00.00  h:m:s.ms
TODO: 
	- refactor get_video_length to use Mediainfo
"""
def get_video_length(path):
	proc        = subprocess.Popen("ffmpeg -i "+ path +" 2>&1 | grep Duration | awk '{print $2}' | tr -d ,", shell=True, stdout=subprocess.PIPE)
	proc_output = proc.communicate()
	return proc_output[0]

"""
Utility function to return the codec of a video from ffprobe json output
Utilize this in ProcessVideoTask to determine codec of src file for:
	1. validation
	2. deciding which conversion function to use (diff. srcfiles may have diff. reqs.)
"""
def get_vid_type(path, path_type):
	if path_type == 'src':
		stream_num = 1
	else:
		stream_num = 0
	proc = subprocess.Popen("ffprobe -show_format -show_streams -loglevel quiet -print_format json " + path, shell=True, stdout=subprocess.PIPE)
	json_source = proc.communicate()[0]
	json_output = json.loads(json_source)
	video_stream = json_output['streams'][stream_num]
	codec = video_stream['codec_name']
	return codec
