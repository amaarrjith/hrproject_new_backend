from django.http import JsonResponse
from django.shortcuts import render
from guest.models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from datetime import datetime

from guest.serializers import *
# Create your views here.

@csrf_exempt
def login(request,id=0):
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
    elif request.method == "GET":
        try:
            if id:
                loginDetails = Login.objects.select_related('employee').filter(employee_id=id)
                serializer = loginSerializers(loginDetails,many=True)
                return JsonResponse(serializer.data,safe=False,status=200)
            else:
                return JsonResponse({"error":"ID Not Found"},status=404)
        except Login.DoesNotExist:
            return JsonResponse({"error":"Does Not Exists"},status=404)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
    
    else:
        return JsonResponse({"error":"Invalid Request"},status=405)
    
@csrf_exempt
def employees(request,id=0):
    if request.method == "POST":
        employee_name = request.POST.get('name')
        employee_mail = request.POST.get('mail')
        employee_post = request.POST.get('post')
        employee_basepackage = request.POST.get('pay')
        employee_id = request.POST.get('id')
        employee_password = request.POST.get('password')
        if id:
            try:
                getEmployee = Employees.objects.get(employee_id=id)
                getEmployee.employee_name = employee_name
                getEmployee.employee_mail=employee_mail
                getEmployee.post = employee_post
                getEmployee.base_package = employee_basepackage
                getEmployee.save()
                getLogin = Login.objects.get(employee_id=id)
                getLogin.username = employee_id
                getLogin.password = employee_password
                getLogin.save()
                return JsonResponse({"success":True},status=200)
            except Employees.DoesNotExist:
                return JsonResponse({"error":"Employees Doesn't Exists"},status=404)
            except Login.DoesNotExist:
                return JsonResponse({"error":"Login Doesn't Exists"},status=404)
            except Exception as e:
                return JsonResponse({"error":str(e)},status=500)
        else:
            try:
                employeeModel = Employees()
                dateToday = date.today()
                employeeModel.employee_name = employee_name
                employeeModel.employee_mail = employee_mail
                employeeModel.post = employee_post
                employeeModel.base_package = employee_basepackage
                employeeModel.registered_date = dateToday
                employeeModel.save()
                employeeId = Employees.objects.last()
                loginModel = Login()
                loginModel.employee = employeeId
                loginModel.username = employee_id
                loginModel.password = employee_password
                loginModel.save()
                return JsonResponse({"success":True},status=201)
            except Exception as e:
                return JsonResponse ({"error":str(e)},status=500)
    elif request.method == "GET":
        if id:
            try:
                getEmployee=Employees.objects.get(employee_id=id)
                serializer = employeeSerializers(getEmployee)
                return JsonResponse(serializer.data,safe=False,status=200)
            except Employees.DoesNotExist:
                return JsonResponse({"error":"Not Found"},status=404)
            except Exception as e:
                return JsonResponse({"error":str(e)},status=500)
        else:
            try:
                getAllEmployees = Employees.objects.all()
                serializer = employeeSerializers(getAllEmployees,many=True)
                return JsonResponse(serializer.data,safe=False,status=200)
            except Exception as e:
                return JsonResponse({"error":str(e)},status=500)
    elif request.method == "DELETE":
        try:
            getEmployee = Employees.objects.get(employee_id=id)
            getEmployee.delete()
            return JsonResponse({"success":True},status=200)
        except Employees.DoesNotExist:
            return JsonResponse({"error":"Not Found"},status=404)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
    else:
        return JsonResponse({"error":"Invalid Method"},status=405)
    
@csrf_exempt
def bonus(request,id=0):
    if request.method == "POST":
        employee = request.POST.get('employee')
        amount = request.POST.get('amount')
        reason = request.POST.get('reason')
        bonus_month = datetime.now().month
        print(bonus_month)
        try:
            bonusModel = Bonus()
            bonusModel.employee = Employees.objects.get(employee_id=employee)
            bonusModel.bonus_amount = amount
            bonusModel.bonus_reason = reason
            bonusModel.bonus_month = Month.objects.get(month_id=bonus_month)
            bonusModel.save()
            return JsonResponse({"success":True},status=201)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
    elif request.method == "GET":
        try:
            bonusDetails = Bonus.objects.select_related('bonus_month','employee','status').all()
            serializers = bonusSerializers(bonusDetails,many=True)
            return JsonResponse(serializers.data,safe=False,status=200)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
        
    else:
        return JsonResponse({"error":"Invalid Method"},status=500)
    
@csrf_exempt
def reduction(request,id=0):
    if request.method == "POST":
        employee = request.POST.get('employee')
        amount = request.POST.get('amount')
        reason = request.POST.get('reason')
        reduction_month = datetime.now().month
        try:
            reductionModel=Reduction()
            reductionModel.employee = Employees.objects.get(employee_id=employee)
            reductionModel.reduction_amount = amount
            reductionModel.reduction_reason = reason
            reductionModel.reduction_month = Month.objects.get(month_id=reduction_month)
            reductionModel.save()
            return JsonResponse({"success":True},status=200)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
    elif request.method == "GET":
        try:
            reductionDetails = Reduction.objects.select_related('reduction_month','employee','status').all()
            serializer = reductionSerializers(reductionDetails,many=True)
            return JsonResponse(serializer.data,safe=False,status=200)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
        
        
    
                
        
        
        