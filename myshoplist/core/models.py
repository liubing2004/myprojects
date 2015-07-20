from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    name = models.CharField(max_length=20, default="")
    

    def __str__(self):
        return self.name + "," + self.user.username



# class ShopList(models.Model):
#     owner = models.ForeignKey(User)
#     name = models.CharField(max_length=20, default="")
#     
#     def __str__(self):
#         return self.name


class Store(models.Model):
    name = models.CharField(max_length=20, default="")
    
    def __str__(self):
        return self.name

class ShopItem(models.Model):
    owner = models.ForeignKey(User)
    shopList = models.CharField(max_length=20, default="")
    store = models.ForeignKey(Store)
    name = models.CharField(max_length=20, default="")
    
    def __str__(self):
        return self.name
    
    