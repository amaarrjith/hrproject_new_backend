import math
from django.http import JsonResponse
from django.shortcuts import render
from guest.models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timezone
from datetime import datetime
import calendar
from django.db.models import Sum

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
                if Login.objects.filter(username=employee_id).exists():
                    return JsonResponse({"Done":True},status=200)
                else:
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
                if Login.objects.filter(username=employee_id).exists():
                    return JsonResponse({"Done":True},status=200)
                else:
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
                    thisMonth = datetime.now().month
                    thisYear = datetime.now().year
                    employeeleaveModel.employee = employeeId
                    employeeleaveModel.casual_leaves_monthly = 0
                    employeeleaveModel.casual_leaves_yr = 0
                    employeeleaveModel.sick_leaves_monthly = 0
                    employeeleaveModel.sick_leaves_yr = 0
                    employeeleaveModel.half_day_leaves_monthly = 0
                    employeeleaveModel.half_day_leaves_yr = 0
                    employeeleaveModel.for_year = thisYear
                    employeeleaveModel.for_month = Month.objects.get(month_id=thisMonth)
                    employeeleaveModel.excess_leave_yrsl = 0
                    employeeleaveModel.excess_leave_yrhalf = 0
                    employeeleaveModel.excess_leave_yrcl = 0
                    employeeleaveModel.excess_leave_monthsl = 0
                    employeeleaveModel.excess_leave_monthcl = 0
                    employeeleaveModel.excess_leave_monthhalf = 0
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
        
def salary(request):
    if request.method == "GET":
        
            thisMonth = datetime.now().month
            thisYear = datetime.now().year
            salaryMonth = thisMonth - 1  # Previous month
            numDays = calendar.monthrange(thisYear, salaryMonth)
            daysperMonth = numDays[1]

            employees = Employees.objects.all()

            for employee in employees:
                salary_exists = employeeSalary.objects.filter(employee=employee.employee_id, salary_month=salaryMonth).exists()
                
                if not salary_exists:
                    payperDay = int(employee.base_package) / int(daysperMonth)
                    bonuses = Bonus.objects.filter(employee=employee, bonus_month=salaryMonth)
                    totalBonus = sum(bonus.bonus_amount for bonus in bonuses)
                    reductions = Reduction.objects.filter(employee=employee, reduction_month=salaryMonth)
                    totalReduction = sum(reduction.reduction_amount for reduction in reductions)
                    try:
                        employee_leave = EmployeeLeave.objects.get(employee=employee, for_month=salaryMonth)
                        excess_leave = int(employee_leave.excess_leave_monthcl)+int(employee_leave.excess_leave_monthhalf)+int(employee_leave.excess_leave_monthsl)+int(employee_leave.excess_leave_yrcl)+int(employee_leave.excess_leave_yrhalf)+int(employee_leave.excess_leave_yrsl)
                        leave_reduction = int(excess_leave) * int(payperDay)
                    except EmployeeLeave.DoesNotExist:
                        leave_reduction = 0

                    total_salary = int(employee.base_package) + int(totalBonus) - int(totalReduction) - int(leave_reduction)
                    
                    salary_model = employeeSalary()
                    salary_model.employee = Employees.objects.get(employee_id=employee.employee_id)
                    salary_model.base_package = employee.base_package
                    salary_model.salary_month = Month.objects.get(month_id=salaryMonth)
                    salary_model.total_bonus = totalBonus
                    salary_model.total_reduction = totalReduction
                    salary_model.leave_reductions = leave_reduction
                    salary_model.generated_salary = math.floor(total_salary)
                    salary_model.status = Status.objects.get(status_id=1)
                    salary_model.save()

            return JsonResponse({"success": True}, status=201)

        
        
def viewsalary(request):
    if request.method == "GET":
        try:
            salaryDetails = employeeSalary.objects.all()
            serializer = salarySerializer(salaryDetails,many=True)
            
            return JsonResponse(serializer.data,safe=False,status=200)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
    
def generatesalary(request,id=0):
    if request.method =="GET":
        if id:
            try:
                employeesalaryModel = employeeSalary.objects.get(employee=id)
                employeesalaryModel.status = Status.objects.get(status_id=2)
                employeesalaryModel.save()
                return JsonResponse({"success":True},status=200)
            except employeeSalary.DoesNotExist:
                return JsonResponse({"error":"Does Not Exists"},status=404)
            except Exception as e:
                return JsonResponse({"error":str(e)},status=500)
        else:
            try:
                employeesalaryAll = employeeSalary.objects.all()
                for employee in employeesalaryAll:
                    employee.status = Status.objects.get(status_id=2)
                    employee.save()
                    continue
                return JsonResponse({"success":True},status=200)
            except Exception as e:
                return JsonResponse({"error":str(e)},status=500)

