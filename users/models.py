from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    nid = models.TextField(max_length=30,null=True,blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,**kwargs):
        super().save()

        print("Called")

        img = Image.open(self.image.path)

        if img.height>300 or img.width>300:
            print("Actual Call")
            resize_dim=(150,150)
            img.thumbnail(resize_dim)
            img.save(self.image.path)

