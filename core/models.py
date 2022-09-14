from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Profile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  interests = models.CharField(max_length=500,blank=True, null=True) 
  country = models.CharField(max_length=100,blank=True, null=True) 
  
  def __str__(self): 
    return self.user.username