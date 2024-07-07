from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

import os
from django.db import models
from django.core.files import File
from urllib.request import urlopen

class Image(models.Model):
    photo = models.ImageField(upload_to="myImage")
    date = models.DateTimeField(auto_now_add=True)

    def save_image_from_url(url):
       
        img_name = os.path.basename(url)
        response = urlopen(url)
        image = File(response)
        new_image = Image()
        new_image.photo.save(img_name, image, save=True)
    
##################################################

class UserManager(BaseUserManager):

    def create_user(self, username, email, password ):
        if not username:
            raise ValueError("Username cannot be empty")
        if not email:
            raise ValueError("Email cannot be empty")
        
        user = self.model (
            username=username,
            email=email,
            password=make_password(password)  
        )
        user.save()
        return user
    
    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(username, email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    def get_by_natural_key(self, username):
     return self.get(**{self.model.USERNAME_FIELD: username})

   

class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'  
    REQUIRED_FIELDS = ['password']  
    
    objects = UserManager() 

    def __str__(self):
        return self.email 

    
##########################
