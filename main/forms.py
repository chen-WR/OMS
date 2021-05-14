from django import forms

class CheckoutForm(forms.Form):
	email = forms.EmailField(label="Email")
