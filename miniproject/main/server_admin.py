from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from .models import Admin

def add(request, username, password):
    try:
        admin, created = Admin.objects.get_or_create(email=username)
        admin.password = make_password(password)
        admin.save()
        return JsonResponse({"status": "ok", "message": "Password updated successfully."})
    except Exception as e:
        return JsonResponse({"status": "bad", "error": str(e)})
