from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.middleware.csrf import get_token  
from .models import User 

def logout(request):
    request.session.clear()
    return HttpResponse("logged out")

def dash(request):
    if request.session.has_key("user"):
        return HttpResponse("logged in")
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
            if password==user.password:  
                if True:#user.email_verified:  # Check if email is veri
                    request.session["user"]=user
                    return JsonResponse({"message": "success"}, status=200)
                else:
                    return JsonResponse({"message": "Email not verified"}, status=403)
            else:
                return JsonResponse({"message": "Incorrect password"}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"message": "User does not exist"}, status=404)
        except Exception as e:
            print(str(e))
            return JsonResponse({"message": "Something went wrong :("}, status=500)

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
        confirm  = request.POST.get("confirm")
        if (password!=confirm):
        	return JsonResponse({"message":"Passwords Doesn't Match :("},status=500)
        	
        additional_params = request.POST.get('additional_params')  
        try:
        	new_user = User(name=name, email=email, password=password, additional_params=additional_params)
        	new_user.save()
        	return JsonResponse({'message': 'success'},status=200)
        except Exception as e:
        	print(str(e))
        	return JsonResponse({"message":"Something Went Wrong :("},status=500)

    else:
        csrf_token = get_token(request)
        context = {'csrf_token': csrf_token}
        template = loader.get_template('signup.html')
        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template)

