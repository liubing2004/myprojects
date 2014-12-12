from django.db import models
from django.contrib.auth.models import User

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
    status = models.IntegerField(default=0)
    
    def __str__(self):
        return "id="+str(self.id)+", name="+self.name
    
    
    
