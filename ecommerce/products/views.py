from django.shortcuts import render

# Create your views here.

def home(request):
	if request.user.is_authenticated():
		username = "Eli"
		context = {'username_is':request.user}

	else:
			context = {"username_is":"AnonymousUser"}

	template = 'home.html'
	
	return render(request, template, context)