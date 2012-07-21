from celery.task     import Task
from celery.registry import tasks
from emp.apps.videos.utils    import convert_uploaded_video

""" Task to be started from videos.views.video_upload to process uploaded video
Process contained in videos.utils """
class ProcessVideoTask(Task):
	def run(self, video_id, **kwargs):
		convert_uploaded_video(video_id) # convert video, pass in Video id for further processing

tasks.register(ProcessVideoTask)
