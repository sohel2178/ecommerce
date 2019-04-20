from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product
from carts.models import Cart

# Create your views here.

class ProductListView(ListView):
    model = Product


    # Unimpotant Method
    def get(self, request, *args, **kwargs):
        print(request.session.get('first_name',"Unknown"))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart,is_new = Cart.objects.new_or_get(self.request)
        context['cart'] = cart

        return context

class ProductDetailView(DetailView):
    model = Product
    template_name='products/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart,is_new = Cart.objects.new_or_get(self.request)
        context['cart'] = cart

        return context

    

