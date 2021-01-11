from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
# Create your views here.

@unauthenticated_user
def registerPage(request):
		
	form =CreateUserForm()

	if request.method == 'POST':
		form =CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			group = Group.objects.get(name='customer')
			user.groups.add(group)

			Customer.objects.create(
				user=user
			)
			messages.success(request, 'Account was created for '+username)
			return redirect('login')
	context={'form':form}
	return render(request,'accounts/register.html',context)


@unauthenticated_user
def loginPage(request):

	if request.method== 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username = username, password = password)
		if user is not None:
			login(request,user)
			return redirect('home')

		else:
			messages.info(request, 'Username or Password is incorrect')

	context={}
	return render(request,'accounts/login.html',context)

def logoutUser(request):
	
	logout(request)
	return redirect('login')

def userPage(request):
	orders = request.user.customer.order_set.all()
	total_orders = orders.count()
	delhivered = orders.filter(status='D').count()
	pending =orders.filter(status='P').count()

	context={'orders':orders,'total_orders':total_orders,'delhivered':delhivered, 'pending':pending}
	return render(request,'accounts/user.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def accountSettings(request):
	user = request.user.customer
	form =CustomerForm(instance=user)
	if  request.method == 'POST':
		form =CustomerForm(request.POST,request.FILES ,instance=user)
		if form.is_valid():
			form.save()
	context = {'form':form}
	return render(request,'accounts/account_settings.html', context)

@login_required(login_url='login')
@admin_only
def home(request):
	orders= Order.objects.all()
	customers = Customer.objects.all()
	total_customers = customers.count()
	total_orders = orders.count()
	delhivered = orders.filter(status='D').count()
	pending =orders.filter(status='P').count()
	context ={
	'orders':orders,
	'customers':customers,
	'total_customers':total_customers,
	'total_orders':total_orders,
	'delhivered':delhivered,
	'pending': pending
	}
	return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def product(request):
	products = Product.objects.all()

	context = {
		'products':products
	}
	return render(request,'accounts/product.html',context)


	
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer(request,cid):
	customer = Customer.objects.get(id=cid)

	orders = customer.order_set.all()
	orders_count = orders.count()
	myFilter = OrderFilter(request.GET,queryset=orders)
	orders = myFilter.qs
	context={
		'customer':customer,
		'orders':orders,
		'orders_count':orders_count,
		'myFilter':myFilter
	}
	return render(request,'accounts/customer.html', context)



	
@login_required(login_url='login')
def create_order(request, coid):
	OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
	customer = Customer.objects.get(id=coid)
	print(customer,'save')
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	# form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		
		print('Printing Post',request.POST)
		# form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)

		if formset.is_valid():
			formset.save()
			return redirect('/')

	context={
		'formset':formset
	}
	return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def update_order(request,uoid):

	order =Order.objects.get(id=uoid)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		
		print('Printing Post',request.POST)
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {
		'form':form,
		'order':order,
	}

	return render(request,'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def delete_order(request,doid):
	order =Order.objects.get(id=doid)

	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context = {
		'order':order
	}
	return render(request,'accounts/delete.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])

def create_customer(request):

	form = CustomerForm()
	if request.method == 'POST':
		
		print('Printing Post',request.POST)
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context={
		'form':form
	}
	return render(request,'accounts/customer_form.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])

def update_customer(request,ucid):

	customer =Customer.objects.get(id=ucid)
	form = CustomerForm(instance=customer)
	if request.method == 'POST':
		
		print('Printing Post',request.POST)
		form = CustomerForm(request.POST, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {
		'form':form,
		'customer':customer,
	}

	return render(request,'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def delete_customer(request,dcid):
	customer = Customer.objects.get(id=dcid)

	if request.method == 'POST':
		customer.delete()
		return redirect('/')
	context = {
		'customer':customer
	}
	return render(request,'accounts/delete.html', context)
