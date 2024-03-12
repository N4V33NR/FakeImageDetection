from django.shortcuts import render,redirect
from django.http import HttpResponse,request
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
import tensorflow as tf
from django.contrib import messages



import numpy as np
from .form import ImageForm
from .models import User
import cv2
import os

MEDIA_ROOT = 'C:\\Users\\Dell\\projects\\FakeImageDetection\\media\\myImage'

# Create your views here.


def welcome(request):
   return render(request,"welcome.html") 


    

def signup(request):
   if request.method=="POST":
      username=request.POST['username']
      email=request.POST['email']
      password=request.POST['password']

      user= User.objects.create_user(username=username,email=email,password=password) 
      user.save()
      print("user created")
      return redirect('home')

   else: return render(request,"signup.html")


def logIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)
            print("User logged in")
            return redirect('home')
        else:
            messages = "Invalid credentials" # Use error message type
            return render(request, 'login.html',{'messages':messages})
    else:
        messages = ""
        return render(request, "login.html",{'messages':messages})
  
  

   

        
    


###########################################################################

def preprocess_image(image):
    # Read the image using OpenCV
    
    
    # Resize the image to a fixed size (e.g., 150x150 pixels)
    image = cv2.resize(image, (150, 150))
    
    # Convert the image to RGB color space (if it's in BGR format)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Normalize pixel values to range [0, 1]
    image = image.astype('float32') / 255.0
    
    # Expand dimensions to add batch dimension
    image = np.expand_dims(image, axis=0)
    
    return image

def predict_image(image):
    model = tf.keras.models.load_model('fake_image_classifier_model.h5')
    image = preprocess_image(image)
    prediction = model.predict(image)
    if prediction[0][0] > 0.5:
        return "Fake"
    else:
        return "Real"
    

def home(request):
    if request.method == 'POST':
        form= ImageForm(request.POST, request.FILES)
        if form.is_valid():
         form.save()
        uploaded_file = form.cleaned_data['photo']  
        filename = uploaded_file.name
        # image_path =request.POST.get('image')
        file_path = os.path.join(MEDIA_ROOT, filename)
        image = cv2.imread(file_path)
        
        prediction = predict_image(image)

        return render(request,"home.html",{'result':prediction})
      
    else:
      if not request.user.is_authenticated:
         msg="You are not logged in please log in first"
         return render(request,'login.html',{'messages':msg})
      else:
         return render(request,"home.html",{'form':ImageForm})
######################################################################## 