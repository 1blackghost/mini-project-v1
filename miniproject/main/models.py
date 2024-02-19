from django.db import models
import hashlib
import random
import string

class User(models.Model):
    uid = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=128)  
    email_verified = models.BooleanField(default=False)  #
    additional_params = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.name
    


class Verify_Email(models.Model):
    uid = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    hash = models.CharField(max_length=100)

    def generate_unique_hash(self):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        unique_hash = hashlib.sha256((self.email + random_string).encode()).hexdigest()
        self.hash = unique_hash
        self.save()

    def __str__(self):
        return self.email
