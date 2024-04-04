from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.template import loader
from django.middleware.csrf import get_token
from .models import User
from django.contrib.auth.hashers import make_password, check_password
import time
from .models import Verify_Email,Cart,CartItem
from . import Graph


def addItem(request):
    user=request.get("user")
    cart = Cart.objects.get_or_create(user=user)
    cart.save()

def nav(request,start,destination):
    start=start.lower()
    destination=destination.lower()
    navigator = Graph.MallNavigator()
    navigator.create_connections()
    path = navigator.find_path(start, destination)
    average_time = navigator.calculate_average_time(start, destination, average_speed=1.5)

    return JsonResponse({"message":"ok","path":path,"average_time":average_time})

def testing(request):
    template = loader.get_template('test.html')
    return HttpResponse(template.render())  