def leaveRequest(request,id=0):
    if request.method == "POST":
        employee_id = id
        leaveDate = request.POST.get('date')
        leaveReason = request.POST.get('reason')
        try:
            leaveModel = leaveRequests()
            leaveModel.employee = Employees.objects.get(employee_id=employee_id)
            leaveModel.leave_date = leaveDate
            leaveModel.reason = leavetype.objects.get(leave_id=leaveReason)
            leaveModel.status = Status.objects.get(status_id=3)
            leaveModel.save()
        except Employees.DoesNotExist:
            return JsonResponse({"error":"Does Not Exists"},status=404)
        except Exception as e:
            return JsonResponse({"error":str(e)})
        return JsonResponse({"success":True},status=200)
    
    elif request.method == "GET":
        try:
            getallRequests = leaveRequests.objects.select_related('employee','status','reason').all()
            serializer = leaverequestsSerializer(getallRequests,many=True)
            return JsonResponse(serializer.data,safe=False,status=200)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
        
def approveLeave(request,id=0,leaveid=0):
    if request.method == "GET":
        try:
            print(id)
            print(leaveid)
            leavereqModel = leaveRequests.objects.get(leave_id=leaveid)
            leavereqModel.status = Status.objects.get(status_id=4)
            leavereqModel.save()
            employeeLeave = EmployeeLeave.objects.get(employee_id=id)
            policyYear = LeavePolicyYearly.objects.last()
            clYear = policyYear.casual_leaves
            slYear = policyYear.sick_leaves
            hlYear = policyYear.half_day_leaves
            policyMonth = LeavePolicyMonthly.objects.last()
            clMonth = policyMonth.casual_leaves
            slMonth = policyMonth.sick_leaves
            hlMonth = policyMonth.half_day_leaves
            if leavereqModel.reason == leavetype.objects.get(leave_id=1):
                employeeLeave.casual_leaves_monthly += 1
                employeeLeave.casual_leaves_yr += 1
                employeeLeave.save()
                if employeeLeave.casual_leaves_monthly > clMonth:
                    employeeLeave.excess_leave_monthcl = int(employeeLeave.casual_leaves_monthly)-int(clMonth)
                    employeeLeave.save()
                if employeeLeave.casual_leaves_yr > clYear:
                    employeeLeave.excess_leave_yrcl = int(employeeLeave.casual_leaves_yr)-int(clYear)
                    employeeLeave.save()
                return JsonResponse({"suceess":True},status=200)
            
            elif leavereqModel.reason == leavetype.objects.get(leave_id=2):
                employeeLeave.sick_leaves_monthly += 1
                employeeLeave.sick_leaves_yr += 1
                employeeLeave.save()
                if employeeLeave.sick_leaves_monthly > slMonth:
                    employeeLeave.excess_leave_monthsl = int(employeeLeave.sick_leaves_monthly)-int(slMonth)
                    employeeLeave.save()
                if employeeLeave.sick_leaves_yr > slYear:
                    employeeLeave.excess_leave_yrcl = int(employeeLeave.sick_leaves_yr)-int(slYear)
                    employeeLeave.save()
                return JsonResponse({"suceess":True},status=200)
            
            elif leavereqModel.reason == leavetype.objects.get(leave_id=3):
                employeeLeave.half_day_leaves_monthly += 1
                employeeLeave.half_day_leaves_yr += 1
                employeeLeave.save()
                if employeeLeave.half_day_leaves_monthly > hlMonth:
                    employeeLeave.excess_leave_monthhalf = int(employeeLeave.half_day_leaves_monthly)-int(hlMonth)
                    employeeLeave.save()
                if employeeLeave.half_day_leaves_yr > hlYear:
                    employeeLeave.excess_leave_yrhalf = int(employeeLeave.half_day_leaves_yr)-int(hlYear)
                    employeeLeave.save()
                return JsonResponse({"suceess":True},status=200)
            else:
                return JsonResponse({"error":"Reason Not Found"})
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
        
