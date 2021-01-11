from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
	
	user = models.OneToOneField(User, null=True, blank= True, on_delete=models.CASCADE)
	name = models.CharField(max_length=255, null= True)
	phone = models.CharField(max_length=255, null= True)
	email = models.CharField(max_length=255, null= True)
	profile_pic = models.ImageField(default = "default.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null= True)

	def __str__(self):
		return self.name

class Tag(models.Model):
	
	name = models.CharField(max_length=255, null= True)
	
	def __str__(self):
		return self.name

class Product(models.Model):

	CATEGORY_CHOICES = (
		('IN','Indoor'),
		('OUT','Outdoor'),
		)

	name = models.CharField(max_length=255, null= True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=3, null= True, choices=CATEGORY_CHOICES)
	description = models.CharField(max_length=255, null= True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null= True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name

class Order(models.Model):

	STATUS_CHOICES = (
		('P','Pending'),
		('O','Out for Delivery'),
		('D','Delivered')
		)

	customer = models.ForeignKey(Customer,null=True,on_delete = models.SET_NULL) 
	product = models.ForeignKey(Product,null=True,on_delete = models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null= True)
	status = models.CharField(choices=STATUS_CHOICES,max_length=1, null=True)
	note = models.CharField(max_length=1000, null=True)

	def __str__(self):
		return self.product.name
