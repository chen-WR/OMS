from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	id = models.AutoField(primary_key=True)

	def __str__(self):
		return f"{self.username}"

class Product(models.Model):
	id = models.AutoField(primary_key=True)
	sap_code = models.IntegerField()
	name = models.CharField(max_length=100)
	inventory = models.IntegerField()
	price_per_unit = models.DecimalField(max_digits=6, decimal_places=2)
	availability = models.BooleanField()

	def __str__(self):
		return f"{self.name}"

class Order(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	product = models.ManyToManyField(Product)
