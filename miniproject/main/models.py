from django.db import models

class User(models.Model):
    uid = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=128)  
    email_verified = models.BooleanField(default=False)  #
    additional_params = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.name
	
