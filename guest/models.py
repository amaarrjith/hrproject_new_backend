from django.db import models

# Create your models here.

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
    def __str__(main):
        return main.username
    
class Employees(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=50)
    employee_mail = models.CharField((""), max_length=50)
    post = models.CharField((""), max_length=50)
    base_package = models.BigIntegerField((""))
    registered_date = models.DateField()
    
    def __str__(main):
        return main.employee_name
    
class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employees,on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
    def __str__(main):
        return main.username

class Month(models.Model):
    month_id = models.AutoField(primary_key=True)
    month_name = models.CharField((""), max_length=50)
    
    def __str__(main):
        return main.month_name
    
class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField((""), max_length=50)
    
class Bonus(models.Model):
    bonus_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employees,on_delete=models.CASCADE)
    bonus_amount = models.BigIntegerField((""))
    bonus_reason = models.CharField((""), max_length=50)
    bonus_month = models.ForeignKey(Month, on_delete=models.CASCADE)
    added_on = models.DateField((""), auto_now=False, auto_now_add=False)
    status = models.ForeignKey(Status,on_delete=models.CASCADE)
    
    def __str__(main):
        return main.bonus_id
    
class Reduction(models.Model):
    reduction_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employees,on_delete=models.CASCADE)
    reduction_amount = models.BigIntegerField((""))
    reduction_reason = models.CharField((""), max_length=50)
    reduction_month = models.ForeignKey(Month, on_delete=models.CASCADE)
    added_on = models.DateField((""), auto_now=False, auto_now_add=False)
    status = models.ForeignKey(Status,on_delete=models.CASCADE)
    
    def __str__(main):
        return main.reduction_id
    
class LeavePolicyYearly(models.Model):
    id = models.AutoField(primary_key=True)
    casual_leaves = models.IntegerField()
    sick_leaves = models.IntegerField()
    half_day_leaves = models.IntegerField()
    
    
    def __str__(main):
        return main.id
    
class LeavePolicyMonthly(models.Model):
    id = models.AutoField(primary_key=True)
    casual_leaves = models.IntegerField()
    sick_leaves = models.IntegerField()
    half_day_leaves = models.IntegerField()
    
    
    def __str__(main):
        return main.id
    
class EmployeeLeave(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    casual_leaves_yr = models.IntegerField()
    sick_leaves_yr = models.IntegerField()
    half_day_leaves_yr = models.IntegerField()
    casual_leaves_monthly = models.IntegerField()
    sick_leaves_monthly = models.IntegerField()
    half_day_leaves_monthly = models.IntegerField()
    excess_leave_monthcl = models.IntegerField()
    excess_leave_monthsl = models.IntegerField()
    excess_leave_monthhalf = models.IntegerField()
    excess_leave_yrcl = models.IntegerField()
    excess_leave_yrsl = models.IntegerField()
    excess_leave_yrhalf = models.IntegerField()
    
    for_month = models.ForeignKey(Month, on_delete=models.CASCADE)
    for_year = models.IntegerField()

    def __str__(main):
        return main.id

class employeeSalary(models.Model):
    salary_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employees,on_delete=models.CASCADE)
    salary_month = models.ForeignKey(Month,on_delete=models.CASCADE)
    base_package = models.BigIntegerField()
    total_reduction = models.BigIntegerField()
    total_bonus = models.BigIntegerField()
    leave_reductions = models.BigIntegerField()
    generated_salary = models.BigIntegerField()
    status = models.ForeignKey(Status,on_delete=models.CASCADE)

    def __str__(main):
        return main.salary_id
    
class leavetype(models.Model):
    leave_id = models.AutoField(primary_key=True)
    leave_name = models.CharField(max_length=50)
    
    def __str__(main):
        return main.leave_name

class leaveRequests(models.Model):
    leave_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employees,on_delete=models.CASCADE)
    leave_date = models.DateField((""), auto_now=False, auto_now_add=False)
    reason = models.ForeignKey(leavetype,on_delete=models.CASCADE)
    status = models.ForeignKey(Status,on_delete=models.CASCADE)
    
    def __str__(main):
        return main.leave_id
    
class leaveReductions(models.Model):
    employee = models.ForeignKey(Employees,on_delete=models.CASCADE)
    
    excess_leave_monthcl = models.IntegerField()
    excess_leave_monthsl = models.IntegerField()
    excess_leave_monthhalf = models.IntegerField()
    excess_leave_yrcl = models.IntegerField()
    excess_leave_yrsl = models.IntegerField()
    excess_leave_yrhalf = models.IntegerField()
    for_month = models.ForeignKey(Month, on_delete=models.CASCADE)
    for_year = models.IntegerField()
    total_excess_leave = models.IntegerField()
    pay_per_day = models.BigIntegerField((""))
    reduction_amount = models.BigIntegerField(("")) 
    
    def __str__(main):
        return main.employee
