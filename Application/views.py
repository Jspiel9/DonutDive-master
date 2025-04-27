# views.py

from datetime import datetime, timedelta
from django.utils import timezone
from django.db import IntegrityError
from django.conf import UserSettingsHolder
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from djangoApplication import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from .models import CustomUser
from django.http import HttpResponseForbidden


def Home(request):
    fname = request.user.first_name if request.user.is_authenticated else ''
    context = {'fname': fname}
    return render(request, "Application/Home.html", context)

def Calendar(request):
    fname = request.user.first_name if request.user.is_authenticated else ''
    context = {'fname': fname}
    return render(request, "Application/Calendar.html", context)

def Contacts(request):
    fname = request.user.first_name if request.user.is_authenticated else ''
    context = {'fname': fname}
    return render(request, "Application/Contacts.html", context)

def Weekly_reward(request):
    fname = request.user.first_name if request.user.is_authenticated else ''
    context = {'fname': fname}
    if request.method == "POST":
        # Check if the user is authenticated
        if request.user.is_authenticated:
            user = request.user
            last_claim_time = user.last_reward_claim_time

            # Check if the user has already claimed the reward within the past week
            if last_claim_time is None or (timezone.now() - last_claim_time).days >= 7:
                # Update the last claim time for the user
                user.last_reward_claim_time = timezone.now()
                user.save()
                return HttpResponse("You have successfully claimed your weekly reward.")
            else:
                return HttpResponseForbidden("You have already claimed your weekly reward.")
        else:
            return HttpResponseForbidden("You need to log in to claim the reward.")
    else:
        return render(request, "Application/Weekly_reward.html", context)

def Login(request):
    context = {}

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "Application/home.html", {'fname': fname})
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('Home')

    return render(request, "Application/Login.html", context)

def Signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        try:
            # Check if the username already exists
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different username.")
                return redirect('Signup')
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists. Please choose a different Email.")
                return redirect('Signup')
            if len(username)>10:
                messages.error(request, "Username must be under 10 characters.")
                
            if pass1 != pass2:
                messages.error(request, "Passwords didn't match.")
                
            if not username.isalnum():
                messages.error(request, "Username must be Alpha-Numeric.")
                return redirect('Signup')

            # Create the user if the username is unique
            myuser = CustomUser.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = False
            myuser.save()

            # Welcome Email

            subject = "Welcome to the Donut Dive Website!"
            message = "Hello " + myuser.first_name + "!! \n" + "Welcome to the Donut Dive website!! \n Thank you for visiting our website \n We have also sent you a confirmation email, please confirm your email address in order to activate your account.  \n\n Thank you." 
            from_email = settings.EMAIL_HOST_USER
            to_email = myuser.email
            send_mail(subject, message, from_email, [to_email], fail_silently = True)

            # Confirmation Email

            current_site = get_current_site(request)
            email_subject = "Confirm your email @ Donut Dive!"
            message2 = render_to_string('email_confirmation.html',{
                'name': myuser.first_name,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser),
            })

            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )
            email.fail_silently = True
            email.send()


            messages.success(request, "Sign up successful. We have sent you a confirmation email, please verify your account before logging in.")
            return redirect('Login')
        
        except IntegrityError:
            # Handle integrity error (e.g., database constraint violation)
            messages.error(request, "An error occurred during sign up. Please try again.")
            return redirect('Signup')
        
    
    return render(request, "Application/Signup.html", {})

def Logout(request):
    context = {}
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('Home')
    

def Activate(request, uidb64, token):
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('Home')
    else:
        return render(request, 'Activation_failed.html')

def check_authentication(request):
    if request.user.is_authenticated:
        return JsonResponse({'message': 'User is authenticated', 'username': request.user.username})
    else:
        return JsonResponse({'message': 'User is not authenticated'})

