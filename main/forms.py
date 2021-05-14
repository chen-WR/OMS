from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class CheckoutForm(forms.Form):
	email = forms.EmailField(label="Email")

class RegisterForm(UserCreationForm):
	secret_key = forms.CharField(label="Secret Key")
	class Meta:
		model = User
		fields = ['username', 'email',  'password1', 'password2', 'store_name', 'secret_key']

	def clean(self):
		email = self.cleaned_data.get('email')
		username = self.cleaned_data.get('username')
		if User.objects.filter(email=email).exists():
			raise ValidationError("account with that email already exists")
		if User.objects.filter(username=username).exists():
			raise ValidationError("account with that username already exists")
		return self.cleaned_data