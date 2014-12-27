from django.db import models
from django.contrib.auth.models import User
from paypal.standard.ipn.signals import payment_was_successful
from paypal.standard.ipn.tests.test_ipn import IPN_POST_PARAMS
from stripe.resource import Invoice

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    name = models.CharField(max_length=20, default="")
    
    def __str__(self):
        return self.name + "," + self.user.username
    
    
class ProjectProfile(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200, default="")
    profile_image = models.CharField(max_length=200, default="")
    threedmodel = models.CharField(max_length=200, default="")
    texture = models.CharField(max_length=200, default="")
    modelx = models.FloatField(default=0)
    modely = models.FloatField(default=0)
    modelz = models.FloatField(default=0)
    status = models.IntegerField(default=0)
    
    def __str__(self):
        return "id="+str(self.id)+", name="+self.name
    
class PriceUnit(models.Model):
    price = models.FloatField(default=0)
    material = models.CharField(max_length=50, default="")
    color = models.CharField(max_length=50, default="")
    finish = models.CharField(max_length=50, default="")
    unit = models.CharField(max_length=10, default="")
    
    def __str__(self):
        return self.material+","+self.color+","+self.finish+","+self.unit

class ShippingAddress(models.Model):
    user = models.ForeignKey(User)
    shipUserName = models.CharField(max_length=200, default="")
    country = models.CharField(max_length=200, default="")
    state = models.CharField(max_length=200, default="")
    city = models.CharField(max_length=200, default="")
    postcode = models.CharField(max_length=200, default="")
    addressline_1 = models.CharField(max_length=1024, default="")
    addressline_2 = models.CharField(max_length=1024, default="")
    phone = models.CharField(max_length=100, default="")
    
    def isEmpty(self):
        return self.user == None
    
class Order(models.Model):
   user = models.ForeignKey(User)
   shippingAddress =  models.ForeignKey(ShippingAddress)
   invoice = models.CharField(max_length=200, default="")
   gross = models.FloatField(default=0.0)
   paymentFee = models.FloatField(default=0)
   status = models.IntegerField(default=0)
    
class ShopCartItem(models.Model):
    user = models.ForeignKey(User)
    priceUnit = models.ForeignKey(PriceUnit)
    project = models.ForeignKey(ProjectProfile)
    sizex = models.FloatField(default=0)
    sizey = models.FloatField(default=0)
    sizez = models.FloatField(default=0)    
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(Order, default=0)
    
    @property
    def getPrice(self):
        return round(self.priceUnit.price * self.sizex * self.sizey * self.sizez , 2)
    
    @property
    def getTotalPrice(self):
        return round(self.priceUnit.price * self.sizex * self.sizey * self.sizez * self.quantity , 2)
    
    


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    print "ipn_obj", IPN_POST_PARAMS,ipn_obj.payment_status,\
        ipn_obj.custom,ipn_obj.invoice, ipn_obj.mc_gross, ipn_obj.mc_fee
    # You need to check 'payment_status' of the IPN

    if ipn_obj.payment_status == "Completed":
        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom == "Upgrade all users!":
            Users.objects.update(paid=True)
    else:
        pass
payment_was_successful.connect(show_me_the_money)
