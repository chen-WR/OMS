from django.shortcuts import redirect

# Access denied if logged in
def checkLogin(func):
	def wrapper(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return func(request, *args, **kwargs)
	return wrapper


def checkSuperuser(func):
	def wrapper(request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('home')
		elif not request.user.is_superuser:
			return redirect("home")
		else:
			return func(request, *args, **kwargs)
	return wrapper