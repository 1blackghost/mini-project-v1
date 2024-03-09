"""
URL configuration for miniproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import authen_view,cart_view,nav_view,payment_view

urlpatterns = [
    path("",authen_view.index,name="index"),
    path("login/",authen_view.login,name="login"),
    path("signup/",authen_view.signup,name="signup"),
    path("dash",payment_view.dash,name="dash"),
    path("logout",authen_view.logout,name="logout"),
    path("unverified",authen_view.unverified,name="unverified"),
    path("resend",authen_view.resend,name="resend"),
    path("verify/<str:hash_value>",authen_view.verify,name="verify"),
    path("cart/<str:value>/<int:qu>",cart_view.cart,name="cart"),
    path("delete/<str:value>",cart_view.delete,name="delete"),
    path("getCart",cart_view.get_cart,name="get_cart"),
    path("nav/<str:start>/<str:destination>",nav_view.nav,name="nav"),
    path("test",nav_view.testing,name="test"),
    path('paymenthandler/', payment_view.paymenthandler, name='paymenthandler'),
    path("getAmount",payment_view.getAmount,name="getAmount"),
]
