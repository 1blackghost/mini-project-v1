from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.template import loader
from django.http import JsonResponse
from .models import ProductDB ,Admin
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.template import loader
from django.middleware.csrf import get_token
from .models import Admin
from django.contrib.auth.hashers import make_password, check_password
import time
from . import helper

        

def submit_data(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        price = request.POST.get('price')
        code = request.POST.get('code')
        
        try:
            existing_product = ProductDB.objects.get(code=code)
            existing_product.name = name
            existing_product.quantity = quantity
            existing_product.category = category
            existing_product.price = price
            existing_product.save()
            return JsonResponse({'success': True})
        except ProductDB.DoesNotExist:
            new_product = ProductDB(name=name, quantity=quantity, category=category, price=price, code=code)
            new_product.save()
            return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)




def adminPanel(request):
    if request.session.has_key("admin"):
        template = loader.get_template('adminpanel.html')
        return HttpResponse(template.render())  
    else:
        return HttpResponse("Unauthorised! 403 forbidden.")


def adminL(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Admin.objects.get(email=email)
            if check_password(password, user.password):
                request.session["admin"] = user
                return JsonResponse({"message": "success"}, status=200)
    
            else:
                return JsonResponse({"message": "Incorrect password"}, status=401)
        except Admin.DoesNotExist:
            return JsonResponse({"message": "Admin does not exist"}, status=404)
        except Exception as e:
            print(str(e))
            return JsonResponse({"message": "Something went wrong:("}, status=500)

    else:
        csrf_token = get_token(request)
        context = {'csrf_token': csrf_token}
        template = loader.get_template('admin_login.html')
        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template)