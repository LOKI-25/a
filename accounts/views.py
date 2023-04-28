
from django.shortcuts import render , redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile
import random

# import http.client
from twilio.rest import Client

from django.conf import settings
from django.contrib.auth import authenticate, login

# Create your views here.

def cart(request):
    return render(request, 'accounts/cart.html')
def send_otp(mobile , otp):
    print("FUNCTION CALLED")
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                                    body=f'The otp is {otp}',
                                    
                                                    from_='',
                                                    to=f'+91{mobile}'
                                                )

    print(message)
    return None



def login_attempt(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        user = Profile.objects.filter(mobile = mobile).first()
        
        if user is None:
            context = {'message' : 'User not found' , 'class' : 'danger' }
            return render(request,'accounts/login.html' , context)
        
        otp = str(random.randint(1000 , 9999))
        user.otp = otp
        user.save()
        send_otp(mobile , otp)
        request.session['mobile'] = mobile
        return redirect('login_otp')        
    return render(request,'accounts/login.html')


def login_otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        
        if otp == profile.otp:
            user = User.objects.get(id = profile.user.id)
            login(request , user)
            print(user)
            return redirect('/')
        else:
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'accounts/login_otp.html' , context)
    
    return render(request,'accounts/login_otp.html' , context)

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['first_name']
        mobile = request.POST['mobile']
        username=request.POST['username']
        gender=request.POST['gender']
        city=request.POST['city']
        state=request.POST['state']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1 == password2:
            if Profile.objects.filter(mobile=mobile).exists():
                messages.info(request,'Phone number is already Taken.')
                return render(request,'accounts/register.html',{'success':True})
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username is already Taken.')
                return render(request,'accounts/register.html',{'success':True})
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=name)
                profile=Profile(user=user,mobile=mobile,otp=1111,name=name,gender=gender,city=city,state=state)
                user.save()
                profile.save()
                print('user created')
                return redirect('login')
        else:
            messages.info(request,'Password is not matched')
            return render(request,'accounts/register.html',{'success':True})

        check_user = User.objects.filter(email = email).first()
        check_profile = Profile.objects.filter(mobile = mobile).first()
        


        if check_user or check_profile :
            context = {'message' : 'User already exists' , 'class' : 'danger' }
            return render(request,'accounts/register.html' , context)
            
        user = User(email = email , first_name = name)
        user.save()
        otp = str(random.randint(1000 , 9999))
        profile = Profile(user = user , mobile=mobile , otp = otp,name=name) 
        profile.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('otp')
    return render(request,'accounts/register.html')

def otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        
        if otp == profile.otp:
            return redirect('cart')
        else:
            print('Wrong')
            
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'accounts/otp.html' , context)
            
    return render(request,'accounts/otp.html' , context)

def logout(request):
    auth.logout(request) 
    return redirect("/")