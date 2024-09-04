import math
from django.http import JsonResponse
from django.shortcuts import render
from guest.models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from datetime import datetime
import calendar

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
                employeeleaveModel = EmployeeLeave()
                leavestatusMonthly = LeavePolicyMonthly.objects.last()
                leavestatusYearly = LeavePolicyYearly.objects.last()
                thisMonth = datetime.now().month
                thisYear = datetime.now().year
                employeeleaveModel.employee = employeeId
                employeeleaveModel.casual_leaves_monthly = leavestatusMonthly.casual_leaves
                employeeleaveModel.casual_leaves_yr = leavestatusYearly.casual_leaves
                employeeleaveModel.sick_leaves_monthly = leavestatusMonthly.sick_leaves
                employeeleaveModel.sick_leaves_yr = leavestatusYearly.sick_leaves
                employeeleaveModel.half_day_leaves_monthly = leavestatusMonthly.half_day_leaves
                employeeleaveModel.half_day_leaves_yr = leavestatusYearly.half_day_leaves
                employeeleaveModel.for_year = thisYear
                employeeleaveModel.for_month = Month.objects.get(month_id=thisMonth)
                employeeleaveModel.excess_leave = 0
                employeeleaveModel.save()
                return JsonResponse({"success":True},status=201)
            except Employees.DoesNotExist:
                return JsonResponse({"error": "Employee not found"}, status=404)
            except Login.DoesNotExist:
                return JsonResponse({"error": "Login information not found"}, status=404)
            except LeavePolicyMonthly.DoesNotExist:
                return JsonResponse({"error": "Monthly leave policy not found"}, status=404)
            except LeavePolicyYearly.DoesNotExist:
                return JsonResponse({"error": "Yearly leave policy not found"}, status=404)
            except Month.DoesNotExist:
                return JsonResponse({"error": "Month not found"}, status=404)
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
        date_today = date.today()
        print(bonus_month)
        try:
            bonusModel = Bonus()
            bonusModel.employee = Employees.objects.get(employee_id=employee)
            bonusModel.bonus_amount = amount
            bonusModel.bonus_reason = reason
            bonusModel.bonus_month = Month.objects.get(month_id=bonus_month)
            bonusModel.added_on = date_today
            bonusModel.status = Status.objects.get(status_id=1)
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
        date_today = date.today()
        try:
            reductionModel=Reduction()
            reductionModel.employee = Employees.objects.get(employee_id=employee)
            reductionModel.reduction_amount = amount
            reductionModel.reduction_reason = reason
            reductionModel.reduction_month = Month.objects.get(month_id=reduction_month)
            reductionModel.added_on = date_today
            reductionModel.status = Status.objects.get(status_id=1)
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
        
def salary(request,id=0):
    if request.method =="GET":
        try:
            thisMonth = datetime.now().month
            thisYear = datetime.now().year
            salaryMonth = int(thisMonth)-1
            numDays = calendar.monthrange(thisYear,salaryMonth)
            daysperMonth = numDays[1]
            getEmployee = Employees.objects.all()   
            for employee in getEmployee:
                if employeeSalary.objects.filter(employee=employee.employee_id,salary_month=salaryMonth).exists():
                    None
                else:
                    payperDay = int(employee.base_package)/int(daysperMonth)
                    bonusModel = Bonus.objects.filter(employee=employee,bonus_month=salaryMonth)
                    reductionModel = Reduction.objects.filter(employee=employee,reduction_month=salaryMonth)
                    
                    

                    totalBonus = sum(bonus.bonus_amount for bonus in bonusModel)
                    totalReduction = sum(reduction.reduction_amount for reduction in reductionModel)
                    try:
                        employeeleaveModel = EmployeeLeave.objects.get(employee=employee,for_month=salaryMonth)
                        leaveReduction = int(employeeleaveModel.excess_leave)*int(payperDay)
                    except EmployeeLeave.DoesNotExist:
                        leaveReduction = 0
                    print(totalReduction)
                    totalSalary = int(employee.base_package)+int(totalBonus)-int(totalReduction)-int(leaveReduction)
                    salaryModel = employeeSalary()
                    salaryModel.employee = Employees.objects.get(employee_id=employee.employee_id)
                    salaryModel.base_package = employee.base_package
                    salaryModel.salary_month = Month.objects.get(month_id = salaryMonth)
                    salaryModel.total_bonus = totalBonus
                    salaryModel.total_reduction = totalReduction
                    
                    salaryModel.leave_reductions = leaveReduction
                    salaryModel.generated_salary = math.floor(totalSalary)
                    salaryModel.status = Status.objects.get(status_id=1)
                    salaryModel.save()
                    return JsonResponse({"success":True},status=201)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
        
def viewsalary(request):
    if request.method == "GET":
        try:
            salaryDetails = employeeSalary.objects.all()
            serializer = salarySerializer(salaryDetails,many=True)
            return JsonResponse(serializer.data,safe=False,status=200)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
    
# def generatesalary(request):

        
            
            
        

        
    
                
        
        
        