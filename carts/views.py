from django.shortcuts import render,redirect

from .models import Cart
from products.models import Product

# Create your views here.

def cart_home(request):
    cart_obj,is_created = Cart.objects.new_or_get(request)
    


    print(cart_obj,is_created)
    
        

    # print(cart_id)
    # print(request.session.__dict__)
    # print(request.session.session_key)

    # request.session['first_name'] = 'Sohel'

    # print(dir(request.session))
    return render(request,'carts/home.html',{"cart":cart_obj})

def cart_update(request):
    print(request.POST)
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)

    cart,is_created = Cart.objects.new_or_get(request)

    if product in cart.products.all():
        cart.products.remove(product)
    else:
        cart.products.add(product)

    return redirect("product-list")
