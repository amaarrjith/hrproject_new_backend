import math
import random
from django.http import JsonResponse
from guest.models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from datetime import datetime
import calendar
from django.core.mail import send_mail
from guest.serializers import *

# Create your views here.


@csrf_exempt
def login(request, id=0):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            if Login.objects.filter(username=username, password=password).exists():
                employeeDetails = Login.objects.get(username=username)
                employeeID = employeeDetails.employee.employee_id
                return JsonResponse(
                    {"success": True, "employeeID": employeeID}, status=200
                )
            elif Admin.objects.filter(username=username, password=password).exists():
                return JsonResponse({"admin": True}, status=200)
            else:
                return JsonResponse({"failure": True}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == "GET":
        try:
            if id:
                loginDetails = Login.objects.select_related("employee").filter(
                    employee_id=id
                )
                serializer = loginSerializers(loginDetails, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
            else:
                return JsonResponse({"error": "ID Not Found"}, status=404)
        except Login.DoesNotExist:
            return JsonResponse({"error": "Does Not Exists"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error":"Invalid Method"},status=405)


@csrf_exempt
def employees(request, id=0):
    if request.method == "POST":
        employee_name = request.POST.get("name")
        employee_mail = request.POST.get("mail")
        employee_post = request.POST.get("post")
        employee_basepackage = request.POST.get("pay")
        employee_id = request.POST.get("id")
        employee_password = request.POST.get("password")
        if id:
            try:
                if Login.objects.filter(username=employee_id).exists():
                    return JsonResponse({"Done": True}, status=200)
                else:
                    getEmployee = Employees.objects.get(employee_id=id)
                    getEmployee.employee_name = employee_name
                    getEmployee.employee_mail = employee_mail
                    getEmployee.post = employee_post
                    getEmployee.base_package = employee_basepackage
                    getEmployee.save()
                    getLogin = Login.objects.get(employee_id=id)
                    getLogin.username = employee_id
                    getLogin.password = employee_password
                    getLogin.save()
                return JsonResponse({"success": True}, status=200)
            except Employees.DoesNotExist:
                return JsonResponse({"error": "Employees Doesn't Exists"}, status=404)
            except Login.DoesNotExist:
                return JsonResponse({"error": "Login Doesn't Exists"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            try:
                if Login.objects.filter(username=employee_id).exists():
                    return JsonResponse({"Done": True}, status=200)
                else:
                    employeeModel = Employees()
                    dateToday = date.today()
                    employeeModel.employee_name = employee_name
                    employeeModel.employee_mail = employee_mail
                    employeeModel.post = employee_post
                    employeeModel.base_package = employee_basepackage
                    employeeModel.registered_date = dateToday
                    employeeModel.status = Status.objects.get(status_id=6)
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
                    return JsonResponse({"success": True}, status=201)
            except Employees.DoesNotExist:
                return JsonResponse({"error": "Employee not found"}, status=404)
            except Login.DoesNotExist:
                return JsonResponse(
                    {"error": "Login information not found"}, status=404
                )
            except LeavePolicyMonthly.DoesNotExist:
                return JsonResponse(
                    {"error": "Monthly leave policy not found"}, status=404
                )
            except LeavePolicyYearly.DoesNotExist:
                return JsonResponse(
                    {"error": "Yearly leave policy not found"}, status=404
                )
            except Month.DoesNotExist:
                return JsonResponse({"error": "Month not found"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    elif request.method == "GET":
        if id:
            try:
                getEmployee = Employees.objects.get(employee_id=id)
                serializer = employeeSerializers(getEmployee)
                return JsonResponse(serializer.data, safe=False, status=200)
            except Employees.DoesNotExist:
                return JsonResponse({"error": "Not Found"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            try:
                getAllEmployees = Employees.objects.all()
                serializer = employeeSerializers(getAllEmployees, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    elif request.method == "DELETE":
        try:
            getEmployee = Employees.objects.get(employee_id=id)
            getEmployee.delete()
            return JsonResponse({"success": True}, status=200)
        except Employees.DoesNotExist:
            return JsonResponse({"error": "Not Found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error":"Invalid Method"},status=405)


@csrf_exempt
def bonus(request, id=0):
    if request.method == "POST":
        employee = request.POST.get("employee")
        amount = request.POST.get("amount")
        reason = request.POST.get("reason")
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
            return JsonResponse({"success": True}, status=201)
        except Employees.DoesNotExist:
            return JsonResponse({"error": "Employee Not Found"}, status=404)
        except Month.DoesNotExist:
            return JsonResponse({"error": "Month Not Found"}, status=404)
        except Status.DoesNotExist:
            return JsonResponse({"error": "Status Not Found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == "GET":
        if id:
            try:
                bonusDetails = Bonus.objects.select_related(
                    "bonus_month", "employee", "status"
                ).filter(employee_id=id)
                serializers = bonusSerializers(bonusDetails, many=True)
                return JsonResponse(serializers.data, safe=False, status=200)
            except Bonus.DoesNotExist:
                return JsonResponse({"error": "Bonus Details Not Found"})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            try:
                bonusDetails = Bonus.objects.select_related(
                    "bonus_month", "employee", "status"
                ).all()
                serializers = bonusSerializers(bonusDetails, many=True)
                return JsonResponse(serializers.data, safe=False, status=200)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error":"Invalid Method"},status=405)


@csrf_exempt
def reduction(request, id=0):
    if request.method == "POST":
        employee = request.POST.get("employee")
        amount = request.POST.get("amount")
        reason = request.POST.get("reason")
        reduction_month = datetime.now().month
        date_today = date.today()
        try:
            reductionModel = Reduction()
            reductionModel.employee = Employees.objects.get(employee_id=employee)
            reductionModel.reduction_amount = amount
            reductionModel.reduction_reason = reason
            reductionModel.reduction_month = Month.objects.get(month_id=reduction_month)
            reductionModel.added_on = date_today
            reductionModel.status = Status.objects.get(status_id=1)
            reductionModel.save()
            return JsonResponse({"success": True}, status=200)
        except Employees.DoesNotExist:
            return JsonResponse({"error": "Employee Not Found"}, status=404)
        except Month.DoesNotExist:
            return JsonResponse({"error": "Month Not Found"}, status=404)
        except Status.DoesNotExist:
            return JsonResponse({"error": "Status Not Found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == "GET":
        if id:
            try:
                reductionDetails = Reduction.objects.select_related(
                    "reduction_month", "employee", "status"
                ).filter(employee_id=id)
                serializer = reductionSerializers(reductionDetails, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
            except Reduction.DoesNotExist:
                return JsonResponse({"error": "Reduction Details Not Found"})
        else:
            try:
                reductionDetails = Reduction.objects.select_related(
                    "reduction_month", "employee", "status"
                ).all()
                serializer = reductionSerializers(reductionDetails, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error":"Invalid Method"},status=405)


def salary(request):
    if request.method == "GET":

        thisMonth = datetime.now().month
        thisYear = datetime.now().year
        if thisMonth == 1:
            salaryMonth = 12
            thisYear = thisYear - 1
        else:
            salaryMonth = thisMonth - 1

        numDays = calendar.monthrange(thisYear, salaryMonth)
        daysperMonth = numDays[1]
        employees = Employees.objects.all()

        for employee in employees:
            try:
                salary_exists = employeeSalary.objects.filter(
                    employee=employee.employee_id, salary_month=salaryMonth
                ).exists()

                if not salary_exists:
                    payperDay = int(employee.base_package) / int(daysperMonth)
                    bonuses = Bonus.objects.filter(
                        employee=employee, bonus_month=salaryMonth
                    )
                    totalBonus = sum(bonus.bonus_amount for bonus in bonuses)
                    reductions = Reduction.objects.filter(
                        employee=employee, reduction_month=salaryMonth
                    )
                    totalReduction = sum(
                        reduction.reduction_amount for reduction in reductions
                    )
                    try:
                        employee_leave = EmployeeLeave.objects.get(
                            employee=employee, for_month=salaryMonth
                        )
                        excess_leave = (
                            int(employee_leave.excess_leave_monthcl)
                            + int(employee_leave.excess_leave_monthhalf)
                            + int(employee_leave.excess_leave_monthsl)
                            + int(employee_leave.excess_leave_yrcl)
                            + int(employee_leave.excess_leave_yrhalf)
                            + int(employee_leave.excess_leave_yrsl)
                        )
                        leave_reduction = int(excess_leave) * int(payperDay)
                    except EmployeeLeave.DoesNotExist:
                        leave_reduction = 0

                    total_salary = (
                        int(employee.base_package)
                        + int(totalBonus)
                        - int(totalReduction)
                        - int(leave_reduction)
                    )

                    salary_model = employeeSalary()
                    salary_model.employee = Employees.objects.get(
                        employee_id=employee.employee_id
                    )
                    salary_model.base_package = employee.base_package
                    salary_model.salary_month = Month.objects.get(month_id=salaryMonth)
                    salary_model.total_bonus = totalBonus
                    salary_model.total_reduction = totalReduction
                    salary_model.leave_reductions = leave_reduction
                    salary_model.generated_salary = math.floor(total_salary)
                    salary_model.status = Status.objects.get(status_id=1)
                    salary_model.save()
                    bonusModel = Bonus.objects.filter(
                        employee=employee, bonus_month=salaryMonth
                    )
                    for bonus in bonusModel:
                        bonus.status = 2
                        bonus.save()
                    reductionModel = Reduction.objects.filter(
                        employee=employee, reduction_month=salaryMonth
                    )
                    for reduction in reductionModel:
                        reduction.status = 2
                        reduction.save()
                return JsonResponse({"success": True}, status=201)
            except employeeSalary.DoesNotExist:
                return JsonResponse({"error":"Salary Details Not Found"},status=404)
            except Bonus.DoesNotExist:
                return JsonResponse({"error":"Bonus Details Not Found"},status=404)
            except Reduction.DoesNotExist:
                return JsonResponse({"error":"Reduction Details Not Found"},status=404)
            except Employees.DoesNotExist:
                return JsonResponse({"error":"Employee Details Not Found"},status=404)
            except Month.DoesNotExist:
                return JsonResponse({"error": "Month Not Found"}, status=404)
            except Status.DoesNotExist:
                return JsonResponse({"error": "Status Not Found"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error":"Invalid Method"},status=405)

            


def viewsalary(request, id=0):
    if request.method == "GET":
        if id:
            try:
                salaryDetails = employeeSalary.objects.filter(employee=id)
                serializer = salarySerializer(salaryDetails, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
            except employeeSalary.DoesNotExist:
                return JsonResponse({"error":"Salary Details Not Found"},status=404)
            except Exception as e:
                return JsonResponse({"error":str(e)})
        else:
            try:
                salaryDetails = employeeSalary.objects.all()
                serializer = salarySerializer(salaryDetails, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error":"Invalid Method"},status=405)
def generatesalary(request, id=0):
    if request.method == "GET":
        if id:
            try:
                employeesalaryModel = employeeSalary.objects.get(employee=id)
                employeesalaryModel.status = Status.objects.get(status_id=2)
                employeesalaryModel.save()
                return JsonResponse({"success": True}, status=200)
            except employeeSalary.DoesNotExist:
                return JsonResponse({"error": "Salary Does Not Exists"}, status=404)
            except Status.DoesNotExist:
                return JsonResponse({"error": "Status Does Not Exists"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            try:
                employeesalaryAll = employeeSalary.objects.all()
                for employee in employeesalaryAll:
                    employee.status = Status.objects.get(status_id=2)
                    employee.save()
                    continue
                return JsonResponse({"success": True}, status=200)
            except Status.DoesNotExist:
                return JsonResponse({"error": "Status Does Not Exists"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error":"Invalid Method"},status=405)

@csrf_exempt
def leaveRequest(request, id=0):
    if request.method == "POST":
        employee_id = id
        print(employee_id)
        leaveDate = request.POST.get("date")
        leaveReason = request.POST.get("reason")
        try:

            leaveModel = leaveRequests()
            leaveModel.employee = Employees.objects.get(employee_id=employee_id)
            leaveModel.leave_date = leaveDate
            leaveModel.reason = leavetype.objects.get(leave_id=leaveReason)
            leaveModel.status = Status.objects.get(status_id=3)
            leaveModel.save()
            return JsonResponse({"success": True}, status=200)
        except Employees.DoesNotExist:
            return JsonResponse({"error": "Employees Does Not Exists"}, status=404)
        except leavetype.DoesNotExist:
            return JsonResponse({"error": "leavetype Does Not Exists"}, status=404)
        except Status.DoesNotExist:
            return JsonResponse({"error": "Status Does Not Exists"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)})

    elif request.method == "GET":
        if id:
            try:
                getRequests = leaveRequests.objects.filter(employee=id)
                serializer = leaverequestsSerializer(getRequests, many=True)
                return JsonResponse(serializer.data, safe=False)
            except leaveRequests.DoesNotExist:
                return JsonResponse({"error": "leaveRequests Does Not Exists"}, status=404)
            except Exception as e:
                return JsonResponse({"error":str(e)},status=500)
        else:
            try:
                getallRequests = leaveRequests.objects.select_related(
                    "employee", "status", "reason"
                ).all()
                serializer = leaverequestsSerializer(getallRequests, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error":"Invalid Method"},status=405)

def approveLeave(request, id=0, leaveid=0):
    if request.method == "GET":
        try:
            leavereqModel = leaveRequests.objects.get(leave_id=leaveid)
            requested_for = leavereqModel.leave_date
            month = requested_for.month
            year = requested_for.year
            leavereqModel.status = Status.objects.get(status_id=4)
            leavereqModel.save()
            employeeLeave = EmployeeLeave.objects.get(
                employee_id=id, for_month_id=month
            )
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
                    employeeLeave.excess_leave_monthcl = int(
                        employeeLeave.casual_leaves_monthly
                    ) - int(clMonth)
                    employeeLeave.save()
                if employeeLeave.casual_leaves_yr > clYear:
                    employeeLeave.excess_leave_yrcl = int(
                        employeeLeave.casual_leaves_yr
                    ) - int(clYear)
                    employeeLeave.save()
                return JsonResponse({"suceess": True}, status=200)

            elif leavereqModel.reason == leavetype.objects.get(leave_id=2):
                employeeLeave.sick_leaves_monthly += 1
                employeeLeave.sick_leaves_yr += 1
                employeeLeave.save()
                if employeeLeave.sick_leaves_monthly > slMonth:
                    employeeLeave.excess_leave_monthsl = int(
                        employeeLeave.sick_leaves_monthly
                    ) - int(slMonth)
                    employeeLeave.save()
                if employeeLeave.sick_leaves_yr > slYear:
                    employeeLeave.excess_leave_yrcl = int(
                        employeeLeave.sick_leaves_yr
                    ) - int(slYear)
                    employeeLeave.save()
                return JsonResponse({"suceess": True}, status=200)

            elif leavereqModel.reason == leavetype.objects.get(leave_id=3):
                employeeLeave.half_day_leaves_monthly += 1
                employeeLeave.half_day_leaves_yr += 1
                employeeLeave.save()
                if employeeLeave.half_day_leaves_monthly > hlMonth:
                    employeeLeave.excess_leave_monthhalf = int(
                        employeeLeave.half_day_leaves_monthly
                    ) - int(hlMonth)
                    employeeLeave.save()
                if employeeLeave.half_day_leaves_yr > hlYear:
                    employeeLeave.excess_leave_yrhalf = int(
                        employeeLeave.half_day_leaves_yr
                    ) - int(hlYear)
                    employeeLeave.save()
                return JsonResponse({"suceess": True}, status=200)
            else:
                return JsonResponse({"error": "Reason Not Found"})

        except EmployeeLeave.DoesNotExist:
            employeeleaveModel = EmployeeLeave()
            employeeId = Employees.objects.get(employee_id=id)
            employeeleaveModel.employee = employeeId
            employeeleaveModel.casual_leaves_monthly = 0
            employeeleaveModel.casual_leaves_yr = 0
            employeeleaveModel.sick_leaves_monthly = 0
            employeeleaveModel.sick_leaves_yr = 0
            employeeleaveModel.half_day_leaves_monthly = 0
            employeeleaveModel.half_day_leaves_yr = 0
            employeeleaveModel.for_year = year
            employeeleaveModel.for_month = Month.objects.get(month_id=month)
            employeeleaveModel.excess_leave_yrsl = 0
            employeeleaveModel.excess_leave_yrhalf = 0
            employeeleaveModel.excess_leave_yrcl = 0
            employeeleaveModel.excess_leave_monthsl = 0
            employeeleaveModel.excess_leave_monthcl = 0
            employeeleaveModel.excess_leave_monthhalf = 0
            employeeleaveModel.save()
            employeeLeave = EmployeeLeave.objects.get(
                employee_id=id, for_month_id=month
            )
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
                    employeeLeave.excess_leave_monthcl = int(
                        employeeLeave.casual_leaves_monthly
                    ) - int(clMonth)
                    employeeLeave.save()
                if employeeLeave.casual_leaves_yr > clYear:
                    employeeLeave.excess_leave_yrcl = int(
                        employeeLeave.casual_leaves_yr
                    ) - int(clYear)
                    employeeLeave.save()
                return JsonResponse({"suceess": True}, status=200)

            elif leavereqModel.reason == leavetype.objects.get(leave_id=2):
                employeeLeave.sick_leaves_monthly += 1
                employeeLeave.sick_leaves_yr += 1
                employeeLeave.save()
                if employeeLeave.sick_leaves_monthly > slMonth:
                    employeeLeave.excess_leave_monthsl = int(
                        employeeLeave.sick_leaves_monthly
                    ) - int(slMonth)
                    employeeLeave.save()
                if employeeLeave.sick_leaves_yr > slYear:
                    employeeLeave.excess_leave_yrcl = int(
                        employeeLeave.sick_leaves_yr
                    ) - int(slYear)
                    employeeLeave.save()
                return JsonResponse({"suceess": True}, status=200)

            elif leavereqModel.reason == leavetype.objects.get(leave_id=3):
                employeeLeave.half_day_leaves_monthly += 1
                employeeLeave.half_day_leaves_yr += 1
                employeeLeave.save()
                if employeeLeave.half_day_leaves_monthly > hlMonth:
                    employeeLeave.excess_leave_monthhalf = int(
                        employeeLeave.half_day_leaves_monthly
                    ) - int(hlMonth)
                    employeeLeave.save()
                if employeeLeave.half_day_leaves_yr > hlYear:
                    employeeLeave.excess_leave_yrhalf = int(
                        employeeLeave.half_day_leaves_yr
                    ) - int(hlYear)
                    employeeLeave.save()
                return JsonResponse({"suceess": True}, status=200)
            else:
                return JsonResponse({"error": "Reason Not Found"})
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error":"Invalid Method"},status=405)


def declineLeave(request, id=0):
    if request.method == "GET":
        try:
            leavereqModel = leaveRequests.objects.get(employee_id=id)
            leavereqModel.status = Status.objects.get(status_id=5)
            leavereqModel.save()
            return JsonResponse({"suceess": True}, status=200)
        except leaveRequests.DoesNotExist:
            return JsonResponse({"error": "leaveRequests Not Found"}, status=404)
        except Status.DoesNotExist:
            return JsonResponse({"error": "Status Not Found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error":"Invalid Method"},status=405)


@csrf_exempt
def leaveStatus(request):
    if request.method == "GET":
        try:
            leavestatusMonthModel = LeavePolicyMonthly.objects.all()
            leavestatusYearModel = LeavePolicyYearly.objects.all()
            monthserializer = leavestatusMonthlySerializer(
                leavestatusMonthModel, many=True
            )
            yearserializer = leavestatusYearlySerializer(
                leavestatusYearModel, many=True
            )
            response = {"month": monthserializer.data, "year": yearserializer.data}
            return JsonResponse(response, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)})
        
    elif request.method == "POST":
        casualYr = request.POST.get("casualyr")
        sickYr = request.POST.get("sickyr")
        halfYr = request.POST.get("halfyr")
        casualMonth = request.POST.get("casualmonth")
        sickMonth = request.POST.get("sickmonth")
        halfMonth = request.POST.get("halfmonth")
        try:
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
            return JsonResponse({"success": True}, status=200)
        except LeavePolicyYearly.DoesNotExist:
            return JsonResponse({"error": "Year Policy Does Not EXists"}, status=404)
        except LeavePolicyMonthly.DoesNotExist:
            return JsonResponse({"error": "Month Policy Does Not Exists"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error":"Invalid Method"},status=405)


@csrf_exempt
def generatesalarymonth(request):
    if request.method == "POST":
        employee_id = request.POST.get("id")
        thisMonth = datetime.now().month
        thisYear = datetime.now().year
        today = datetime.now()
        salaryMonth = thisMonth
        numDays = calendar.monthrange(thisYear, salaryMonth)
        daysperMonth = numDays[1]
        try:
            employees = Employees.objects.get(employee_id=employee_id)
            monthObject = Month.objects.get(month_id=salaryMonth)
            if employeeSalary.objects.filter(
                employee=employees, salary_month=monthObject
            ).exists():
                print(employees)
                print(salaryMonth)
                return JsonResponse({"success": "Done"}, status=200)
            else:
                salaryModel = employeeSalary()
                salaryModel.employee = employees
                payperDay = int(employees.base_package) / int(daysperMonth)
                workingDays = today.day
                amountThismonth = payperDay * workingDays
                bonuses = Bonus.objects.filter(
                    employee=employee_id, bonus_month=salaryMonth, status=1
                )
                totalBonus = sum(bonus.bonus_amount for bonus in bonuses)
                reductions = Reduction.objects.filter(
                    employee=employee_id, reduction_month=salaryMonth, status=1
                )
                totalReduction = sum(reduction.reduction_amount for reduction in reductions)
                try:
                    employee_leave = EmployeeLeave.objects.get(
                        employee=employee_id, for_month=salaryMonth
                    )
                    excess_leave = (
                        int(employee_leave.excess_leave_monthcl)
                        + int(employee_leave.excess_leave_monthhalf)
                        + int(employee_leave.excess_leave_monthsl)
                        + int(employee_leave.excess_leave_yrcl)
                        + int(employee_leave.excess_leave_yrhalf)
                        + int(employee_leave.excess_leave_yrsl)
                    )
                    leave_reduction = int(excess_leave) * int(payperDay)
                except EmployeeLeave.DoesNotExist:
                    leave_reduction = 0

                total_salary = (
                    int(amountThismonth)
                    + int(totalBonus)
                    - int(totalReduction)
                    - int(leave_reduction)
                )

                salary_model = employeeSalary()
                salary_model.employee = Employees.objects.get(
                    employee_id=employees.employee_id
                )
                salary_model.base_package = amountThismonth
                salary_model.salary_month = Month.objects.get(month_id=salaryMonth)
                salary_model.total_bonus = totalBonus
                salary_model.total_reduction = totalReduction
                salary_model.leave_reductions = leave_reduction
                salary_model.generated_salary = math.floor(total_salary)
                salary_model.status = Status.objects.get(status_id=2)
                salary_model.save()
                bonuses = Bonus.objects.filter(
                    employee=employee_id, bonus_month=salaryMonth, status=1
                )
                for bonus in bonuses:
                    bonus.status = Status.objects.get(status_id=2)
                    bonus.save()
                reductions = Reduction.objects.filter(
                    employee=employee_id, reduction_month=salaryMonth, status=1
                )
                for reduction in reductions:
                    reduction.status = Status.objects.get(status_id=2)
                    reduction.save()
                employeeleaveModel = EmployeeLeave.objects.get(
                    employee=employees, for_month=monthObject
                )
                employeeleaveModel.sick_leaves_monthly = 0
                employeeleaveModel.casual_leaves_monthly = 0
                employeeleaveModel.half_day_leaves_monthly = 0
                employeeleaveModel.excess_leave_monthcl = 0
                employeeleaveModel.excess_leave_monthhalf = 0
                employeeleaveModel.excess_leave_monthsl = 0
                employeeleaveModel.save()
                return JsonResponse({"success": True}, status=200)
        except Employees.DoesNotExist:
            return JsonResponse({"error": "Employee not found"}, status=404)
        except Month.DoesNotExist:
            return JsonResponse({"error": "Month not found"}, status=404)
        except Status.DoesNotExist:
            return JsonResponse({"error": "Status not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error":"Invalid Method"},status=405)


def getallleavetype(request):
    if request.method == "GET":
        try:
            getallLeave = leavetype.objects.all()
            serializer = leavetypeSerializer(getallLeave, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
    else:
        return JsonResponse({"error":"Invalid Method"},status=405)


def remainingleave(request, id=0):
    if request.method == "GET":
        if id == 0:
            return JsonResponse({"error":"Employee ID Not Found"},status=404)
        try:
            thisMonth = datetime.now().month
            thisYear = datetime.now().year
            employeeleaveStatus = EmployeeLeave.objects.get(
                employee_id=id, for_month_id=thisMonth, for_year=thisYear
            )
            clthisYear = employeeleaveStatus.casual_leaves_yr
            clthisMonth = employeeleaveStatus.casual_leaves_monthly
            slthisYear = employeeleaveStatus.sick_leaves_yr
            slthisMonth = employeeleaveStatus.sick_leaves_monthly
            halfdaythisMonth = employeeleaveStatus.half_day_leaves_monthly
            halfdaythisYear = employeeleaveStatus.half_day_leaves_yr
            leavepolicyMonthly = LeavePolicyMonthly.objects.last()
            leavepolicyYearly = LeavePolicyYearly.objects.last()
            clperYear = leavepolicyYearly.casual_leaves
            clperMonth = leavepolicyMonthly.casual_leaves
            slperYear = leavepolicyYearly.sick_leaves
            slperMonth = leavepolicyMonthly.sick_leaves
            halfdaysperYear = leavepolicyYearly.half_day_leaves
            halfdaysperMonth = leavepolicyMonthly.half_day_leaves
            remainingclthisYear = clperYear - clthisYear
            remainingclthisMonth = clperMonth - clthisMonth
            if remainingclthisYear < 0:
                remainingclthisYear = 0
            if remainingclthisMonth < 0:
                remainingclthisMonth = 0
            remainingslthisYear = slperYear - slthisYear
            remainingslthisMonth = slperMonth - slthisMonth
            if remainingslthisYear < 0:
                remainingslthisYear = 0
            if remainingslthisMonth < 0:
                remainingslthisMonth = 0
            remaininghalfdaysthisYear = halfdaysperYear - halfdaythisYear
            remaininghalfdaysthisMonth = halfdaysperMonth - halfdaythisMonth
            if remaininghalfdaysthisYear < 0:
                remaininghalfdaysthisYear = 0
            if remaininghalfdaysthisMonth < 0:
                remaininghalfdaysthisMonth = 0

            data = {
                "clYear": remainingclthisYear,
                "clMonth": remainingclthisMonth,
                "slYear": remainingslthisYear,
                "slMonth": remainingslthisMonth,
                "halfYear": remaininghalfdaysthisYear,
                "halfMonth": remaininghalfdaysthisMonth,
            }
            print(data)
            return JsonResponse(data, safe=False, status=200)
        except EmployeeLeave.DoesNotExist:
            return JsonResponse({"error": "Leave record not found for the employee"}, status=404)
        except LeavePolicyMonthly.DoesNotExist:
            return JsonResponse({"error": "Leave policy monthly record not found"}, status=404)
        except LeavePolicyYearly.DoesNotExist:
            return JsonResponse({"error": "Leave policy yearly record not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def leavereductions(request, id=0):
    if request.method == "GET":
        if id:
            try:
                leaveReductionModel = leaveReductions.objects.filter(employee_id=id)
                serializer = leavereductionSerializer(leaveReductionModel, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
            except leaveReductions.DoesNotExist:
                return JsonResponse({"error":"leaveReductions Doesnt Exists"},status=404)
            except Exception as e:
                return JsonResponse({"error":str(e)},status=500)
        else:
            try:
                thisMonth = datetime.now().month
                thisYear = datetime.now().year
                if thisMonth == 1:
                    salaryMonth = 12
                    salaryYear = thisYear - 1
                else:
                    salaryMonth = thisMonth - 1
                    salaryYear = thisYear

                monthDetails = Month.objects.get(month_id=salaryMonth)
                employeeDetails = Employees.objects.all()
                for employees in employeeDetails:
                    id = employees.employee_id
                    basePackage = employees.base_package
                    try:

                        employeeleaveStatus = EmployeeLeave.objects.get(
                            employee_id=id,
                            for_month_id=monthDetails.month_id,
                            for_year=salaryYear,
                        )
                    except EmployeeLeave.DoesNotExist:
                        continue

                    excessClYear = employeeleaveStatus.excess_leave_yrcl
                    excessSlYear = employeeleaveStatus.excess_leave_yrsl
                    excessHalfDaysYear = employeeleaveStatus.excess_leave_yrhalf
                    excessClMonth = employeeleaveStatus.excess_leave_monthcl
                    excessSlMonth = employeeleaveStatus.excess_leave_monthsl
                    excessHalfDaysMonth = employeeleaveStatus.excess_leave_monthhalf
                    totalExcesss = (
                        excessClYear
                        + excessSlYear
                        + excessHalfDaysYear
                        + excessClMonth
                        + excessSlMonth
                        + excessHalfDaysMonth
                    )

                    numDays = calendar.monthrange(salaryYear, salaryMonth)
                    daysperMonth = numDays[1]
                    payperDay = basePackage / daysperMonth

                    if leaveReductions.objects.filter(
                        employee_id=id, for_month=monthDetails, for_year=thisYear
                    ).exists():
                        continue
                    leaveReductionModel = leaveReductions()
                    leaveReductionModel.employee = Employees.objects.get(employee_id=id)
                    leaveReductionModel.pay_per_day = payperDay
                    leaveReductionModel.total_excess_leave = totalExcesss
                    leaveReductionModel.reduction_amount = payperDay * totalExcesss
                    leaveReductionModel.excess_leave_monthcl = excessClMonth
                    leaveReductionModel.excess_leave_monthhalf = excessHalfDaysMonth
                    leaveReductionModel.excess_leave_monthsl = excessSlMonth
                    leaveReductionModel.excess_leave_yrcl = excessClYear
                    leaveReductionModel.excess_leave_yrhalf = excessHalfDaysYear
                    leaveReductionModel.excess_leave_yrsl = excessSlYear
                    leaveReductionModel.for_month = monthDetails
                    leaveReductionModel.for_year = thisYear
                    leaveReductionModel.save()
                return JsonResponse({"success": True})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def forgetPassword(request):
    if request.method == "POST":
        zoohr_id = request.POST.get("zoohrid")
        try:
            employeeCheck = Login.objects.filter(username=zoohr_id)
            if employeeCheck.exists():
                for employee in employeeCheck:
                    employeeID = employee.employee.employee_id
                    emplolyeeStatus = Employees.objects.get(employee_id=employeeID)
                    employeeMail = emplolyeeStatus.employee_mail
                    thisDate = datetime.now().date()
                    thisTime = datetime.now().time()
                    otp = random.randint(100000, 999999)
                    send_mail(
                        "Your OTP Code",
                        f"Your OTP code is: {otp}",
                        "zoondiahr2024@gmail.com",
                        [employeeMail],
                        fail_silently=False,
                    )
                    otpModel = OtpFunction()
                    otpModel.otp = otp
                    otpModel.employee = employee.employee
                    otpModel.otp_date = thisDate
                    otpModel.otp_time = thisTime
                    otpModel.send_to = employeeMail
                    otpModel.save()
                    return JsonResponse({"success": True, "employeeID": employeeID}, status=200)
            else:
                return JsonResponse({"success": "Done"}, status=200)
        except Employees.DoesNotExist:
                return JsonResponse({"error": "Employee does not exist"}, status=404)
        except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    


@csrf_exempt
def otpValidation(request, id=0):
    if request.method == "POST":
        enteredOTP = request.POST.get("otp")
        try:
            employeeID = Employees.objects.get(employee_id=id)
            lastOTP = OtpFunction.objects.filter(employee=employeeID).last()
            print(lastOTP.otp)
            if int(enteredOTP) == int(lastOTP.otp):
                return JsonResponse({"success": True}, status=200)
            else:
                return JsonResponse({"fail": True}, status=200)
        except Employees.DoesNotExist:
            return JsonResponse({"error": "Employee Doesnt Exists"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Method Not Allowed"}, status=405)


@csrf_exempt
def changePassword(request, id=0):
    if request.method == "POST":
        newPassword = request.POST.get("password")
        try:
            employeeID = Employees.objects.get(employee_id=id)
            loginModel = Login.objects.get(employee=employeeID)
            loginModel.password = newPassword
            loginModel.save()
            return JsonResponse({"success": True}, status=200)
        except Employees.DoesNotExist:
            return JsonResponse({"error": "Employee not Found"}, status=401)
        except Login.DoesNotExist:
            return JsonResponse({"error": "Login Doesn't Exist"})
    else:
        return JsonResponse({"error": "Method Not Allowed"}, status=405)


@csrf_exempt
def contactAdmin(request, id=0):
    if request.method == "POST":
        subject = request.POST.get("subject")
        description = request.POST.get("description")
        file = request.FILES.get("file")
        date = datetime.now().date()
        contactAdminModel = AdminContact()
        try:
            employeeID = Employees.objects.get(employee_id=id)
            contactAdminModel.subject = subject
            contactAdminModel.description = description
            contactAdminModel.employee = employeeID
            contactAdminModel.date = date
            if file:
                contactAdminModel.file = file
            contactAdminModel.save()
            return JsonResponse({"success": True}, status=200)
        except Employees.DoesNotExist:
            return JsonResponse({"error":"Employee Not Found"},status=401)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
    elif request.method == "GET":
        if id:
            try:
                contactAdminModel = AdminContact.objects.filter(id=id)
                serializer = ContactadminSerializer(contactAdminModel, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
            except AdminContact.DoesNotExist:
                return JsonResponse({"error":"Not Found"},status=401)
            except Exception as e:
                return JsonResponse({"error":str(e)},status=500)
        else:
            try:
                contactAdminModel = AdminContact.objects.select_related("employee").all()
                serializer = ContactadminSerializer(contactAdminModel, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
            except Exception as e:
                return JsonResponse({"error":str(e)},status=500)
    elif request.method == "DELETE":
        try:
            messageDelete = AdminContact.objects.get(id=id)
            messageDelete.delete()
            return JsonResponse({"success": True}, status=200)
        except AdminContact.DoesNotExist:
            return JsonResponse({"error": "Message Not Found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method Not Found"}, status=404)


def checkLeavePolicy(request):
    if request.method == "GET":
        try:
            leavePolicy = LeavePolicyYearly.objects.last()
            if leavePolicy:
                return JsonResponse({"success": False})
            else:
                return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": "Method Not Found"}, status=404)


def checkMonth(request):
    if request.method == "GET":
        try:
            monthCheck = Month.objects.last()
            if monthCheck:
                return JsonResponse({"success": False})
            else:
                months = [
                    (1, "JANUARY"),
                    (2, "FEBRUARY"),
                    (3, "MARCH"),
                    (4, "APRIL"),
                    (5, "MAY"),
                    (6, "JUNE"),
                    (7, "JULY"),
                    (8, "AUGUST"),
                    (9, "SEPTEMBER"),
                    (10, "OCTOBER"),
                    (11, "NOVEMBER"),
                    (12, "DECEMBER"),
                ]
                getMonth = Month()
                for month_id, month_name in months:
                    getMonth.month_id = month_id
                    getMonth.month_name = month_name
                    getMonth.save()
                return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method Not Found"}, status=404)


def checkStatus(request):
    if request.method == "GET":
        try:
            statusCheck = Status.objects.last()
            if statusCheck:
                return JsonResponse({"success": False})
            else:
                status = [
                    (1, "NOT GENERATED"),
                    (2, "GENERATED"),
                    (3, "NOT APPROVED"),
                    (4, "APPROVED"),
                    (5, "DECLINED"),
                    (6, "ACTIVE"),
                    (7, "BLOCKED"),
                ]
                getStatus = Status()
                for status_id, status_name in status:
                    getStatus.status_id = status_id
                    getStatus.status_name = status_name
                    getStatus.save()
                return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method Not Found"}, status=404)


@csrf_exempt
def addpolicy(request):
    if request.method == "POST":
        casualYr = request.POST.get("casualyr")
        sickYr = request.POST.get("sickyr")
        halfYr = request.POST.get("halfyr")
        casualMonth = request.POST.get("casualmonth")
        sickMonth = request.POST.get("sickmonth")
        halfMonth = request.POST.get("halfmonth")
        try:
            policyYear = LeavePolicyYearly()
            policyYear.casual_leaves = casualYr
            policyYear.sick_leaves = sickYr
            policyYear.half_day_leaves = halfYr
            policyYear.save()
            policyMonth = LeavePolicyMonthly()
            policyMonth.casual_leaves = casualMonth
            policyMonth.sick_leaves = sickMonth
            policyMonth.half_day_leaves = halfMonth
            policyMonth.save()
            return JsonResponse({"success": True}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method Not Found"}, status=404)


def blockemployee(request, id=0):
    if request.method == "GET":
        try:
            getEmployee = Employees.objects.get(employee_id=id)
            getEmployee.status = Status.objects.get(status_id=7)
            getEmployee.save()
            return JsonResponse({"success": True}, status=200)
        except Employees.DoesNotExist:
            return JsonResponse({"error": "Employee Not Found"}, status=401)
        except Status.DoesNotExist:
            return JsonResponse({"error": "Status Not Found"}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method Not Found"}, status=404)


def unblockemployee(request, id=0):
    if request.method == "GET":
        try:
            getEmployee = Employees.objects.get(employee_id=id)
            getEmployee.status = Status.objects.get(status_id=6)
            getEmployee.save()
            return JsonResponse({"success": True}, status=200)
        except Employees.DoesNotExist:
            return JsonResponse({"error": "Employee Not Found"}, status=401)
        except Status.DoesNotExist:
            return JsonResponse({"error": "Status Not Found"}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method Not Found"}, status=404)


def count(request):
    if request.method == "GET":
        try:
            employeeCount = Employees.objects.count()
            messageCount = AdminContact.objects.count()
            statusObject = Status.objects.get(status_id=3)
            leaveCount = leaveRequests.objects.filter(status=statusObject).count()
            data = {
                "employeeCount": employeeCount,
                "messageCount": messageCount,
                "leaveCount": leaveCount,
            }
            return JsonResponse(data, safe=False)
        except Status.DoesNotExist:
            return JsonResponse({"error": "Status Not Found"}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method Not Found"}, status=404)
        


def addLeaveType(request):
    if request.method == "GET":
        try:
            checkLeave = leavetype.objects.last()
            if checkLeave:
                return JsonResponse({"success": True}, status=200)
            else:
                leavetypes = [
                    (1, "CASUAL LEAVE"),
                    (2, "SICK LEAVE"),
                    (3, "HALF DAY LEAVE"),
                ]
                leavetypeModel = leavetype()
                for leave_id, leave_name in leavetypes:
                    leavetypeModel.leave_id = leave_id
                    leavetypeModel.leave_name = leave_name
                    leavetypeModel.save()
                return JsonResponse({"success": "Done"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method Not Found"}, status=404)
