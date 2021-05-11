from django.http import JsonResponse, Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .decorators import checkLogin, checkSuperuser
from django.conf import settings
from django.views.generic.list import ListView
from .models import Product, Order

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
	return render(request, 'main/product.html', {})

@login_required(login_url='/')
def cart(request):
	return render(request, 'main/cart.html', {})

@login_required(login_url='/')
def checkout(request):
	return render(request, 'main/checkout.html', {})