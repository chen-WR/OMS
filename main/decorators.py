from django.shortcuts import redirect
from .models import Order

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

def checkCart(func):
	def wrapper(request, *args, **kwargs):
		order, create = Order.objects.get_or_create(user=request.user, checkout=False)
		if order.getCartTotal == 0:
			return redirect('cart')
		else:
			return func(request, *args, **kwargs)
	return wrapper

def checkEdit(func):
	def wrapper(request, *args, **kwargs):
		if request.user.is_authenticated and request.user.allow_edit:
			return func(request, *args, **kwargs)
		else:
			return redirect('home')
	return wrapper