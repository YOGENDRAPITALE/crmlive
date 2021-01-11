from django.shortcuts import render, redirect
from django.http import HttpResponse


def unauthenticated_user(view_func):

	def wraper_func(request, *args, **kwargs):

		if request.user.is_authenticated:
				return redirect('home')		
		else:		
			return view_func(request, *args, **kwargs)

	return wraper_func


def allowed_user(allowed_roles=[]):

	def decorator(view_func):

		def wraper_func(request, *args, **kwargs):

			print('working')
			group =None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			
			if group in allowed_roles:		
				return view_func(request, *args, **kwargs)
			else:
			 return HttpResponse('You are not authorised to this page')	
		return wraper_func
	return decorator



def admin_only(view_func):

	def wrapper_function(request, *args, **kwargs):

		print('working')
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name
		
		if group == 'customer':
			return redirect('user')
		if group == 'admin':
			return view_func(request, *args, **kwargs)
		
	return wrapper_function
