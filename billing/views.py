from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def stripe_webhook(request):
	# TODO: verify signature and handle events
	return HttpResponse("ok")
