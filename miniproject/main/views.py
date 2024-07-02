from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.template import loader
from django.middleware.csrf import get_token
from django.contrib.auth.hashers import make_password, check_password
import time
from . import Graph


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())  
