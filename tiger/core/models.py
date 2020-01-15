from django.db import models
from django.contrib.auth.models import User
from paypal.standard.ipn.signals import payment_was_successful
from paypal.standard.ipn.tests.test_ipn import IPN_POST_PARAMS

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    name = models.CharField(max_length=20, default="")
    
    def __str__(self):
        return self.name + "," + self.user.username
    
    


