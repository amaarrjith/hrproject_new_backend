from django.http import JsonResponse
from django.shortcuts import render
from guest.models import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def login(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            if Login.objects.filter(username=username,password=password).exists():
                return JsonResponse({"success":True},status=200)
            if Admin.objects.filter(username=username,password=password).exists():
                return JsonResponse({"admin":True},status=200)
            else:
                return JsonResponse({"error":"Invalid"},status=401)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
    else:
        return JsonResponse({"error":"Invalid Request"},status=405)