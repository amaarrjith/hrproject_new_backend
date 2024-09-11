from rest_framework import serializers
from guest.models import *
class statusSerializers(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"
        
class employeeSerializers(serializers.ModelSerializer):
    status = statusSerializers()
    class Meta:
        model = Employees
        fields = '__all__'
        
class loginSerializers(serializers.ModelSerializer):
    employee = employeeSerializers()
    class Meta:
        model = Login
        fields = '__all__'
 
class monthSerializers(serializers.ModelSerializer):
    class Meta:
        model = Month
        fields = '__all__'
        

               
class bonusSerializers(serializers.ModelSerializer):
    employee = employeeSerializers()
    bonus_month = monthSerializers()
    status = statusSerializers()
    class Meta:
        model = Bonus
        fields = '__all__'
        
class reductionSerializers(serializers.ModelSerializer):
    employee = employeeSerializers()
    reduction_month = monthSerializers()
    status = statusSerializers()
    class Meta:
        model = Reduction
        fields = '__all__'

class salarySerializer(serializers.ModelSerializer):
    employee = employeeSerializers()
    salary_month = monthSerializers()
    status = statusSerializers()
    class Meta:
        model = employeeSalary
        fields = '__all__'

class leavetypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = leavetype
        fields = '__all__'  
         
class leaverequestsSerializer(serializers.ModelSerializer):
    employee = employeeSerializers()
    status = statusSerializers()
    reason = leavetypeSerializer()
    class Meta:
        model = leaveRequests
        fields = '__all__'
        
class leavestatusYearlySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavePolicyYearly
        fields = '__all__'
                
class leavestatusMonthlySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavePolicyMonthly
        fields = '__all__'

class leavereductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = leaveReductions
        fields = '__all__'
        
class ContactadminSerializer(serializers.ModelSerializer):
    employee = employeeSerializers()
    class Meta:
        model = AdminContact
        fields = '__all__'
        
class leavepolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavePolicyYearly
        fields = '__all__'