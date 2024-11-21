from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from api.models import User
from api.models import User
# Create your views here.

def signup(request):
    if request.method == "POST" :
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"] # password2 is the confirm password field
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already taken")
                return redirect("signup/")
            elif User.objects.filter(username=username).exists():           #! change maybe
                messages.error(request, "Username is already taken")
                return redirect("signup/")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                user_model = User.objects.get(email=email)
                new_profile = Profile.objects.create(user=user_model, email=email) #remider email is primary key
                new_profile.save()
                
                messages.success(request, "You are now registered and can log in")
                return redirect("login")
        else:
            messages.error(request, "Passwords do not match")
            return redirect("signup/")
    
    else:
       return render(request, "register_app/registration.html")
   
   
def login(request):
    render(request, "register_app/login.html")