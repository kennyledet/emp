import os, subprocess, json, re
import magic # python-magic, wrapper around libmagic to check file types
from   emp.settings  import MEDIA_ROOT
from   emp.apps.videos.models import Video

""" Utility functions to pass uploaded video data into ffmpeg/mencoder to be converted, as well as
into the utilities necessary to inject metadata (yamdi, flvtool2) and generate thumbnails

Also, update additional Video object model properties down here
Note: Data is only considered safe to pass into cmds when the necessary data validation is done via validates_as_video() """

""" Convert an uploaded video """
def convert_uploaded_video(video_id):
	video = Video.objects.get(id=video_id) # Retrieve video from db by id

	# Set source and destination paths for ffmpeg (and other tools) conversion
	src_path    = MEDIA_ROOT + '/videos/src/' + video.src_filename
	dest_path	= MEDIA_ROOT + '/videos/flv/' + str(video_id) + '.flv'

	if validates_as_video(src_path): # VALIDATE FILE UPLOAD AS VIDEO BEFORE PASSING INTO ANY SHELL CALLS

		video.length = get_video_length(src_path) # Get video length

		generate_video_thumbs(src_path, video) # Generate video thumbnails from source video (higher quality)
		video.src_vidtype = str(get_video_type(src_path)) # Get src video codec

		# Convert file to .flv using ffmpeg ( very generic for now, should support diff. settings )
		ffmpeg_call = "ffmpeg -i "+ src_path +" -ar 22050 -ab 96k -r 24 -b 600k -f flv " + dest_path
		os.system(ffmpeg_call)

		# Get and commit additional data of processed video to db #
		video.vidtype         = str(get_video_type(dest_path))
		video.converted_file  = dest_path
		video.converted       = True

		video.save()
	else: # if validation fails, no need for a non-video to even be a record in the videos database! Remove it.
		video.delete()
	
	call = subprocess.call(['rm', str(src_path)]) # Clean up, remove source file regardless of validation

""" Return the length of a video from ffmpeg output in this format: 00:00:00.00  h:m:s.ms """
def get_video_length(path):
	proc        = subprocess.Popen("ffmpeg -i "+ path +" 2>&1 | grep Duration | awk '{print $2}' | tr -d ,", shell=True, stdout=subprocess.PIPE)
	proc_output = proc.communicate()
	return proc_output[0]

""" Return the codec of a video from ffprobe json output
Utilize this in the future to determine codec of src file for 
deciding which conversion function to use (diff. srcfiles may have diff. reqs.) """
def get_video_type(path):

	proc = subprocess.Popen("ffprobe -show_format -show_streams -loglevel quiet -print_format json " + path, shell=True, stdout=subprocess.PIPE)
	
	json_source  = proc.communicate()[0]
	json_output  = json.loads(json_source)
	streams      = json_output['streams']

	# Figure which stream is video stream
	for stream in streams:
		if stream['codec_type'] == 'video':
			video_stream = stream

	codec = video_stream['codec_name']
	return codec

""" Generate video thumbnails and save them to /media/videos/thumbs/*video_id*/ """
# the # of thumbnails generated will either be equal to the default num_thumbs variable, 
# OR be equal to the approximate length of the video, in seconds 
# IF the # of thumbnails specified is indeed greater than the length of the video, in seconds.
def generate_video_thumbs(path, video):
	num_thumbs = 10
	dest_path	  = MEDIA_ROOT + '/videos/thumbs/'+ str(video.id) +'/'
	create_path(dest_path)

	total_seconds = video.total_seconds
	frame = 1

	if total_seconds < num_thumbs:
		step = 1
		num_thumbs = total_seconds+1
	else:
		step = total_seconds / num_thumbs
		
	for i in range(num_thumbs):
		os.system("ffmpeg -ss "+ str(frame) +" -i "+ path +" -vframes 1 -f image2 -s 125x125 "+dest_path + str(i)+".jpg")
		frame = frame + step

""" Create paths (namely, directories) for use in other functions like generate_video_thumbs() """
def create_path(path):
	if not os.path.isdir(path):
		os.makedirs(path)

""" Validate whether or not a file is a video, based on the file's mimetype (using python-magic) """
def validates_as_video(path):
	mime 	 = magic.Magic(mime=True)
	mimetype = mime.from_file(path)
	result   = re.match("^video/.*", mime.from_file(path)) 	# check if mimetype matches regexp

	if result:
		return True
	else:
		return False