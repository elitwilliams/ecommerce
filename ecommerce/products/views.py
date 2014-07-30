from django.shortcuts import render

from .models import Product

# Create your views here.

def home(request):
	products = Product.objects.all()
	template = 'products/home.html'
	context = {"products":products}

	return render(request, template, context)

def all(request):
	products = Product.objects.all()
	context = {'products': products}
	template = 'products/all.html'
	return render(request, template, context)