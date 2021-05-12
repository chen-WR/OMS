from django.http import JsonResponse, Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .decorators import checkLogin, checkSuperuser
from django.templatetags.static import static
from django.conf import settings
from django.views.generic.list import ListView
from .models import User, Product, Cart, Order
import string
import random

def index(request):
	return redirect('/login')

@checkLogin
def logins(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect("/home")
	else:
		form = AuthenticationForm()
	return render(request, 'main/login.html',context = {"form":form})


def logouts(request):
	logout(request)
	return redirect("/")

@login_required(login_url='/')
def home(request):
	return render(request, 'main/home.html', {})

@login_required(login_url='/')
def product(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'main/product.html', context)

@login_required(login_url='/')
def cart(request):
	while True:
		order_id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = 20))	
		if not Order.objects.filter(order_id=order_id).exists():
			break
	if not Order.objects.filter(user=request.user).exists():
		Order.objects.create(user=request.user, order_id=order_id)
	elif not Order.objects.filter(user=request.user).filter(checkout=False).exists():
		Order.objects.create(user=request.user, order_id=order_id)
	order = Order.objects.get(user=request.user, checkout=False)
	carts = order.cart_set.all()
	context = {'carts':carts, 'order':order}
	return render(request, 'main/cart.html', context)

@login_required(login_url='/')
def checkout(request):
	return render(request, 'main/checkout.html', {})