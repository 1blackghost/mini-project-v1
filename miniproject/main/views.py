from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.template import loader
from django.middleware.csrf import get_token
from .models import User
from django.contrib.auth.hashers import make_password, check_password
import time
from .models import Verify_Email


def verify(request, hash_value):
    try:
        verify_email = Verify_Email.objects.get(hash=hash_value)
        user = User.objects.get(email=verify_email.email)
        request.session.clear()
        request.session["user"]=user.name
        user.email_verified = 1
        user.save()
        verify_email.delete()

        template = loader.get_template('verified.html')
        return HttpResponse(template.render())  
    except Verify_Email.DoesNotExist:
        return JsonResponse({"message": "Invalid verification link"}, status=400)

def resend(request):
    verification_started = request.session.get("verification_started")
    
    if verification_started and request.session.has_key("user"):
        timer_duration = 10
        
        current_time = time.time()
        last_request_time = request.session.get("last_request_time", current_time)
        elapsed_time = current_time - last_request_time
        
        if elapsed_time >= timer_duration:
            request.session["last_request_time"] = current_time
            
            email = request.session.get("email")
            verify_email, created = Verify_Email.objects.get_or_create(email=email)
            
            if created or not verify_email.hash:
                verify_email.generate_unique_hash()
                send_verification_email(email, verify_email.hash)  # Call send_verification_email
            else:
                verify_email.generate_unique_hash()
                send_verification_email(email, verify_email.hash)  # Call send_verification_email
                
            return redirect("unverified")
        else:
            return HttpResponse("Time has not elapsed yet")
    else:
        return HttpResponse("You're not logged in.")
            

def unverified(request):
    verification_started = request.session.get("verification_started")
    if verification_started and request.session.has_key("user"):
        timer_duration = 10
        current_time = time.time()
        if not request.session.has_key("last_request_time"):
            email = request.session.get("email")
            verify_email, created = Verify_Email.objects.get_or_create(email=email)
            
            if created or not verify_email.hash:
                verify_email.generate_unique_hash()
            send_verification_email(email, verify_email.hash)
        last_request_time = request.session.get("last_request_time", current_time)
        elapsed_time = current_time - last_request_time

        remaining_time = max(timer_duration - elapsed_time, 0)

        request.session["last_request_time"] = current_time

        template = loader.get_template("unverified.html")
        mail=request.session.get("email")
        mail=mail.split("@")
        l=len(mail[0])-1
        formated_email=mail[0][0]+str(l*"*")+"@"+mail[1]
        context = {"email": formated_email, "timer_duration": remaining_time}
        render = template.render(context, request)
        return HttpResponse(render)
    else:
        return HttpResponse("Verification not started or user not logged in")

def send_verification_email(email, hash_value):
    print("verify email here: /verify/"+hash_value)

def logout(request):
    request.session.clear()
    return HttpResponse("logged out")

def cart(request,value):
    if request.method == "POST":
        print("value",value)
        return HttpResponse("ok")

def dash(request):
    if request.session.get("user"):
        template = loader.get_template('dash.html')
        return HttpResponse(template.render())
    else:
        return redirect("login")

def index(request):
    
    template = loader.get_template('home.html')
    return HttpResponse(template.render())


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                if user.email_verified:  
                    request.session["user"] = user
                    return JsonResponse({"message": "success"}, status=200)
                if not user.email_verified:
                    request.session["user"] = user
                    request.session["verification_started"]=True
                    request.session["email"]=user.email
                    return JsonResponse({"message": "verify"}, status=200)
                else:
                    return JsonResponse({"message":"Something went wrong:("},status=500)
            else:
                return JsonResponse({"message": "Incorrect password"}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"message": "User does not exist"}, status=404)
        except Exception as e:
            print(str(e))
            return JsonResponse({"message": "Something went wrong:("}, status=500)

    else:
        csrf_token = get_token(request)
        context = {'csrf_token': csrf_token}
        template = loader.get_template('login.html')
        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template)


def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get("confirm")
        if (password != confirm):
            return JsonResponse({"message": "Passwords Doesn't Match :("}, status=500)

        additional_params = request.POST.get('additional_params')
        try:
            new_user = User(name=name, email=email, password=make_password(
                password), additional_params=additional_params)
            new_user.save()
            return JsonResponse({'message': 'success'}, status=200)
        except Exception as e:
            print(str(e))
            return JsonResponse({"message": "Something Went Wrong :("}, status=500)

    else:
        csrf_token = get_token(request)
        context = {'csrf_token': csrf_token}
        template = loader.get_template('signup.html')
        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template)
