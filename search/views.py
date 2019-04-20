from django.shortcuts import render
from django.views.generic import ListView,DetailView
from products.models import Product

# Create your views here.

class SearchListView(ListView):
    model = Product
    template_name = 'search/list.html'

    def get_queryset(self):
        request = self.request
        print(request.GET.get('q'))
        # query = self.request.GET.
        if self.request.GET.get('q'):
            q_set = Product.objects.search(self.request.GET.get('q'))

            if len(q_set)>0:
                return q_set
            else:
                return Product.objects.featured()

        return Product.objects.featured()

