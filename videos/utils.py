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

	# Set source and destination paths for ffmpeg (and other tools) conversion
	src_path    = MEDIA_ROOT + '/videos/src/' + video.src_filename
	dest_path	= MEDIA_ROOT + '/videos/flv/' + str(video_id) + '.flv'

	# Generate video thumbnails from source video (higher quality)
	generate_video_thumbs(src_path, video_id)

	# Get src video codec
	video.src_vidtype = str(get_video_type(src_path))

	# Convert file to .flv using ffmpeg ( very generic for now,should support diff. settings)
	ffmpeg_call = "ffmpeg -i "+ src_path +" -ar 22050 -ab 96k -r 24 -b 600k -f flv " + dest_path
	os.system(ffmpeg_call)

	# Delete sauce file
	call = subprocess.call(['rm', str(src_path)])

	# Commit additional data of processed video to db #
	video.length 	      = get_video_length(dest_path)
	video.vidtype         = str(get_video_type(dest_path,))
	video.converted_file  = dest_path
	# video.src_file        = ""
	video.converted       = True
	video.save()

"""
Utility function to return the length of a video from ffmpeg output 
In this format: 00:00:00.00  h:m:s.ms
"""
def get_video_length(path):
	proc        = subprocess.Popen("ffmpeg -i "+ path +" 2>&1 | grep Duration | awk '{print $2}' | tr -d ,", shell=True, stdout=subprocess.PIPE)
	proc_output = proc.communicate()
	return proc_output[0]

def get_total_seconds(path):
	length = get_video_length(path)
	length_list = length.split(':')

	hours   = length_list[0]
	minutes = length_list[1]
	seconds = length_list[2].split('.')[0]

	seconds_in_hours   = int(hours) * 60 * 60
	seconds_in_minutes = int(minutes) * 60
	total_seconds = seconds_in_hours + seconds_in_minutes + int(seconds)

	return total_seconds

"""
Utility function to return the codec of a video from ffprobe json output
Utilize this in ProcessVideoTask to determine codec of src file for:
	1. validation
	2. deciding which conversion function to use (diff. srcfiles may have diff. reqs.)
"""
def get_video_type(path):

	proc = subprocess.Popen("ffprobe -show_format -show_streams -loglevel quiet -print_format json " + path, shell=True, stdout=subprocess.PIPE)
	
	json_source  = proc.communicate()[0]
	json_output  = json.loads(json_source)
	streams      = json_output['streams']

	# figure which stream is video stream
	for stream in streams:
		if stream['codec_type'] == 'video':
			video_stream = stream

	codec = video_stream['codec_name']
	return codec

"""
Utility function to generate video thumbnails and save them to /media/videos/thumbs/*video_id*/
"""
def generate_video_thumbs(path, video_id):
	dest_path	  = MEDIA_ROOT + '/videos/thumbs/'+ str(video_id) +'/'
	create_path(dest_path)

	total_seconds = get_total_seconds(path)
	frame = 1
	if total_seconds < 10:
		step = 1
	else:
		step = total_seconds / 10
		
	for i in range(10):
		os.system("ffmpeg -ss "+ str(frame) +" -i "+ path +" -vframes 1 -f image2 -s 320x240 "+dest_path + str(i)+".jpg")
		frame = frame + step

"""
Utility function to create paths (namely, directories) for use in other functions like generate_video_thumbs()
"""
def create_path(path):
	if not os.path.isdir(path):
		os.makedirs(path)
