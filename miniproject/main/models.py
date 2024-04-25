from django.db import models
import hashlib
import random
import string

class Teacher(models.Model):
    uid = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=100)
    profile = models.EmailField(unique=True)  
    data = models.CharField(max_length=128)  
    additional_params = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.name
