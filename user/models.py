from django.db import models

# Create your models here.
class User(models.Model):
    id= models.AutoField(primary_key=True)
    verified = models.BooleanField(default=False) #email verification
    active = models.BooleanField(default=True) #user active status(not banned)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    email = models.EmailField(max_length = 254)
    password=models.CharField(max_length=20)
    picture=models.ImageField(upload_to ='profile_pictures/%y/%m/%d/',blank=True)
   
   
    class Meta:
            # Specify the custom collection name
            db_table = 'user'
 