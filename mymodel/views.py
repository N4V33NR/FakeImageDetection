from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
import tensorflow as tf
from django.http import HttpResponse
import numpy as np
from .form import ImageForm
from .models import User,Image
import cv2
import os

MEDIA_ROOT = 'C:\\Users\\Dell\\projects\\FakeImageDetection\\media\\myImage'


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
    
    image = cv2.resize(image, (150, 150))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.astype('float32') / 255.0
    image = np.expand_dims(image, axis=0)
    
    return image

def predict_image(image):
    model = tf.keras.models.load_model('fake_image_classifier_model.h5')
    image = preprocess_image(image)
    prediction = model.predict(image)
    print(prediction)
    if prediction[0][0] > 0.5:
        return "Fake"
    else:
        return "Real"
    



def home(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if file is uploaded
            if request.FILES:
                form.save()
                uploaded_file = form.cleaned_data['photo']
                filename = uploaded_file.name
                file_path = os.path.join(MEDIA_ROOT, filename)
                image = cv2.imread(file_path)
                prediction = predict_image(image)
                img = Image.objects.order_by('-id').first()
                return render(request, "home.html", {'result': prediction, 'img': img, 'form': ImageForm()})
            # Check if URL is provided
    if request.method == 'POST':
        url = request.POST.get('image_url')
        
        try:
            Image.save_image_from_url(url)
            img = Image.objects.order_by('-id').first()
            image_file = img.photo
            file_path = image_file.path
            image = cv2.imread(file_path)
            prediction = predict_image(image)
            return render(request, "home.html", {'result': prediction, 'img': img, 'form': ImageForm()})
        except Exception as e:
            print("Error:", e)  
            return HttpResponse(f"Error downloading or saving image: {str(e)}")
    else:
        form = ImageForm()
    return render(request, "home.html", {'form': form})

######################################################################## 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2

@csrf_exempt
def check_image_authenticity(request):
    if request.method == 'POST':
        # Assuming the image URL is sent in the request body
        image_url = request.POST.get('image_url')
       
        if image_url:
           Image.save_image_from_url(image_url)
           img = Image.objects.order_by('-id').first()
           image_file = img.photo
           file_path = image_file.path
           image = cv2.imread(file_path)
           prediction = predict_image(image)
           return JsonResponse({'authenticity': prediction})
        else:
            return JsonResponse({'error': 'Image URL not found'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
