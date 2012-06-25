from django.contrib.auth    import logout
from django.http 			import HttpResponse, Http404, HttpResponseRedirect

def home(request):
	# TODO: A buncha shit
	return HttpResponseRedirect("/videos/")