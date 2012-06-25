from celery.task     import Task
from celery.registry import tasks
from videos.utils    import convert_uploaded_video
"""
Task to be ran from the video_upload view to process video upload 
"""
class ProcessVideoTask(Task):
	def run(self, video_id, **kwargs):
		# CONVERT VIDEO, pass in Video object for further processing
		convert_uploaded_video(video_id)

	

tasks.register(ProcessVideoTask)
