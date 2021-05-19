from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static

class User(AbstractUser):
	id = models.AutoField(primary_key=True)
	store_name = models.CharField(max_length=100)
	allow_edit = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.username}"

class Secret(models.Model):
	id = models.AutoField(primary_key=True)
	secret_key = models.CharField(max_length=10, blank=True, null=True)
	active = models.BooleanField(default=False)

class Product(models.Model):
	id = models.AutoField(primary_key=True)
	category = models.CharField(max_length=100, null=True, blank=True)
	sap = models.IntegerField(null=True, blank=True)
	description = models.CharField(max_length=100, null=True, blank=True)
	picture = models.ImageField(null=True, blank=True)
	size = models.CharField(max_length=100, null=True, blank=True)
	unit_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
	unit = models.IntegerField(null=True, blank=True)
	availability = models.BooleanField(default=True)
	
	def __str__(self):
		return f"{self.description}"

	@property
	def imageURL(self):
		try:
			url = static(self.picture.url)
		except:
			url = static("unavailable.jpg")
		return url

class Order(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	date = models.DateTimeField(default=timezone.now)
	checkout = models.BooleanField(default=False)
	confirm = models.BooleanField(default=False)
	confirmation_number = models.CharField(max_length=30, blank=True, null=True)
	comment = models.CharField(max_length=300, blank=True, null=True)
	tracking_number = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return f"user:{self.user}--checkout:{self.checkout}"

	@property
	def getCartList(self):
		carts = self.cart_set.all()
		lists = len([cart.product for cart in carts])
		return lists
	
	@property
	def getCartCount(self):
		carts = self.cart_set.all()
		total = sum([cart.getItemCount for cart in carts])
		return total

	@property
	def getCartTotal(self):
		carts = self.cart_set.all()
		total = sum([cart.getItemTotal for cart in carts])
		return total

	@property
	def getShippedCount(self):
		carts = self.cart_set.all()
		lists = len([cart.shipped_quantity for cart in carts if cart.shipped_quantity != 0])
		return lists
	
	@property
	def getShippedTotal(self):
		carts = self.cart_set.all()
		total = sum([cart.getShipableTotal for cart in carts])
		return total	

class Cart(models.Model):
	id = models.AutoField(primary_key=True)
	order = models.ForeignKey(Order, null=True, blank=True,on_delete = models.SET_NULL)
	product = models.ForeignKey(Product, null=True, blank=True,on_delete = models.SET_NULL)
	quantity = models.IntegerField(default=0, blank=True, null=True)
	shipped_quantity = models.IntegerField(default=0, blank=True, null=True)

	def __str__(self):
		return f"product:{self.product}"

	@property
	def getItemTotal(self):
		total = self.product.unit_price * self.quantity
		return total
	
	@property
	def getItemCount(self):
		total = self.product.unit * self.quantity
		return total

	@property
	def getShipableTotal(self):
		total = self.product.unit_price * self.shipped_quantity
		return total

	
	


	
	


	



