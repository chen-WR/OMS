from django import forms
from .models import User, Secret
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
	store_name = forms.CharField(label="Store Name", help_text="Store Location and Name")
	secret_key = forms.CharField(label="Secret Key", help_text="Secret Key from Admin")
	class Meta:
		model = User
		fields = ['username', 'email',  'password1', 'password2', 'store_name', 'secret_key']

	def clean(self):
		email = self.cleaned_data.get('email')
		username = self.cleaned_data.get('username')
		secret_key = self.cleaned_data.get('secret_key')
		if User.objects.filter(email=email).exists():
			raise ValidationError("Account with that email already exists")
		if User.objects.filter(username=username).exists():
			raise ValidationError("Account with that username already exists")
		if not Secret.objects.filter(secret_key=secret_key).filter(active=True).exists():
			raise ValidationError('Secet Key Does Not Exist')
		return self.cleaned_data