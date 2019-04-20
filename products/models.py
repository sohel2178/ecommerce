from django.db import models
import random
import os
from .utils import unique_slug_generator
from django.db.models.signals import pre_save,post_save

from django.db.models import Q


def get_file_ext(file_path):
    return os.path.splitext(file_path)


def upload_image_path(instance,filename):
    print(instance)
    print(filename)
    new_filename = random.randint(1,85544655654)
    name,ext = get_file_ext(filename)
    return f'products/{new_filename}.{ext}'


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self): #Product.objects.featured() 
        return self.get_queryset().featured()

    def search(self,query):
        lookups =( 
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tag__title__icontains=query)
            )
        return Product.objects.filter(lookups).distinct()




# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/products/{self.slug}/"

    @property
    def name(self):
        return self.title


def product_pre_save_receiver(sender,instance,*args, **kwargs):
    print("Called")
    if not instance.slug:
        print("Called")
        instance.slug = unique_slug_generator(instance=instance)

pre_save.connect(product_pre_save_receiver,sender=Product)
