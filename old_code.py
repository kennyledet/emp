# Old favorite/remove from favorites method using GET with no AJAX
	"""
	if 'f' in request.GET:
		video_id = request.GET['f']
		if video_id:
			# if favorite query string isn't empty, add it to user's favorites
			video = Video.objects.get(id=video_id)

			user_profile = request.user.profile
			user_profile.video_favorites.add(video)

			return HttpResponseRedirect(request.META['HTTP_REFERER'])
		else:
			return HttpResponseRedirect(request.META['HTTP_REFERER'])
	elif 'fr' in request.GET:
		video_id = request.GET['fr']
		if video_id:
			# if favorite remove query string isn't empty, remove it from user's favorites
			video = Video.objects.get(id=video_id)

			user_profile = request.user.profile
			user_profile.video_favorites.remove(video)
			
			return HttpResponseRedirect(request.META['HTTP_REFERER'])
	else:
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	"""


# Removed from videos.utils , refactored as Video model method/prop
"""
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