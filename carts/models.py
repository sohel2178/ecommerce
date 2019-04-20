from django.db import models
from products.models import Product
from django.contrib.auth.models import User

from django.db.models.signals import pre_save,post_save,m2m_changed

# Create your models here.

class CartManager(models.Manager):

    def new_or_get(self,request):
        cart_id = request.session.get('cart_id',None)
        qs = self.get_queryset().filter(id=cart_id)



        if qs.count() == 1:
            cart_obj = qs.first()
            is_created=False
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
            print("Cart Exist "+str(cart_obj.id))
        else:
            cart_obj = Cart.objects.new_cart(user=request.user)
            is_created=True
            request.session['cart_id']=cart_obj.id

        return cart_obj,is_created

    
    def new_cart(self,user=None):
        print(user)
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    total = models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    time_to_add = models.DateTimeField(auto_now_add=True)
    time_to_update = models.DateTimeField(auto_now=True)

    objects= CartManager()

    def __str__(self):
        return str(self.id)


def call_before_cart_save(sender,instance,action,*args,**kwargs):
    print(action)

    if action is 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            print(x.price)
            total += x.price

        instance.total = total
        instance.save()

m2m_changed.connect(call_before_cart_save,sender=Cart.products.through)

def update_subtotal(sender,instance,*args,**kwars):
    if instance.total > 0:
        instance.subtotal = instance.total + 10
    else:
        instance.subtotal = 0

pre_save.connect(update_subtotal,sender=Cart)
