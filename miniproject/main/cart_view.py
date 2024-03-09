from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.template import loader
from django.middleware.csrf import get_token
from .models import User
from django.contrib.auth.hashers import make_password, check_password
import time
from .models import Verify_Email,Cart,CartItem


def get_cart(request):
    user = request.session.get("user")
    try:
        cart_items = CartItem.objects.filter(cart__user=user)
        cart_data = [{'item': item.item, 'quantity': item.quantity,"price":item.price} for item in cart_items]
        return JsonResponse({'cart': cart_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def cart(request, value, qu):
    user = request.session.get("user")
    try:
        cart, created = Cart.objects.get_or_create(user=user)
        value=value.lower()
        qu = int(qu)
        
        if qu > 0:
            array={"apple":10,"orange":10,"book":30,"cookies":10}
            p = qu * array.get(value, 0)
            cart.add_item(item_name=value, quantity=qu, price=p)
            cart.save()
            if created:
                return JsonResponse({"status": "ok", "message": "Item added to cart."}, status=200)
            else:
                return JsonResponse({"status": "ok", "message": "Item quantity updated in cart."}, status=200)
        else:
            return JsonResponse({"status": "bad", "error": "Invalid quantity. Quantity must be greater than 0."}, status=400)
    except ValueError:
        return JsonResponse({"status": "bad", "error": "Invalid quantity format. Please provide a valid integer."}, status=400)
    except Exception as e:
        return JsonResponse({"status": "bad", "error": str(e)}, status=500)



def delete(request, value):
    try:
        user = request.session.get("user")
        cart, created = Cart.objects.get_or_create(user=user)
        cart.remove_item(item_name=value)
        cart.save()
        return JsonResponse({"status": "ok"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "bad"}, status=500)