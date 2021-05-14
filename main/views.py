from django.http import JsonResponse, Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .decorators import checkLogin, checkSuperuser
from django.templatetags.static import static
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from .models import User, Product, Cart, Order, Secret
from .forms import CheckoutForm, RegisterForm
from .updateDB import updateData
import string
import json
import random

def index(request):
	# Currently Not needed
	# updateData()
	return redirect('logins')

@checkLogin
def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			return redirect('home')
		else:				
			errors = form.errors.get_json_data()
			for error in errors:
				message = errors[error][0]['message'] 
				messages.error(request, message)
	form = RegisterForm() 
	return render(request, 'main/register.html', {'form': form })

@checkLogin
def logins(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect("home")
		else:
			messages.error(request, "Incorrect Username or Password")
	form = AuthenticationForm()
	return render(request, 'main/login.html',context = {"form":form})

def logouts(request):
	logout(request)
	return redirect("index")

@login_required(login_url='index')
def home(request):
	if request.user.is_superuser:
		orders = Order.objects.filter(checkout=True)
	else:
		orders = Order.objects.filter(user=request.user, checkout=True)
	context = {'orders': orders}
	return render(request, 'main/home.html', context)

@login_required(login_url='index')
def product(request):
	order, create = Order.objects.get_or_create(user=request.user, checkout=False)
	carts = order.cart_set.all()
	products = Product.objects.all()
	context = {'products':products, 'carts':carts}
	return render(request, 'main/product.html', context)

@login_required(login_url='index')
def cart(request):
	order, create = Order.objects.get_or_create(user=request.user, checkout=False)
	carts = order.cart_set.all()
	context = {'carts':carts, 'order':order}
	return render(request, 'main/cart.html', context)

@login_required(login_url='index')
def checkout(request):
	if request.method == "POST":
		form = CheckoutForm(request.POST)
		if form.is_valid():
			confirmation_number = getConfirmationNumber()
			order = Order.objects.get(user=request.user, checkout=False)
			order.checkout = True
			order.confirmation_number = confirmation_number
			order.date = timezone.now()
			order.save()
			return HttpResponseRedirect(f'/ordered/{confirmation_number}')
	order, create = Order.objects.get_or_create(user=request.user, checkout=False)
	carts = order.cart_set.all()
	form = CheckoutForm() 
	context = {'carts':carts, 'order':order, 'form':form}
	return render(request, 'main/checkout.html', context)

@login_required(login_url='index')
def ordered(request, confirmation_number):
	return render(request, 'main/ordered.html', {'confirmation_number':confirmation_number})

@login_required(login_url='index')
def viewOrder(request, confirmation_number):
	if request.user.is_superuser:
		order = Order.objects.get(checkout=True, confirmation_number=confirmation_number)
	else:
		order = Order.objects.get(user=request.user, checkout=True, confirmation_number=confirmation_number)
	carts = order.cart_set.all()
	context = {'order':order, 'carts':carts}
	return render(request, 'main/vieworder.html', context)

@login_required(login_url='index')
def updateCart(request):
	if request.method == "POST":
		data = json.loads(request.body)
		product_id = data['product_id']
		action = data['action']
		product = Product.objects.get(id=product_id)
		order, create = Order.objects.get_or_create(user=request.user, checkout=False)
		cart, create = Cart.objects.get_or_create(order=order, product=product)
		if action == "add":
			cart.quantity += 1
		elif action == "remove":
			cart.quantity -= 1
		cart.save()
		if cart.quantity <= 0:
			cart.delete()
		return JsonResponse({'data':data})
	return redirect('home')

def getConfirmationNumber():
	while True:
		confirmation_number = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = 10))	
		if not Order.objects.filter(confirmation_number=confirmation_number).exists():
			break
	return confirmation_number

@login_required(login_url='index')
@checkSuperuser
def generateSecretKey(request):
	while True:
		secret_key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = 10))	
		if not Secret.objects.filter(secret_key=secret_key).exists():
			break
	if not Secret.objects.filter(active=True).exists():
		secret = Secret.objects.create(secret_key=secret_key, active=True)
		context = {'secret_key':secret.secret_key}
	else:
		secret = Secret.objects.get(active=True)
		context = {'secret_key':secret.secret_key}
	return render(request, 'main/secret.html', context)

@login_required(login_url='index')
@checkSuperuser
def updateSecretKey(request):
	if request.is_ajax():
		while True:
			secret_key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = 10))	
			if not Secret.objects.filter(secret_key=secret_key).exists():
				break
		secret = Secret.objects.get(active=True)
		secret.delete()
		secret = Secret.objects.create(secret_key=secret_key, active=True)
		context = {'secret_key':secret.secret_key}
		return JsonResponse(context)
	else:
		return HttpResponseRedirect('home')