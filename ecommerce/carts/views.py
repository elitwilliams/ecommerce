from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.

from products.models import Product

from .models import Cart, CartItem

def view(request):
	try:
		the_id = request.session['cart_id']
	except:
		the_id = None
	if the_id:
		cart = Cart.objects.get(id=the_id)
		context = {"cart": cart}		
	else:
		empty_message = "Your cart is empty! Please keep shopping."
		context = {"empty": True, 'empty_message':empty_message}

	template = "cart/view.html"
	return render(request, template, context)

def update_cart(request, slug, qty):
	request.session.set_expiry(120000)
	try:
		qty = request.GET.get('qty')
	except:
		qty = ''
		update_qty = False
	try:
		the_id = request.session['cart_id']
	except:
		new_cart = Cart()
		new_cart.save()
		request.session['cart_id'] = new_cart.id
		the_id = new_cart.id

	cart = Cart.objects.get(id=the_id)

	try:
		product = Product.objects.get(slug=slug)
	except Product.DoesNotExist:
		pass
	except:
		pass

	cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
	if created:
		print "yeah"
	if int(qty) == 0 and update_qty:
		cart_item.delete()
	elif update_qty:
		cart_item.quantity = qty
		cart_item.save()
	else:
		pass
	# if not cart_item in cart.items.all():
	# 	cart.items.add(cart_item)
	# else:
	# 	cart.items.remove(cart_item)

	new_total = 0.00
	for item in cart.cartitem_set.all():
			line_total = float(item.product.price) * item.quantity
			new_total += line_total

	cart.total = new_total
	cart.save()

	request.session['items_total'] = cart.cartitem_set.count()
	
	return HttpResponseRedirect(reverse('cart'))