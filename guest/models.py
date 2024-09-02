from django.db import models

# Create your models here.

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
    def __str__(main):
        return main.username
    
class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
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
