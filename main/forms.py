from django import forms
from .models import User, StoreSecret, WarehouseSecret
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
	store_name = forms.CharField(label="Store Name", help_text="Store Name")
	store_location = forms.IntegerField(label="Store Location", help_text="Three Digit Store Code")
	secret_key = forms.CharField(label="Secret Key", help_text="Secret Key from Admin")
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2', 'store_name', 'store_location', 'secret_key']

	def clean(self):
		username = self.cleaned_data.get('username')
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		secret_key = self.cleaned_data.get('secret_key')
		if User.objects.filter(username=username).exists():
			raise ValidationError("Account with that username already exists")
		if not Secret.objects.filter(secret_key=secret_key).filter(active=True).exists():
			raise ValidationError('Secet Key Does Not Exist')
		if password1 and password2 and password1 != password2:
			raise ValidationError("Password Does Not Match")
		return self.cleaned_data

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.username = self.cleaned_data["username"]
		user.password1 = self.cleaned_data["password1"]
		user.store_name = self.cleaned_data["store_name"]
		user.store_location= self.cleaned_data["store_location"]
		user.secret_key = self.cleaned_data["secret_key"]
		if commit:
			user.save()
		return user