def declineLeave(request,id=0):
    if request.method == "GET":
        try:
            leavereqModel = leaveRequests.objects.get(employee_id=id)
            leavereqModel.status = Status.objects.get(status_id=5)
            leavereqModel.save()
            return JsonResponse({"suceess":True},status=200)
        except leaveRequests.DoesNotExist:
            return JsonResponse({"error":"Not Found"},status=404)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)

@csrf_exempt
def leaveStatus(request):
    if request.method == "GET":
        try:
            leavestatusMonthModel = LeavePolicyMonthly.objects.all()
            leavestatusYearModel = LeavePolicyYearly.objects.all()
            monthserializer = leavestatusMonthlySerializer(leavestatusMonthModel,many=True)
            yearserializer = leavestatusYearlySerializer(leavestatusYearModel,many=True)
            response = {
                'month':monthserializer.data,
                'year':yearserializer.data
            }
            return JsonResponse(response,safe=False,status=200)
        except Exception as e:
            return JsonResponse({"error":str(e)})
    elif request.method == "POST":
        casualYr = request.POST.get('casualyr')
        sickYr = request.POST.get('sickyr')
        halfYr = request.POST.get('halfyr')
        casualMonth = request.POST.get('casualmonth')
        sickMonth = request.POST.get('sickmonth')
        halfMonth = request.POST.get('halfmonth')
        try : 
            policyYear = LeavePolicyYearly.objects.last()
            policyYear.casual_leaves = casualYr
            policyYear.sick_leaves = sickYr
            policyYear.half_day_leaves = halfYr
            policyYear.save()
            policyMonth = LeavePolicyMonthly.objects.last()
            policyMonth.casual_leaves = casualMonth
            policyMonth.sick_leaves = sickMonth
            policyMonth.half_day_leaves = halfMonth
            policyMonth.save()
            return JsonResponse({"success":True},status=200)
        except LeavePolicyYearly.DoesNotExist:
            return JsonResponse({"error":"Year Policy Does Not EXists"},status=404)
        except LeavePolicyMonthly.DoesNotExist:
            return JsonResponse({"error":"Month Policy Does Not Exists"},status=404)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
    
@csrf_exempt
def generatesalarymonth(request):
    if request.method == "POST":
        employee_id = request.POST.get('id')
        thisMonth = datetime.now().month
        thisYear = datetime.now().year
        today = datetime.now()
        salaryMonth = thisMonth 
        numDays = calendar.monthrange(thisYear, salaryMonth)
        daysperMonth = numDays[1]
        employees = Employees.objects.get(employee_id=employee_id)
        salaryModel = employeeSalary()
        salaryModel.employee = employees
        payperDay = int(employees.base_package) / int(daysperMonth)
        workingDays = today.day
        amountThismonth = payperDay * workingDays
        bonuses = Bonus.objects.filter(employee=employee_id, bonus_month=salaryMonth)
        totalBonus = sum(bonus.bonus_amount for bonus in bonuses)
        reductions = Reduction.objects.filter(employee=employee_id, reduction_month=salaryMonth)
        totalReduction = sum(reduction.reduction_amount for reduction in reductions)
        try:
            employee_leave = EmployeeLeave.objects.get(employee=employee_id, for_month=salaryMonth)
            excess_leave = int(employee_leave.excess_leave_monthcl)+int(employee_leave.excess_leave_monthhalf)+int(employee_leave.excess_leave_monthsl)+int(employee_leave.excess_leave_yrcl)+int(employee_leave.excess_leave_yrhalf)+int(employee_leave.excess_leave_yrsl)
            leave_reduction = int(excess_leave) * int(payperDay)
        except EmployeeLeave.DoesNotExist:
            leave_reduction = 0

        total_salary = int(amountThismonth) + int(totalBonus) - int(totalReduction) - int(leave_reduction)
        
        salary_model = employeeSalary()
        salary_model.employee = Employees.objects.get(employee_id=employees.employee_id)
        salary_model.base_package = amountThismonth
        salary_model.salary_month = Month.objects.get(month_id=salaryMonth)
        salary_model.total_bonus = totalBonus
        salary_model.total_reduction = totalReduction
        salary_model.leave_reductions = leave_reduction
        salary_model.generated_salary = math.floor(total_salary)
        salary_model.status = Status.objects.get(status_id=2)
        salary_model.save()
        return JsonResponse({"success":True},status=200)

        
        
        
            
            
            
            
            
        
        
            
            
        

        
    
                
        
        
        